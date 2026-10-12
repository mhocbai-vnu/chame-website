import os, re, json, secrets, hashlib, mimetypes, shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session
from PIL import Image, UnidentifiedImageError
from .db import get_db
from .models import *
from .core import *
from .seed import layout, section, b

router=APIRouter()

def admin_view(request,db,template,roles=('owner','content','orders'),**extra):
    from .main import render
    u,s=require(db,request,roles)
    return render(request,db,'admin/'+template,user=u,csrf=s.csrf,noindex=True,**extra)

def csrf_form(form,session):
    if not form.get('csrf') or not secrets.compare_digest(str(form.get('csrf')),session.csrf):raise HTTPException(403,'Thiếu xác thực CSRF')

def slug_unique(db,model,slug,exclude=0):
    stmt=select(model).where(model.slug==slug)
    existing=db.scalar(stmt)
    if existing and existing.id!=exclude:raise HTTPException(422,'Đường dẫn (slug) đã tồn tại')

def tobool(s):return s in ('1','on','true',True)

def normalize_idlist(s):
    return [int(x) for x in str(s).split(',') if x.strip().isdigit()][:100]

@router.get('/quan-tri/dang-nhap')
def login_page(request:Request,db:Session=Depends(get_db)):
    from .main import render
    return render(request,db,'admin/login.html',noindex=True)

@router.post('/quan-tri/dang-nhap')
async def login(request:Request,db:Session=Depends(get_db)):
    from .main import throttle,render
    throttle(request,'login',6,300)
    form=await request.form()
    email=str(form.get('email','')).lower().strip()[:200]
    password=str(form.get('password',''))
    user=db.scalar(select(User).where(User.email==email))
    if not user or not user.active or not verify_password(password,user.password_hash):
        return render(request,db,'admin/login.html',error='Email hoặc mật khẩu không đúng',noindex=True)
    token=secrets.token_urlsafe(48)
    db.add(LoginSession(user_id=user.id,token_hash=sha(token),csrf=secrets.token_urlsafe(32),expires=datetime.now(timezone.utc)+timedelta(hours=12)))
    db.commit()
    response=RedirectResponse('/quan-tri',status_code=303)
    response.set_cookie('chamea_session',token,max_age=43200,httponly=True,secure=os.getenv('SESSION_SECURE','false').lower()=='true',samesite='lax',path='/')
    return response

@router.post('/quan-tri/dang-xuat')
async def logout(request:Request,db:Session=Depends(get_db)):
    form=await request.form()
    u,s=require(db,request)
    csrf_form(form,s)
    db.delete(s);db.commit()
    resp=RedirectResponse('/quan-tri/dang-nhap',status_code=303)
    resp.delete_cookie('chamea_session',path='/')
    return resp

@router.get('/quan-tri')
def dashboard(request:Request,db:Session=Depends(get_db)):
    u,s=require(db,request)
    counts={'products':db.scalar(select(func.count()).select_from(Product)),'orders':db.scalar(select(func.count()).select_from(Order)),'posts':db.scalar(select(func.count()).select_from(Post).where(Post.deleted==False)),'leads':db.scalar(select(func.count()).select_from(Lead))}
    recent=db.scalars(select(Order).order_by(Order.created_at.desc()).limit(8)).all()
    missing=[]
    for key,name in [('brand_logo','Logo gốc'),('phone','Số điện thoại'),('email','Email liên hệ'),('shipping_flat','Phí vận chuyển'),('qr_bank','Tên ngân hàng QR'),('qr_holder','Chủ tài khoản QR'),('qr_account','Số tài khoản QR'),('qr_media','Tệp mã QR')]:
        if not config(db,key):missing.append(name)
    if not db.scalar(select(Product).where(Product.published==True)):missing.append('Sản phẩm đã xác minh và xuất bản')
    return admin_view(request,db,'dashboard.html',counts=counts,recent=recent,missing=missing,opened=is_open(db))

@router.get('/quan-tri/don-hang')
def orders_page(request:Request,db:Session=Depends(get_db),q:str='',status:str=''):
    require(db,request,('owner','orders'))
    stmt=select(Order)
    if q: stmt=stmt.where(or_(Order.code.ilike('%'+q[:70]+'%'),Order.phone.ilike('%'+q[:70]+'%')))
    if status:stmt=stmt.where(Order.status==status)
    return admin_view(request,db,'orders.html',roles=('owner','orders'),orders=db.scalars(stmt.order_by(Order.created_at.desc()).limit(250)).all(),q=q,status=status)

