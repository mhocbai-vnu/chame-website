"""Kiểm thử luồng thực tế trên SQLite riêng. Không dùng dữ liệu demo sản xuất."""
import os, tempfile, io, json, uuid, re
from pathlib import Path
ROOT=Path(tempfile.mkdtemp(prefix='chamea-test-'))
os.environ['DATABASE_URL']='sqlite:///'+str(ROOT/'test.db')
os.environ['MEDIA_DIR']=str(ROOT/'media')
os.environ['SESSION_SECURE']='false'
from fastapi.testclient import TestClient
from PIL import Image
from sqlalchemy import select
from app.main import app
from app.db import SessionLocal
from app.models import User, Page, Product, Variant, Order, Audit
from app.core import hash_password, sha, jdumps, jloads, quote, validate_layout


def jpeg_bytes():
    img=Image.new('RGB',(96,96),(182,160,152));o=io.BytesIO();img.save(o,format='JPEG');return o.getvalue()

def test_shop_order_cms_and_security():
    with TestClient(app) as c:
        assert c.get('/').status_code==200
        assert c.get('/san-pham').status_code==200
        assert c.get('/quan-tri',follow_redirects=False).status_code==303
        assert c.post('/api/orders',json={'items':[],'method':'COD','idempotency_key':'a'*35}).status_code==409
        with SessionLocal() as db:
            db.add(User(email='owner@example.test',password_hash=hash_password('OnlyForTest123!'),role='owner'));db.commit()
        response=c.post('/quan-tri/dang-nhap',data={'email':'owner@example.test','password':'OnlyForTest123!'},follow_redirects=False)
        assert response.status_code==303
        # Session cookie thật và CSRF từ trang quản trị
        d=c.get('/quan-tri/cai-dat'); assert d.status_code==200
        csrf=re.search(r'name="csrf" value="([^"]+)"',d.text).group(1)
        wrong=c.post('/api/admin/media',files={'file':('fake.jpg',b'not-image','image/jpeg')})
        assert wrong.status_code==403
        bad=c.post('/api/admin/media',files={'file':('fake.jpg',b'not-image','image/jpeg')},headers={'X-CSRF-Token':csrf})
        assert bad.status_code==422
        media=c.post('/api/admin/media',files={'file':('own.jpg',jpeg_bytes(),'image/jpeg')},headers={'X-CSRF-Token':csrf});assert media.status_code==200,media.text
        mid=media.json()['id'];assert c.get('/media/'+media.json()['url'].split('/')[-1]).status_code==200
        # Tạo sản phẩm qua CMS
        f={'csrf':csrf,'name':'Túi mẫu kiểm thử','sku':'TST-001','summary':'Mẫu chỉ tồn tại trong kiểm thử','images':str(mid),'published':'on','styles':'tối giản','uses':'đi làm'}
        r=c.post('/quan-tri/noi-dung/san-pham/0',data=f,follow_redirects=False);assert r.status_code==303,r.text
        prod_id=int(r.headers['location'].split('/')[-1].split('?')[0]); assert c.get('/san-pham/tui-mau-kiem-thu').status_code==200
        f={'csrf':csrf,'name':'Màu nâu','sku':'TST-001-NAU','price':'580000','stock':'5','active':'on','image_id':str(mid)}
        r=c.post(f'/quan-tri/bien-the/{prod_id}',data=f,follow_redirects=False);assert r.status_code==303,r.text
        with SessionLocal() as db:
            variant=db.scalar(select(Variant).where(Variant.product_id==prod_id));vid=variant.id
            policies=db.scalars(select(Page).where(Page.slug.in_(['giao-hang','doi-tra','bao-mat']))).all()
            for page in policies:
                page.live=jdumps({'sections':[{'id':'s','settings':{},'rows':[{'id':'r','columns':[{'id':'c','span':12,'blocks':[{'id':'b','type':'text','content':{'text':'Chính sách kiểm thử, không dùng ngoài bài test.'},'style':{},'responsive':{}}]}]}]}]})
                page.published=True
            db.commit()
        # Lưu một lần cấu hình thực tế giả lập chỉ trong DB test
        f={'csrf':csrf,'brand_logo':str(mid),'phone':'0987654321','email':'sample@chamea.test','address':'Số 10, Đường Thử Nghiệm, Hà Nội','shipping_flat':'35000','qr_bank':'TEST BANK','qr_holder':'TEST HOLDER','qr_account':'000123456','qr_media':str(mid),'theme_primary':'#3C2535','theme_accent':'#AB8A6B','theme_bg':'#FEFBFD','menu':'[]'}
        assert c.post('/quan-tri/cai-dat',data=f,follow_redirects=False).status_code==303
        r=c.post('/quan-tri/mo-ban',data={'csrf':csrf,'enabled':'on'},follow_redirects=False);assert r.status_code==303,r.text
        q=c.post('/api/quote',json={'items':[{'variant_id':vid,'quantity':2}]});assert q.status_code==200,q.text
        assert q.json()['total']==1195000
        badmethod=c.post('/api/orders',json={'idempotency_key':'b'*40,'items':[{'variant_id':vid,'quantity':1}],'name':'Nguyễn Thị A','phone':'0987654321','address':'Một địa chỉ hợp lệ trên 10 ký tự','method':'CARD'})
        assert badmethod.status_code==422
        order_req={'idempotency_key':'c'*40,'items':[{'variant_id':vid,'quantity':2}],'name':'Nguyễn Thị A','phone':'0987654321','address':'Số 12, phố Kiểm Thử, Hà Nội','method':'COD'}
        a=c.post('/api/orders',json=order_req);assert a.status_code==200,a.text
        d=c.post('/api/orders',json=order_req);assert d.status_code==200 and d.json()['duplicate']
        assert a.json()['code']==d.json()['code']; assert c.get(a.json()['receipt']).status_code==200
        qr=dict(order_req,idempotency_key='d'*40,method='QR',items=[{'variant_id':vid,'quantity':1}])
        qr_resp=c.post('/api/orders',json=qr);assert qr_resp.status_code==200,qr_resp.text
        qr_path=qr_resp.json()['receipt'];assert 'QR cố định' in c.get(qr_path).text
        token=qr_path.split('/')[-1]
        with SessionLocal() as db: assert db.scalar(select(Order).where(Order.method=='QR')).payment_status=='unpaid'
        assert c.post('/api/orders/'+token+'/verify').status_code==200
        with SessionLocal() as db:
            created=db.scalars(select(Order)).all();assert len(created)==2
            assert next(x for x in created if x.method=='COD').payment_status=='unpaid'
            assert next(x for x in created if x.method=='QR').payment_status=='pending_verification'
            assert 'TEST BANK' in next(x for x in created if x.method=='QR').payment_snapshot
            assert db.get(Variant,vid).stock==2
        # Bản nháp builder riêng với bản công khai + optimistic locking
        with SessionLocal() as db: page=db.scalar(select(Page).where(Page.slug=='trang-chu'));pid=page.id;previous=page.live
        data=c.get(f'/api/admin/layout/trang/{pid}').json();assert data['layout']['sections']
        upd=c.put(f'/api/admin/layout/trang/{pid}',json={'layout':data['layout'],'version':data['version']},headers={'X-CSRF-Token':csrf});assert upd.status_code==200,upd.text
        assert c.put(f'/api/admin/layout/trang/{pid}',json={'layout':data['layout'],'version':data['version']},headers={'X-CSRF-Token':csrf}).status_code==409
        with SessionLocal() as db:assert db.get(Page,pid).live==previous
        assert c.post(f'/api/admin/layout/trang/{pid}/publish',headers={'X-CSRF-Token':csrf}).status_code==200
        assert c.post('/api/admin/media/'+str(mid)+'/delete',headers={'X-CSRF-Token':csrf}).status_code==409
        # Price does not come from client
        impossible=c.post('/api/quote',json={'items':[{'variant_id':vid,'quantity':50,'price':1}]});assert impossible.status_code==422
        assert c.get('/khong-ton-tai-ne').status_code==404
        for path in ['/','/gio-hang','/thanh-toan','/goi-y-chon-qua','/san-pham/tui-mau-kiem-thu','/sitemap.xml']:
            assert c.get(path).status_code==200,path


def test_layout_xss_and_bad_url():
    raw={'sections':[{'rows':[{'columns':[{'blocks':[{'type':'richtext','content':{'html':'<script>alert(1)</script><p>OK</p>'},'style':{}}]}]}]}]}
    clean=validate_layout(raw)
    html=clean['sections'][0]['rows'][0]['columns'][0]['blocks'][0]['content']['html']
    assert '<script>' not in html and '<p>OK</p>' in html
    raw['sections'][0]['rows'][0]['columns'][0]['blocks'][0]={'type':'button','content':{'href':'javascript:alert(1)'},'style':{}}
    assert validate_layout(raw)['sections'][0]['rows'][0]['columns'][0]['blocks'][0]['content']['href']=='#'
