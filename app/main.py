import os, re, io, secrets, json, hashlib, time, mimetypes
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from urllib.parse import quote as uri_quote
from fastapi import FastAPI, Request, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy import select, func, or_, desc, update
from sqlalchemy.orm import Session
from PIL import Image, UnidentifiedImageError
from .db import get_db, SessionLocal, ROOT
from .models import *
from .core import *
from .seed import initialize

@asynccontextmanager
async def lifespan(app):
    initialize()
    yield

app=FastAPI(title='CHAMÉA',docs_url=None,redoc_url=None,openapi_url=None,lifespan=lifespan)
app.mount('/static',StaticFiles(directory=str(ROOT/'app'/'static')),name='static')
MEDIA_DIR=Path(os.getenv('MEDIA_DIR',str(ROOT/'data'/'media')))
MEDIA_DIR.mkdir(parents=True,exist_ok=True)
views=Jinja2Templates(directory=str(ROOT/'app'/'templates'))
views.env.globals.update(money=money,jloads=jloads,href=safe_href,safe_style=safe_style)

@app.middleware('http')
async def slug_redirects(request, call_next):
    if request.method=='GET' and not request.url.path.startswith(('/media/','/static/','/api/','/quan-tri/')):
        with SessionLocal() as db:
            target=db.scalar(select(Redirect).where(Redirect.source==request.url.path))
            if target:return RedirectResponse(target.destination,status_code=301)
    return await call_next(request)

@app.middleware('http')
async def security_headers(request, call_next):
    response=await call_next(request)
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Referrer-Policy']='strict-origin-when-cross-origin'
    response.headers['X-Frame-Options']='SAMEORIGIN'
    response.headers['Permissions-Policy']='camera=(), microphone=(), geolocation=()'
    response.headers['Content-Security-Policy']="default-src 'self'; img-src 'self' data:; font-src 'self' https://fonts.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; script-src 'self'; connect-src 'self'; frame-ancestors 'self'; object-src 'none'; base-uri 'self'; form-action 'self'"
    if request.url.path.startswith('/quan-tri') or request.url.path.startswith('/api/admin') or request.url.path.startswith('/dat-hang/'):
        response.headers['Cache-Control']='no-store'
        response.headers['X-Robots-Tag']='noindex, nofollow'
    return response

# Giới hạn cơ bản theo IP; khi triển khai nhiều worker cần Redis/nginx rate limiting.
requests_map=defaultdict(deque)
def throttle(request, action, count=15, seconds=60):
    key=(request.client.host if request.client else 'unknown',action)
    nowt=time.monotonic(); q=requests_map[key]
    while q and q[0]<nowt-seconds:q.popleft()
    if len(q)>=count:raise HTTPException(429,'Thao tác quá nhanh. Vui lòng thử lại sau.')
    q.append(nowt)

@app.get('/media/{file_name}')
def serve_media(file_name:str,db:Session=Depends(get_db)):
    if not re.fullmatch(r'[0-9a-f]{32}\.(jpg|png|webp|gif|mp4|webm)',file_name):raise HTTPException(404)
    obj=db.scalar(select(Media).where(Media.stored_name==file_name))
    if not obj:raise HTTPException(404)
    path=MEDIA_DIR/file_name
    if not path.is_file():raise HTTPException(404)
    return FileResponse(path,media_type=obj.mime,headers={'X-Content-Type-Options':'nosniff','Cache-Control':'public, max-age=604800'})