@router.get('/quan-tri/don-hang/{id}')
def order_view(request:Request,id:int,db:Session=Depends(get_db)):
    require(db,request,('owner','orders'))
    order=db.get(Order,id)
    if not order:raise HTTPException(404)
    rows=db.scalars(select(OrderItem).where(OrderItem.order_id==id)).all()
    history=db.scalars(select(Audit).where(Audit.entity=='order',Audit.entity_id==str(id)).order_by(Audit.created_at.desc())).all()
    return admin_view(request,db,'order.html',roles=('owner','orders'),order=order,rows=rows,history=history)

@router.post('/quan-tri/don-hang/{id}')
async def update_order(request:Request,id:int,db:Session=Depends(get_db)):
    user,session=require(db,request,('owner','orders'))
    f=await request.form();csrf_form(f,session)
    order=db.get(Order,id)
    if not order:raise HTTPException(404)
    status=str(f.get('status',''))
    payment=str(f.get('payment_status',''))
    if status not in ('new','processing','shipped','delivered','cancelled'):raise HTTPException(422,'Trạng thái đơn không hợp lệ')
    if payment not in ('unpaid','pending_verification','paid','refunded'):raise HTTPException(422,'Trạng thái thanh toán không hợp lệ')
    before=f'{order.status}/{order.payment_status}'
    if order.status!='cancelled' and status=='cancelled':
        for item in db.scalars(select(OrderItem).where(OrderItem.order_id==id)).all():
            variant=db.get(Variant,item.variant_id) if item.variant_id else None
            if variant and variant.stock is not None:variant.stock+=item.quantity
    if order.status=='cancelled' and status!='cancelled':
        for item in db.scalars(select(OrderItem).where(OrderItem.order_id==id)).all():
            variant=db.get(Variant,item.variant_id) if item.variant_id else None
            if variant and variant.stock is not None:
                if variant.stock<item.quantity:raise HTTPException(409,'Không đủ tồn kho để mở lại đơn đã hủy')
                variant.stock-=item.quantity
    order.status=status;order.payment_status=payment;order.internal_note=str(f.get('internal_note',''))[:2000]
    audit(db,user,'update_order','order',id,f'{before} -> {status}/{payment}')
    db.commit()
    return RedirectResponse(f'/quan-tri/don-hang/{id}',status_code=303)

@router.get('/quan-tri/yeu-cau')
def leads_page(request:Request,db:Session=Depends(get_db)):
    return admin_view(request,db,'leads.html',roles=('owner','orders','content'),leads=db.scalars(select(Lead).order_by(Lead.created_at.desc()).limit(250)).all(),news=db.scalars(select(Newsletter).order_by(Newsletter.created_at.desc()).limit(250)).all())

@router.get('/quan-tri/cai-dat')
def settings_page(request:Request,db:Session=Depends(get_db)):
    return admin_view(request,db,'settings.html',roles=('owner',),configs={c.key:c.value for c in db.scalars(select(Config)).all()},media=db.scalars(select(Media).order_by(Media.created_at.desc())).all(),ready=qr_ready(db))

SETTINGS_EDIT={'announcement','announcement_enabled','sticky_header','brand_logo','hero_image','hero_mobile','gift_image','brand_video','brand_video_poster','phone','email','address','facebook','instagram','shipping_flat','qr_bank','qr_holder','qr_account','qr_media','seo_title','seo_description','theme_primary','theme_accent','theme_bg','menu'}
@router.post('/quan-tri/cai-dat')
async def save_settings(request:Request,db:Session=Depends(get_db)):
    user,s=require(db,request,('owner',))
    f=await request.form();csrf_form(f,s)
    previous={k:config(db,k) for k in ('qr_bank','qr_holder','qr_account','qr_media','shipping_flat')}
    for key in SETTINGS_EDIT:
        if key in f:
            val=str(f[key]).strip()[:4000]
            if key=='shipping_flat' and val and (not val.isdigit() or int(val)>10000000):raise HTTPException(422,'Phí vận chuyển phải là số VNĐ hợp lệ')
            if key.startswith('theme_') and not re.fullmatch(r'#[0-9a-fA-F]{6}',val):raise HTTPException(422,'Mã màu không hợp lệ')
            if key in ('brand_logo','hero_image','hero_mobile','gift_image','brand_video','brand_video_poster','qr_media') and val and (not val.isdigit() or not db.get(Media,int(val))):raise HTTPException(422,'Ảnh/video được chọn không tồn tại')
            if key in ('brand_logo','hero_image','hero_mobile','gift_image','brand_video','brand_video_poster','qr_media') and val:
                med=db.get(Media,int(val))
                if key=='brand_video' and not med.mime.startswith('video/'):raise HTTPException(422,'Video thương hiệu phải là tệp video')
                if key!='brand_video' and not med.mime.startswith('image/'):raise HTTPException(422,'Thông tin chọn ảnh phải là tệp hình hợp lệ')
            if key=='menu':
                try:
                    menus=json.loads(val)
                    if not isinstance(menus,list) or len(menus)>30:raise ValueError()
                    val=jdumps([{'text':str(x['text'])[:80],'url':safe_href(str(x['url']))} for x in menus])
                except Exception:raise HTTPException(422,'Menu phải là danh sách JSON hợp lệ')
            setconfig(db,key,val)
    for key in ('announcement_enabled','sticky_header'):setconfig(db,key,'true' if key in f else 'false')
    for k,v in previous.items():
        if v!=config(db,k):audit(db,user,'update_config','setting',k,'Cấu hình nhạy cảm thay đổi; không ghi giá trị tài khoản vào nhật ký')
    audit(db,user,'save_settings','settings')
    db.commit()
    return RedirectResponse('/quan-tri/cai-dat?success=1',303)

@router.post('/quan-tri/mo-ban')
async def toggle_store(request:Request,db:Session=Depends(get_db)):
    user,s=require(db,request,('owner',));f=await request.form();csrf_form(f,s)
    enable=tobool(f.get('enabled'))
    if enable:
        missing=[]
        for key,label in [('brand_logo','logo gốc'),('phone','số điện thoại'),('email','email'),('address','địa chỉ liên hệ'),('shipping_flat','phí vận chuyển'),('qr_bank','ngân hàng QR'),('qr_holder','tên chủ tài khoản'),('qr_account','số tài khoản'),('qr_media','ảnh QR')]:
            if not config(db,key):missing.append(label)
        for slug in ('giao-hang','doi-tra','bao-mat'):
            p=db.scalar(select(Page).where(Page.slug==slug,Page.published==True))
            if not p:missing.append('chính sách '+slug)
        ps=getattr(__import__('app.main',fromlist=['get_products']),'get_products')(db)
        if not any(p['image'] and p['price']>=0 for p in ps):missing.append('ít nhất một túi có ảnh, giá, biến thể')
        if missing:raise HTTPException(422,'Chưa thể mở bán, thiếu: '+', '.join(missing))
    setconfig(db,'store_open','true' if enable else 'false')
    audit(db,user,'toggle_store','store',detail='open' if enable else 'closed');db.commit()
    return RedirectResponse('/quan-tri/cai-dat',303)

@router.get('/quan-tri/tep')
def media_page(request:Request,db:Session=Depends(get_db)):
    return admin_view(request,db,'media.html',roles=('owner','content'),media=db.scalars(select(Media).order_by(Media.created_at.desc())).all())

@router.post('/api/admin/media')
async def upload_media(request:Request,file:UploadFile=File(...),folder:str=Form(''),alt:str=Form(''),db:Session=Depends(get_db)):
    user,s=require(db,request,('owner','content'),csrf=True)
    suffix=Path(file.filename or '').suffix.lower()
    typ={'jpg':'image/jpeg','jpeg':'image/jpeg','png':'image/png','webp':'image/webp','gif':'image/gif','mp4':'video/mp4','webm':'video/webm'}.get(suffix.removeprefix('.'))
    if not typ:raise HTTPException(422,'Chỉ nhận JPG, PNG, WEBP, GIF, MP4, WEBM')
    max_bytes=250*1024*1024 if typ.startswith('video/') else 20*1024*1024
    from .main import MEDIA_DIR
    stored=secrets.token_hex(16)+('.jpg' if suffix=='.jpeg' else suffix)
    path=MEDIA_DIR/stored;size=0
    try:
        with path.open('xb') as f:
            while True:
                chunk=await file.read(1024*1024)
                if not chunk:break
                size+=len(chunk)
                if size>max_bytes:raise ValueError('Tệp vượt dung lượng cho phép')
                f.write(chunk)
        width=height=None
        if typ.startswith('image/'):
            with Image.open(path) as im:
                im.verify()
            with Image.open(path) as im:
                width,height=im.size
                if width*height>80000000:raise ValueError('Ảnh có kích thước vượt giới hạn')
        elif suffix=='.mp4':
            with path.open('rb') as f: hdr=f.read(32)
            if b'ftyp' not in hdr[:16]:raise ValueError('MP4 không hợp lệ')
        elif suffix=='.webm':
            with path.open('rb') as f: hdr=f.read(4)
            if hdr!=b'\x1a\x45\xdf\xa3':raise ValueError('WEBM không hợp lệ')
        row=Media(file_name=Path(file.filename or 'media').name[:250],stored_name=stored,mime=typ,size=size,width=width,height=height,folder=folder[:100],alt=alt[:500]);db.add(row)
        db.flush();audit(db,user,'upload_media','media',row.id);db.commit()
    except Exception as e:
        path.unlink(missing_ok=True)
        if isinstance(e,(ValueError,UnidentifiedImageError)):raise HTTPException(422,str(e))
        raise
    return {'id':row.id,'url':'/media/'+stored,'file_name':row.file_name,'mime':typ,'size':size}