def common(request,db, **extra):
    site={key:config(db,key) for key in ('announcement','announcement_enabled','sticky_header','brand_logo','hero_image','hero_mobile','gift_image','brand_video','brand_video_poster','phone','email','address','facebook','instagram','seo_title','seo_description','theme_primary','theme_accent','theme_bg','store_open')}
    categories=db.scalars(select(Category).where(Category.active==True)).all()
    menus=jloads(config(db,'menu','[]'),[])
    if not menus: menus=[{'text':t,'url':u} for t,u in [('TRANG CHỦ','/'),('TÚI XÁCH','/san-pham'),('BỘ SƯU TẬP','/bo-suu-tap'),('GỢI Ý CHỌN QUÀ','/goi-y-chon-qua'),('VỀ CHAMÉA','/ve-chamea'),('LIÊN HỆ','/lien-he')]]
    base={'request':request,'site':site,'menus':menus,'categories':categories,'media_url':lambda m:media_url(db,m),'page_title':site['seo_title'],'meta_description':site['seo_description'],'canonical':str(request.url).split('?')[0],'noindex':False,'csrf':'','user':None}
    base.update(extra)
    return base

def render(request,db,filename,**extra): return views.TemplateResponse(request,filename,common(request,db,**extra))

def get_products(db,category=None,collection=None,q='',sort='',minp=None,maxp=None):
    stmt=select(Product).where(Product.published==True)
    if category:stmt=stmt.join(ProductCategory).where(ProductCategory.category_id==category)
    if collection:stmt=stmt.join(CollectionProduct).where(CollectionProduct.collection_id==collection)
    if q:
        qn=slugify(q)
        stmt=stmt.where(or_(Product.name.ilike('%'+q+'%'),Product.sku.ilike('%'+q+'%'),Product.slug.ilike('%'+qn+'%'),Product.summary.ilike('%'+q+'%')))
    ps=list(db.scalars(stmt.distinct()).all())
    out=[]
    for p in ps:
        variants=db.scalars(select(Variant).where(Variant.product_id==p.id,Variant.active==True)).all()
        if not variants:continue
        original_price=min(x.price for x in variants)
        promo=active_promotion(db)
        price=original_price-(original_price*promo.percent//100) if promo else original_price
        if minp is not None and price<minp:continue
        if maxp is not None and price>maxp:continue
        imgs=jloads(p.images,[])
        out.append({'item':p,'price':price,'original_price':original_price,'discount_percent':promo.percent if promo else 0,'image':media_url(db,imgs[0]) if imgs else '', 'variants':variants})
    if sort=='price_asc':out.sort(key=lambda v:v['price'])
    elif sort=='price_desc':out.sort(key=lambda v:-v['price'])
    else:out.sort(key=lambda v:v['item'].created_at,reverse=True)
    return out

def page_content(db, slug, draft=False):
    p=db.scalar(select(Page).where(Page.slug==slug))
    if not p or (not p.published and not draft):return None
    return p

def cms_data(db):
    return {'products':get_products(db)[:8], 'categories':db.scalars(select(Category).where(Category.active==True)).all(), 'collections':db.scalars(select(Collection).where(Collection.active==True)).all(), 'articles':db.scalars(select(Post).where(Post.published==True,Post.deleted==False).order_by(Post.created_at.desc()).limit(6)).all(),'media_url':lambda mid:media_url(db,mid)}

@app.get('/')
def home(request:Request,db:Session=Depends(get_db)):
    p=page_content(db,'trang-chu')
    return render(request,db,'content.html',page=p,layout=jloads(p.live,{'sections':[]}) if p else {'sections':[]},data=cms_data(db))

@app.get('/san-pham')
def catalog(request:Request,db:Session=Depends(get_db),q:str='',sort:str='',min_price:int|None=None,max_price:int|None=None,page:int=1):
    products=get_products(db,q=q.strip()[:100],sort=sort,minp=min_price,maxp=max_price)
    page=max(1,page)
    return render(request,db,'catalog.html',products=products[(page-1)*12:page*12],total=len(products),current_page=page,pages=max(1,(len(products)+11)//12),q=q,sort=sort,heading='Tất cả túi xách',query_params=f'q={uri_quote(q)}&sort={uri_quote(sort)}',min_price=min_price,max_price=max_price)

@app.get('/tim-kiem')
def search(request:Request,db:Session=Depends(get_db),q:str=''):
    return catalog(request,db,q=q)

@app.get('/danh-muc/{slug}')
def category(request:Request,slug:str,db:Session=Depends(get_db),sort:str='',page:int=1):
    cat=db.scalar(select(Category).where(Category.slug==slug,Category.active==True))
    if not cat:raise HTTPException(404)
    ps=get_products(db,category=cat.id,sort=sort)
    page=max(1,page)
    return render(request,db,'catalog.html',products=ps[(page-1)*12:page*12],total=len(ps),current_page=page,pages=max(1,(len(ps)+11)//12),q='',sort=sort,heading=cat.name,description=cat.description,query_params=f'sort={uri_quote(sort)}')

@app.get('/bo-suu-tap')
def collections_page(request:Request,db:Session=Depends(get_db)):
    rows=db.scalars(select(Collection).where(Collection.active==True)).all()
    return render(request,db,'collections.html',collections=rows)

@app.get('/bo-suu-tap/{slug}')
def collection_page(request:Request,slug:str,db:Session=Depends(get_db),sort:str='',page:int=1):
    item=db.scalar(select(Collection).where(Collection.slug==slug,Collection.active==True))
    if not item:raise HTTPException(404)
    ps=get_products(db,collection=item.id,sort=sort)
    page=max(1,page)
    return render(request,db,'catalog.html',products=ps[(page-1)*12:page*12],total=len(ps),current_page=page,pages=max(1,(len(ps)+11)//12),q='',sort=sort,heading=item.name,description=item.description,query_params=f'sort={uri_quote(sort)}')

@app.get('/san-pham/{slug}')
def product_page(request:Request,slug:str,db:Session=Depends(get_db)):
    p=db.scalar(select(Product).where(Product.slug==slug,Product.published==True))
    if not p:raise HTTPException(404)
    variants=db.scalars(select(Variant).where(Variant.product_id==p.id,Variant.active==True)).all()
    images=[media_url(db,x) for x in jloads(p.images,[]) if media_url(db,x)]
    return render(request,db,'product.html',product=p,variants=variants,images=images,specs=jloads(p.specs,{}),page_title=(p.seo_title or p.name)+' | CHAMÉA',meta_description=(p.seo_description or p.summary),related=get_products(db)[:4],selling=is_open(db),active_discount=(active_promotion(db).percent if active_promotion(db) else 0))

@app.get('/goc-chon-qua')
def articles(request:Request,db:Session=Depends(get_db)):
    posts=db.scalars(select(Post).where(Post.published==True,Post.deleted==False,or_(Post.publish_at==None,Post.publish_at<=datetime.now())).order_by(Post.created_at.desc())).all()
    return render(request,db,'posts.html',posts=posts)

@app.get('/bai-viet/{slug}')
def article(request:Request,slug:str,db:Session=Depends(get_db)):
    p=db.scalar(select(Post).where(Post.slug==slug,Post.published==True,Post.deleted==False,or_(Post.publish_at==None,Post.publish_at<=datetime.now())))
    if not p:raise HTTPException(404)
    return render(request,db,'content.html',page=p,layout=jloads(p.live),data=cms_data(db),page_title=(p.seo_title or p.title)+' | CHAMÉA',meta_description=p.seo_description or p.summary)

# API công khai: tuyệt đối tính tiền ở máy chủ.
@app.post('/api/cart/preview')
async def cart_preview(request:Request,db:Session=Depends(get_db)):
    body=await request.json()
    items=body.get('items',[])
    if not isinstance(items,list) or len(items)>50:raise HTTPException(422,'Giỏ hàng không hợp lệ')
    rows=[]
    for item in items:
        try:
            vid=int(item.get('variant_id',0));qty=int(item.get('quantity',0))
            if not 1<=qty<=20:continue
        except (TypeError,ValueError):continue
        v=db.get(Variant,vid)
        p=db.get(Product,v.product_id) if v else None
        if p and v and p.published and v.active:
            imgs=jloads(p.images,[])
            rows.append({'variant_id':v.id,'name':p.name,'variant':v.name,'price':v.price,'quantity':qty,'url':'/san-pham/'+p.slug,'image':media_url(db,v.image_id or (imgs[0] if imgs else None))})
    return {'items':rows}

@app.get('/api/favorites')
def favorites_api(ids:str='',db:Session=Depends(get_db)):
    try:nums=[int(v) for v in ids.split(',')[:40] if v.isdigit()]
    except ValueError:nums=[]
    ps=get_products(db)
    return [{'id':p['item'].id,'name':p['item'].name,'price':p['price'],'image':p['image'],'url':'/san-pham/'+p['item'].slug} for p in ps if p['item'].id in nums]

@app.post('/api/quote')
async def calculate(request:Request,db:Session=Depends(get_db)):
    throttle(request,'quote',40)
    body=await request.json()
    try:
        if not is_open(db):raise ValueError('Cửa hàng chưa mở nhận đơn')
        return quote(db,body.get('items',[]),body.get('coupon',''))
    except (ValueError,TypeError,OverflowError) as e:raise HTTPException(422,str(e))

@app.post('/api/orders')
async def checkout_order(request:Request,db:Session=Depends(get_db)):
    throttle(request,'order',8,300)
    body=await request.json()
    idem=str(body.get('idempotency_key',''))[:100]
    if len(idem)<20:raise HTTPException(422,'Thiếu khóa chống đặt trùng')
    existing=db.scalar(select(Order).where(Order.idem_hash==sha(idem)))
    if existing:return {'code':existing.code,'receipt':'/dat-hang/'+existing.receipt_token,'duplicate':True}
    if not is_open(db):raise HTTPException(409,'Cửa hàng chưa mở nhận đơn')
    method=body.get('method','')
    if method not in ('COD','QR'):raise HTTPException(422,'Chỉ nhận COD hoặc QR')
    if method=='QR' and not qr_ready(db):raise HTTPException(422,'QR chưa được cấu hình hợp lệ')
    name=str(body.get('name','')).strip()[:150]
    phone=str(body.get('phone','')).strip()[:35]
    address=str(body.get('address','')).strip()[:800]
    email=str(body.get('email','')).strip()[:200]
    if len(name)<2 or len(address)<10 or not re.fullmatch(r'[+\d][\d\s().-]{7,22}',phone):raise HTTPException(422,'Tên, số điện thoại hoặc địa chỉ chưa hợp lệ')
    if email and not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email):raise HTTPException(422,'Email chưa hợp lệ')
    try: pricing=quote(db,body.get('items',[]),body.get('coupon',''))
    except (ValueError,OverflowError,TypeError) as e:raise HTTPException(422,str(e))
    receipt=secrets.token_urlsafe(32)
    order=Order(code='CM'+datetime.now().strftime('%y%m%d')+'-'+secrets.token_hex(4).upper(),lookup_token_hash=sha(receipt),receipt_token=receipt,idem_hash=sha(idem),customer_name=name,phone=phone,email=email,address=address,note=str(body.get('note',''))[:1500],gift_message=str(body.get('gift_message',''))[:600],method=method,payment_snapshot=jdumps({'bank':config(db,'qr_bank'),'holder':config(db,'qr_holder'),'account':config(db,'qr_account'),'image':media_url(db,config(db,'qr_media'))}) if method=='QR' else '{}',payment_status='unpaid',subtotal=pricing['subtotal'],discount=pricing['discount'],shipping=pricing['shipping'],total=pricing['total'])
    # SQLite BEGIN IMMEDIATE khóa ghi sớm, giữ xử lý giá/tồn kho và ghi đơn trong một giao dịch.
    # Tích hợp hàng đợi/ngân hàng thật là nâng cấp độc lập, không mô phỏng.
    try:
        db.add(order);db.flush()
        for item in pricing['items']:
            db.add(OrderItem(order_id=order.id,product_id=item['product_id'],variant_id=item['variant_id'],product_name=item['name'],variant_name=item['variant'],sku=item['sku'],quantity=item['qty'],unit_price=item['price'],line_discount=item['discount']))
            variant=db.get(Variant,item['variant_id'])
            if variant.stock is not None:
                # Cập nhật có điều kiện ở DB, không check-then-write trên ORM.
                applied=db.execute(update(Variant).where(Variant.id==variant.id,Variant.stock>=item['qty']).values(stock=Variant.stock-item['qty']))
                if applied.rowcount!=1:raise ValueError('Tồn kho vừa thay đổi, vui lòng tải lại giỏ')
        db.flush();db.commit()
    except Exception as e:
        db.rollback()
        prev=db.scalar(select(Order).where(Order.idem_hash==sha(idem)))
        if prev:return {'code':prev.code,'receipt':'/dat-hang/'+prev.receipt_token,'duplicate':True}
        if isinstance(e,ValueError):raise HTTPException(409,str(e))
        raise HTTPException(503,'Không thể xác nhận đơn hàng. Vui lòng kiểm tra trạng thái trước khi thử lại.')
    return {'code':order.code,'receipt':'/dat-hang/'+receipt,'duplicate':False}

@app.get('/dat-hang/{token}')
def receipt_page(request:Request,token:str,db:Session=Depends(get_db)):
    if len(token)>100:raise HTTPException(404)
    order=db.scalar(select(Order).where(Order.lookup_token_hash==sha(token)))
    if not order:raise HTTPException(404)
    rows=db.scalars(select(OrderItem).where(OrderItem.order_id==order.id)).all()
    return render(request,db,'receipt.html',order=order,rows=rows,qr_config=jloads(order.payment_snapshot,{}),noindex=True)

@app.post('/api/orders/{token}/verify')
async def verify_request(request:Request,token:str,db:Session=Depends(get_db)):
    throttle(request,'verify',10,3600)
    order=db.scalar(select(Order).where(Order.lookup_token_hash==sha(token)))
    if not order or order.method!='QR':raise HTTPException(404)
    if order.payment_status=='paid':return {'ok':True,'message':'Đơn đã được xác nhận thanh toán'}
    order.payment_status='pending_verification'
    audit(db,None,'request_verify','order',order.id,'Yêu cầu đối soát từ khách; chưa xác nhận nhận tiền')
    db.commit()
    return {'ok':True,'message':'Đã ghi nhận yêu cầu đối soát. Đơn chưa được xác nhận thanh toán.'}

@app.post('/api/contact')
async def submit_contact(request:Request,db:Session=Depends(get_db)):
    throttle(request,'lead',4,300)
    body=await request.json()
    if body.get('website'):raise HTTPException(422,'Không hợp lệ')
    name=str(body.get('name','')).strip()[:150];phone=str(body.get('phone','')).strip()[:35];msg=str(body.get('message','')).strip()[:2000]
    if len(name)<2 or not re.fullmatch(r'[+\d][\d\s().-]{7,22}',phone) or len(msg)<5:raise HTTPException(422,'Vui lòng nhập đủ thông tin tư vấn')
    db.add(Lead(name=name,phone=phone,message=msg));db.commit()
    return {'ok':True}

@app.post('/api/newsletter')
async def subscribe(request:Request,db:Session=Depends(get_db)):
    throttle(request,'news',4,300)
    body=await request.json()
    email=str(body.get('email','')).strip().lower()[:200]
    if not body.get('consent') or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email):raise HTTPException(422,'Email hoặc đồng ý nhận tin chưa hợp lệ')
    existing=db.scalar(select(Newsletter).where(Newsletter.email==email))
    if existing:existing.consent=True
    else:db.add(Newsletter(email=email,unsubscribe_hash=sha(secrets.token_urlsafe(32)),consent=True))
    db.commit()
    return {'ok':True,'message':'Đã lưu đăng ký. Email thông báo chưa được cấu hình.'}

@app.post('/api/gift-recommendations')
async def recommend(request:Request,db:Session=Depends(get_db)):
    data=await request.json(); ps=get_products(db)
    style=str(data.get('style',''));use=str(data.get('use',''));occasion=str(data.get('occasion',''));receiver=str(data.get('receiver',''))
    budget=data.get('budget','')
    try:budget=int(budget) if budget else 0
    except: budget=0
    matches=[]
    for p in ps:
        obj=p['item'];st=jloads(obj.styles,[]); uses=jloads(obj.uses,[]);occs=jloads(obj.occasions,[]);receivers=jloads(obj.receivers,[])
        if style and style not in st:continue
        if use and use not in uses:continue
        if occasion and occasion not in occs:continue
        if receiver and receiver not in receivers:continue
        if budget and p['price']>budget:continue
        reasons=[]
        if style:reasons.append('hợp phong cách '+style)
        if use:reasons.append('phù hợp nhu cầu '+use)
        if budget:reasons.append('trong ngân sách bạn chọn')
        matches.append({'name':obj.name,'url':'/san-pham/'+obj.slug,'price':p['price'],'image':p['image'],'reason':', '.join(reasons) or 'Phù hợp với thuộc tính đã chọn'})
    return {'results':matches[:8],'total':len(matches)}

@app.get('/sitemap.xml')
def sitemap(request:Request,db:Session=Depends(get_db)):
    from xml.sax.saxutils import escape
    base=os.getenv('PUBLIC_BASE_URL',str(request.base_url).rstrip('/')).rstrip('/')
    paths=['/','/san-pham','/bo-suu-tap','/goc-chon-qua','/goi-y-chon-qua']
    paths+=['/san-pham/'+p.slug for p in db.scalars(select(Product).where(Product.published==True)).all()]
    paths+=['/bo-suu-tap/'+x.slug for x in db.scalars(select(Collection).where(Collection.active==True)).all()]
    paths+=['/danh-muc/'+x.slug for x in db.scalars(select(Category).where(Category.active==True)).all()]
    paths+=['/bai-viet/'+x.slug for x in db.scalars(select(Post).where(Post.published==True,Post.deleted==False)).all()]
    paths+=['/'+x.slug for x in db.scalars(select(Page).where(Page.published==True,Page.slug!='trang-chu')).all()]
    xml='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+escape(base+x)+'</loc></url>' for x in paths)+'</urlset>'
    return PlainTextResponse(xml,media_type='application/xml')

@app.exception_handler(403)
async def login_for_admin(request,exc):
    if request.method=='GET' and request.url.path.startswith('/quan-tri') and request.url.path!='/quan-tri/dang-nhap':
        return RedirectResponse('/quan-tri/dang-nhap',status_code=303)
    return JSONResponse({'detail':'Bạn không có quyền truy cập'},status_code=403)

@app.exception_handler(404)
async def custom_404(request,exc):
    with SessionLocal() as db: return views.TemplateResponse(request,'404.html',common(request,db,page_title='Không tìm thấy trang | CHAMÉA'),status_code=404)

# Các route /quan-tri và /api/admin đặt trong router riêng để không xung đột wildcard.
from .admin import router as admin_router
app.include_router(admin_router)

@app.get('/{page_slug}')
def static_pages(request:Request,page_slug:str,db:Session=Depends(get_db)):
    if page_slug in ['gio-hang','thanh-toan','yeu-thich','goi-y-chon-qua']:
        files={'gio-hang':'cart.html','thanh-toan':'checkout.html','yeu-thich':'favorites.html','goi-y-chon-qua':'quiz.html'}
        return render(request,db,files[page_slug],qr_ready=qr_ready(db),shipping=config(db,'shipping_flat'),store_open=is_open(db))
    if page_slug=='robots.txt':return PlainTextResponse('User-agent: *\nDisallow: /quan-tri/\nDisallow: /api/admin/\nDisallow: /dat-hang/\n')
    p=page_content(db,page_slug)
    if not p:raise HTTPException(404)
    return render(request,db,'content.html',page=p,layout=jloads(p.live),data=cms_data(db),page_title=p.seo_title or p.name+' | CHAMÉA',meta_description=p.seo_description or '')