@router.post('/api/admin/media/{id}/delete')
def delete_media(id:int,request:Request,db:Session=Depends(get_db)):
    user,s=require(db,request,('owner','content'),csrf=True)
    m=db.get(Media,id)
    if not m:raise HTTPException(404)
    # Tránh xóa tài nguyên đang tham chiếu.
    referenced=[]
    if db.scalar(select(Product).where(Product.images.like('%'+str(id)+'%'))):referenced.append('sản phẩm')
    if db.scalar(select(Product).where(Product.video_id==id)):referenced.append('video sản phẩm')
    if db.scalar(select(Variant).where(Variant.image_id==id)):referenced.append('biến thể')
    if db.scalar(select(Category).where(Category.image_id==id)):referenced.append('danh mục')
    if db.scalar(select(Collection).where(Collection.image_id==id)):referenced.append('bộ sưu tập')
    if db.scalar(select(Post).where(Post.cover_id==id)):referenced.append('bài viết')
    if db.scalar(select(Page).where(or_(Page.draft.like('%/media/'+m.stored_name+'%'),Page.live.like('%/media/'+m.stored_name+'%')))):referenced.append('trang')
    if db.scalar(select(Post).where(or_(Post.draft.like('%/media/'+m.stored_name+'%'),Post.live.like('%/media/'+m.stored_name+'%')))):referenced.append('nội dung bài')
    if db.scalar(select(Order).where(Order.payment_snapshot.like('%/media/'+m.stored_name+'%'))):referenced.append('QR lưu cùng đơn hàng')
    for k in ('brand_logo','hero_image','hero_mobile','gift_image','brand_video','brand_video_poster','qr_media'):
        if config(db,k)==str(id):referenced.append('cấu hình '+k)
    if referenced:raise HTTPException(409,'Tệp đang được sử dụng: '+', '.join(referenced))
    from .main import MEDIA_DIR
    (MEDIA_DIR/m.stored_name).unlink(missing_ok=True)
    db.delete(m);audit(db,user,'delete_media','media',id);db.commit()
    return {'ok':True}

KINDS={'san-pham':Product,'danh-muc':Category,'bo-suu-tap':Collection,'bai-viet':Post,'trang':Page,'uu-dai':Promotion}
DISPLAY={'san-pham':'Sản phẩm','danh-muc':'Danh mục','bo-suu-tap':'Bộ sưu tập','bai-viet':'Bài viết','trang':'Trang','uu-dai':'Ưu đãi'}

@router.get('/quan-tri/noi-dung/{kind}')
def cms_list(request:Request,kind:str,db:Session=Depends(get_db)):
    if kind not in KINDS:raise HTTPException(404)
    stmt=select(KINDS[kind])
    if kind=='bai-viet':stmt=stmt.where(Post.deleted==False)
    return admin_view(request,db,'list.html',roles=('owner','content'),kind=kind,label=DISPLAY[kind],items=db.scalars(stmt.order_by(KINDS[kind].id.desc())).all())

@router.get('/quan-tri/noi-dung/{kind}/moi')
def cms_new(request:Request,kind:str,db:Session=Depends(get_db)):
    return cms_edit(request,kind,0,db)

@router.get('/quan-tri/noi-dung/{kind}/{id}')
def cms_edit(request:Request,kind:str,id:int,db:Session=Depends(get_db)):
    if kind not in KINDS:raise HTTPException(404)
    row=db.get(KINDS[kind],id) if id else None
    if id and not row:raise HTTPException(404)
    variants=db.scalars(select(Variant).where(Variant.product_id==id)).all() if kind=='san-pham' else []
    p_cats=[x.category_id for x in db.scalars(select(ProductCategory).where(ProductCategory.product_id==id)).all()] if kind=='san-pham' else []
    p_collections=[x.collection_id for x in db.scalars(select(CollectionProduct).where(CollectionProduct.product_id==id)).all()] if kind=='san-pham' else []
    return admin_view(request,db,'edit.html',roles=('owner','content'),kind=kind,label=DISPLAY[kind],item=row,variants=variants,p_cats=p_cats,p_collections=p_collections,categories=db.scalars(select(Category)).all(),collections=db.scalars(select(Collection)).all(),media=db.scalars(select(Media).order_by(Media.created_at.desc())).all())

@router.post('/quan-tri/noi-dung/{kind}/{id}')
async def cms_save(request:Request,kind:str,id:int,db:Session=Depends(get_db)):
    user,s=require(db,request,('owner','content'))
    f=await request.form();csrf_form(f,s)
    if kind not in KINDS:raise HTTPException(404)
    model=KINDS[kind]
    item=db.get(model,id) if id else None
    if id and not item:raise HTTPException(404)
    if not item:item=model()
    old_slug=item.slug if id and hasattr(item,'slug') else ''
    if kind=='san-pham':
        name=str(f.get('name','')).strip()[:200];sku=str(f.get('sku','')).strip()[:100]
        if len(name)<2 or not sku:raise HTTPException(422,'Tên và SKU bắt buộc')
        slug=slugify(f.get('slug') or name);slug_unique(db,model,slug,id)
        duplicate=db.scalar(select(Product).where(Product.sku==sku))
        if duplicate and duplicate.id!=id:raise HTTPException(422,'Mã sản phẩm đã tồn tại')
        item.name=name;item.sku=sku;item.slug=slug
        for key in ('summary','description','seo_title','seo_description'):setattr(item,key,str(f.get(key,''))[:10000])
        for key in ('specs','styles','uses','occasions','receivers','images'):
            if key=='specs':
                fields=('material','lining','closure','strap','dimensions','weight','accessories','care')
                setattr(item,key,jdumps({k:str(f.get('spec_'+k,''))[:400] for k in fields if f.get('spec_'+k)}))
            elif key=='images':setattr(item,key,jdumps([mid for mid in normalize_idlist(f.get('images','')) if db.get(Media,mid) and db.get(Media,mid).mime.startswith('image/')]))
            else:setattr(item,key,jdumps([x.strip() for x in str(f.get(key,'')).split(',') if x.strip()][:30]))
        item.published=tobool(f.get('published'));item.featured=tobool(f.get('featured'))
        vid=str(f.get('video_id',''));item.video_id=int(vid) if vid.isdigit() and db.get(Media,int(vid)) and db.get(Media,int(vid)).mime.startswith('video/') else None
        db.add(item);db.flush()
        db.query(ProductCategory).filter_by(product_id=item.id).delete()
        db.query(CollectionProduct).filter_by(product_id=item.id).delete()
        for cid in normalize_idlist(f.get('categories','')):
            if db.get(Category,cid):db.add(ProductCategory(product_id=item.id,category_id=cid))
        for pos,cid in enumerate(normalize_idlist(f.get('collections',''))):
            if db.get(Collection,cid):db.add(CollectionProduct(product_id=item.id,collection_id=cid,position=pos))
    elif kind in ('danh-muc','bo-suu-tap'):
        item.name=str(f.get('name','')).strip()[:180]
        if not item.name:raise HTTPException(422,'Thiếu tên')
        item.slug=slugify(f.get('slug') or item.name);slug_unique(db,model,item.slug,id)
        item.description=str(f.get('description',''))[:3000];item.active=tobool(f.get('active'))
        mid=str(f.get('image_id',''));item.image_id=int(mid) if mid.isdigit() and db.get(Media,int(mid)) else None
    elif kind in ('bai-viet','trang'):
        item.title=str(f.get('title','')).strip()[:220] if kind=='bai-viet' else None
        if kind=='trang':item.name=str(f.get('name','')).strip()[:200]
        name=item.title if kind=='bai-viet' else item.name
        if not name:raise HTTPException(422,'Tên/tiêu đề bắt buộc')
        item.slug=slugify(f.get('slug') or name);slug_unique(db,model,item.slug,id)
        if kind=='bai-viet':
            item.summary=str(f.get('summary',''))[:500];item.tags=str(f.get('tags',''))[:500]
            mid=str(f.get('cover_id',''));item.cover_id=int(mid) if mid.isdigit() and db.get(Media,int(mid)) else None
            schedule=str(f.get('publish_at','')).strip()
            try:item.publish_at=datetime.fromisoformat(schedule) if schedule else None
            except ValueError:raise HTTPException(422,'Lịch đăng không hợp lệ')
        item.seo_title=str(f.get('seo_title',''))[:200];item.seo_description=str(f.get('seo_description',''))[:180]
        # Xuất bản nội dung chỉ qua endpoint publish của builder: không bỏ qua kiểm tra.
        if not id:
            item.draft=layout(section([b('heading',text=name),b('text',text='Nhấp Thiết kế để soạn nội dung.')]));item.live='{"sections":[]}';item.published=False
            if kind=='trang':item.kind='page'
    elif kind=='uu-dai':
        item.code=str(f.get('code','')).strip().upper()[:80]
        if not item.code:raise HTTPException(422,'Mã ưu đãi bắt buộc')
        dupe=db.scalar(select(Promotion).where(Promotion.code==item.code))
        if dupe and dupe.id!=id:raise HTTPException(422,'Mã đã tồn tại')
        item.label=str(f.get('label',''))[:200];item.percent=int(f.get('percent',0))
        if not 1<=item.percent<=90:raise HTTPException(422,'Mức giảm phải trong khoảng 1–90%')
        for key in ('starts_at','ends_at'):
            val=str(f.get(key,'')).strip()
            try:setattr(item,key,datetime.fromisoformat(val) if val else None)
            except ValueError:raise HTTPException(422,'Ngày áp dụng không đúng định dạng')
        item.active=tobool(f.get('active'));item.automatic=tobool(f.get('automatic'))
        if item.automatic:
            for p in db.scalars(select(Promotion).where(Promotion.automatic==True,Promotion.id!=id)).all():p.automatic=False
    db.add(item);db.flush()
    if old_slug and hasattr(item,'slug') and old_slug!=item.slug:
        bases={'san-pham':'/san-pham/','danh-muc':'/danh-muc/','bo-suu-tap':'/bo-suu-tap/','bai-viet':'/bai-viet/','trang':'/'}
        if kind in bases:
            source=bases[kind]+old_slug;dest=bases[kind]+item.slug
            old=db.scalar(select(Redirect).where(Redirect.source==source))
            if old:old.destination=dest
            else:db.add(Redirect(source=source,destination=dest))
    audit(db,user,'save_'+kind,kind,item.id);db.commit()
    return RedirectResponse(f'/quan-tri/noi-dung/{kind}/{item.id}?saved=1',303)

@router.post('/quan-tri/noi-dung/{kind}/{id}/xoa')
async def cms_delete(request:Request,kind:str,id:int,db:Session=Depends(get_db)):
    user,s=require(db,request,('owner','content'));f=await request.form();csrf_form(f,s)
    if kind not in KINDS:raise HTTPException(404)
    obj=db.get(KINDS[kind],id)
    if not obj:raise HTTPException(404)
    if kind=='san-pham':
        if db.scalar(select(OrderItem).where(OrderItem.product_id==id)):obj.published=False
        else:
            for v in db.scalars(select(Variant).where(Variant.product_id==id)).all():db.delete(v)
            db.query(ProductCategory).filter_by(product_id=id).delete();db.query(CollectionProduct).filter_by(product_id=id).delete();db.delete(obj)
    elif kind=='bai-viet':obj.deleted=True;obj.published=False
    elif kind=='trang' and obj.slug in ('trang-chu','ve-chamea','lien-he'):raise HTTPException(409,'Trang lõi chỉ có thể chỉnh sửa')
    else:db.delete(obj)
    audit(db,user,'delete_'+kind,kind,id);db.commit()
    return RedirectResponse(f'/quan-tri/noi-dung/{kind}',303)

@router.get('/quan-tri/bien-the/{product_id}')
def variants_page(request:Request,product_id:int,db:Session=Depends(get_db)):
    p=db.get(Product,product_id)
    if not p:raise HTTPException(404)
    return admin_view(request,db,'variants.html',roles=('owner','content'),product=p,variants=db.scalars(select(Variant).where(Variant.product_id==product_id)).all(),media=db.scalars(select(Media)).all())

@router.post('/quan-tri/bien-the/{product_id}')
async def save_variant(request:Request,product_id:int,db:Session=Depends(get_db)):
    user,s=require(db,request,('owner','content'));f=await request.form();csrf_form(f,s)
    if not db.get(Product,product_id):raise HTTPException(404)
    id=int(f.get('id') or 0)
    v=db.get(Variant,id) if id else None
    if id and (not v or v.product_id!=product_id):raise HTTPException(404)
    name=str(f.get('name','')).strip()[:160];sku=str(f.get('sku','')).strip()[:100];price=int(f.get('price') or -1)
    if not name or not sku or price<0 or price>1000000000:raise HTTPException(422,'Tên, SKU và giá VNĐ phải hợp lệ')
    dupe=db.scalar(select(Variant).where(Variant.sku==sku))
    if dupe and dupe.id!=id:raise HTTPException(422,'SKU biến thể đã tồn tại')
    stocktxt=str(f.get('stock','')).strip()
    stock=int(stocktxt) if stocktxt else None
    if stock is not None and not 0<=stock<=1000000:raise HTTPException(422,'Tồn kho không hợp lệ')
    if not v:v=Variant(product_id=product_id);db.add(v)
    v.name=name;v.sku=sku;v.price=price;v.stock=stock;v.active=tobool(f.get('active'))
    mid=str(f.get('image_id',''));v.image_id=int(mid) if mid.isdigit() and db.get(Media,int(mid)) and db.get(Media,int(mid)).mime.startswith('image/') else None
    db.flush();audit(db,user,'save_variant','variant',v.id);db.commit()
    return RedirectResponse('/quan-tri/bien-the/'+str(product_id),303)

@router.get('/quan-tri/xem-truoc/{kind}/{id}')
def draft_preview(request:Request,kind:str,id:int,db:Session=Depends(get_db)):
    require(db,request,('owner','content'))
    if kind not in ('trang','bai-viet'):raise HTTPException(404)
    obj=db.get(KINDS[kind],id)
    if not obj:raise HTTPException(404)
    from .main import render,cms_data
    return render(request,db,'content.html',page=obj,layout=jloads(obj.draft),data=cms_data(db),page_title='XEM TRƯỚC · '+(obj.name if kind=='trang' else obj.title),noindex=True)

@router.get('/quan-tri/thiet-ke/{kind}/{id}')
def builder_page(request:Request,kind:str,id:int,db:Session=Depends(get_db)):
    if kind not in ('trang','bai-viet'):raise HTTPException(404)
    obj=db.get(KINDS[kind],id)
    if not obj:raise HTTPException(404)
    return admin_view(request,db,'builder.html',roles=('owner','content'),item=obj,kind=kind,media=db.scalars(select(Media).order_by(Media.created_at.desc())).all())

@router.get('/api/admin/layout/{kind}/{id}')
def get_layout(request:Request,kind:str,id:int,db:Session=Depends(get_db)):
    require(db,request,('owner','content'))
    if kind not in ('trang','bai-viet'):raise HTTPException(404)
    obj=db.get(KINDS[kind],id)
    if not obj:raise HTTPException(404)
    return {'layout':jloads(obj.draft),'version':obj.draft_version,'published':obj.published,'title':obj.name if kind=='trang' else obj.title}

@router.put('/api/admin/layout/{kind}/{id}')
async def save_layout(request:Request,kind:str,id:int,db:Session=Depends(get_db)):
    user,s=require(db,request,('owner','content'),csrf=True)
    if kind not in ('trang','bai-viet'):raise HTTPException(404)
    obj=db.get(KINDS[kind],id)
    if not obj:raise HTTPException(404)
    body=await request.json()
    if int(body.get('version',-1))!=obj.draft_version:raise HTTPException(409,'Dữ liệu đã thay đổi ở phiên khác. Tải lại trước khi ghi.')
    try:data=validate_layout(body.get('layout'))
    except (ValueError,TypeError) as e:raise HTTPException(422,str(e))
    db.add(Revision(entity_type=kind,entity_id=id,version=obj.draft_version,layout=obj.draft,actor_id=user.id))
    obj.draft=jdumps(data);obj.draft_version+=1;obj.updated_at=now() if hasattr(obj,'updated_at') else None
    audit(db,user,'save_draft',kind,id,'v'+str(obj.draft_version));db.commit()
    return {'ok':True,'version':obj.draft_version}

@router.post('/api/admin/layout/{kind}/{id}/publish')
def publish_layout(request:Request,kind:str,id:int,db:Session=Depends(get_db)):
    user,s=require(db,request,('owner','content'),csrf=True)
    if kind not in ('trang','bai-viet'):raise HTTPException(404)
    obj=db.get(KINDS[kind],id)
    if not obj:raise HTTPException(404)
    try:validate_layout(jloads(obj.draft))
    except ValueError as e:raise HTTPException(422,str(e))
    obj.live=obj.draft;obj.published=True
    audit(db,user,'publish',kind,id);db.commit()
    return {'ok':True}

@router.post('/api/admin/layout/{kind}/{id}/unpublish')
def unpublish(request:Request,kind:str,id:int,db:Session=Depends(get_db)):
    user,s=require(db,request,('owner','content'),csrf=True)
    if kind not in ('trang','bai-viet'):raise HTTPException(404)
    obj=db.get(KINDS[kind],id)
    if not obj:raise HTTPException(404)
    if kind=='trang' and obj.slug=='trang-chu':raise HTTPException(409,'Không thể gỡ trang chủ')
    obj.published=False;audit(db,user,'unpublish',kind,id);db.commit()
    return {'ok':True}

@router.get('/api/admin/layout/{kind}/{id}/revisions')
def get_revisions(request:Request,kind:str,id:int,db:Session=Depends(get_db)):
    require(db,request,('owner','content'))
    rows=db.scalars(select(Revision).where(Revision.entity_type==kind,Revision.entity_id==id).order_by(Revision.id.desc()).limit(30)).all()
    return [{'id':r.id,'version':r.version,'date':str(r.created_at)} for r in rows]

@router.post('/api/admin/layout/{kind}/{id}/restore/{rev}')
def restore(request:Request,kind:str,id:int,rev:int,db:Session=Depends(get_db)):
    user,s=require(db,request,('owner','content'),csrf=True)
    if kind not in ('trang','bai-viet'):raise HTTPException(404)
    obj=db.get(KINDS[kind],id);r=db.get(Revision,rev)
    if not obj or not r or r.entity_type!=kind or r.entity_id!=id:raise HTTPException(404)
    db.add(Revision(entity_type=kind,entity_id=id,version=obj.draft_version,layout=obj.draft,actor_id=user.id))
    obj.draft=r.layout;obj.draft_version+=1;audit(db,user,'restore_draft',kind,id,'revision '+str(rev));db.commit()
    return {'ok':True,'version':obj.draft_version,'layout':jloads(obj.draft)}

@router.post('/api/admin/presets')
async def save_preset(request:Request,db:Session=Depends(get_db)):
    user,s=require(db,request,('owner','content'),csrf=True);body=await request.json()
    name=str(body.get('name','')).strip()[:180]
    if not name:raise HTTPException(422,'Tên mẫu không được trống')
    try:data=validate_layout(body.get('layout'))
    except ValueError as e:raise HTTPException(422,str(e))
    existing=db.scalar(select(LayoutPreset).where(LayoutPreset.name==name))
    if existing:existing.layout=jdumps(data)
    else:db.add(LayoutPreset(name=name,layout=jdumps(data)))
    db.commit();return {'ok':True}

@router.get('/api/admin/presets')
def list_presets(request:Request,db:Session=Depends(get_db)):
    require(db,request,('owner','content'))
    return [{'name':x.name,'layout':jloads(x.layout)} for x in db.scalars(select(LayoutPreset)).all()]

@router.get('/quan-tri/nguoi-dung')
def users_page(request:Request,db:Session=Depends(get_db)):
    return admin_view(request,db,'users.html',roles=('owner',),users=db.scalars(select(User)).all())

@router.post('/quan-tri/nguoi-dung')
async def users_save(request:Request,db:Session=Depends(get_db)):
    owner,s=require(db,request,('owner',));f=await request.form();csrf_form(f,s)
    email=str(f.get('email','')).strip().lower()[:200];role=str(f.get('role',''))
    passwd=str(f.get('password',''))
    if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email) or role not in ('owner','content','orders') or len(passwd)<12:raise HTTPException(422,'Email, quyền hoặc mật khẩu không hợp lệ')
    if db.scalar(select(User).where(User.email==email)):raise HTTPException(409,'Email đã tồn tại')
    obj=User(email=email,password_hash=hash_password(passwd),role=role);db.add(obj);db.flush()
    audit(db,owner,'create_user','user',obj.id,'role='+role);db.commit()
    return RedirectResponse('/quan-tri/nguoi-dung',303)

@router.post('/quan-tri/nguoi-dung/{id}/status')
async def user_status(request:Request,id:int,db:Session=Depends(get_db)):
    owner,s=require(db,request,('owner',));form=await request.form();csrf_form(form,s)
    user=db.get(User,id)
    if not user:raise HTTPException(404)
    if owner.id==id:raise HTTPException(409,'Không thể tự vô hiệu hóa tài khoản đang dùng')
    enabled=tobool(form.get('active'))
    if not enabled and user.role=='owner':
        total=db.scalar(select(func.count()).select_from(User).where(User.role=='owner',User.active==True))
        if total<=1:raise HTTPException(409,'Cần giữ ít nhất một chủ website đang hoạt động')
    user.active=enabled
    for sess in db.scalars(select(LoginSession).where(LoginSession.user_id==id)).all():db.delete(sess)
    audit(db,owner,'change_user_status','user',id,str(enabled));db.commit()
    return RedirectResponse('/quan-tri/nguoi-dung',303)

@router.post('/quan-tri/nguoi-dung/{id}/password')
async def user_password(request:Request,id:int,db:Session=Depends(get_db)):
    owner,s=require(db,request,('owner',));form=await request.form();csrf_form(form,s)
    user=db.get(User,id)
    if not user:raise HTTPException(404)
    password=str(form.get('password',''))
    if len(password)<12:raise HTTPException(422,'Mật khẩu phải có tối thiểu 12 ký tự')
    user.password_hash=hash_password(password)
    for sess in db.scalars(select(LoginSession).where(LoginSession.user_id==id)).all():db.delete(sess)
    audit(db,owner,'reset_user_password','user',id);db.commit()
    return RedirectResponse('/quan-tri/nguoi-dung',303)
