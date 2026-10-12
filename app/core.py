import os, re, json, hmac, hashlib, secrets, math, unicodedata
from datetime import datetime, timezone, timedelta
from urllib.parse import urlsplit
import bleach
from fastapi import HTTPException
from sqlalchemy import select
from .models import Config, Media, Variant, Product, Promotion, Order, OrderItem, Audit, LoginSession, User

PASSWORD_ITER = 470000
ALLOWED_TAGS = ['p','b','strong','i','em','u','br','ul','ol','li','blockquote','h2','h3','h4','a','table','thead','tbody','tr','th','td','figure','figcaption']
ALLOWED_ATTR = {'a':['href','title','rel'], 'th':['scope']}

def hash_password(raw):
    salt=secrets.token_bytes(16)
    dk=hashlib.pbkdf2_hmac('sha256',raw.encode(),salt,PASSWORD_ITER)
    return f'pbkdf2_sha256${PASSWORD_ITER}${salt.hex()}${dk.hex()}'

def verify_password(raw, stored):
    try:
        algo, it, salt, digest = stored.split('$')
        if algo != 'pbkdf2_sha256': return False
        check = hashlib.pbkdf2_hmac('sha256',raw.encode(),bytes.fromhex(salt),int(it))
        return hmac.compare_digest(check,bytes.fromhex(digest))
    except (ValueError,TypeError): return False

def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def jloads(s, fallback=None):
    try: return json.loads(s or '')
    except (ValueError,TypeError): return fallback if fallback is not None else {}
def jdumps(d): return json.dumps(d,ensure_ascii=False)

def slugify(s):
    s=s.replace('đ','d').replace('Đ','D')
    s=unicodedata.normalize('NFKD',s)
    s=''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:180]

def money(v): return f'{int(v):,}'.replace(',','.')+' ₫'

def config(db,key,default=''):
    v=db.get(Config,key)
    return v.value if v else default

def setconfig(db,key,value):
    row=db.get(Config,key)
    if row: row.value=str(value)
    else: db.add(Config(key=key,value=str(value)))

def audit(db, user, action, entity, eid='', detail=''):
    db.add(Audit(user_id=user.id if user else None,action=action,entity=entity,entity_id=str(eid),detail=str(detail)[:1500]))

def safe_href(url):
    if not isinstance(url,str): return '#'
    url=url.strip()[:500]
    if url.startswith('/') and not url.startswith('//'): return url
    if url.startswith('#'): return url
    if url.startswith(('https://','http://')): return url
    return '#'

def clean_html(html):
    html=bleach.clean(str(html or ''),tags=ALLOWED_TAGS,attributes=ALLOWED_ATTR,protocols=['http','https','mailto'],strip=True)
    return bleach.linkify(html,callbacks=[bleach.callbacks.nofollow])

BLOCK_TYPES={'heading','text','richtext','image','video','button','divider','spacer','hero','products','categories','collections','articles','giftquiz','consult','newsletter','faq','icontext','gallery','product','featured_article','cart','checkout','product_detail','gift_banner','brandvideo'}

def validate_layout(data):
    if not isinstance(data,dict) or not isinstance(data.get('sections'),list): raise ValueError('Dữ liệu bố cục không hợp lệ')
    if len(data['sections']) > 35: raise ValueError('Quá nhiều khu vực')
    total=0
    clean={'sections':[]}
    for sec in data['sections']:
        if not isinstance(sec,dict) or not isinstance(sec.get('rows'),list): raise ValueError('Khu vực không hợp lệ')
        cs={'id':str(sec.get('id') or secrets.token_hex(4))[:50], 'settings':sec.get('settings',{}) if isinstance(sec.get('settings'),dict) else {},'rows':[]}
        if len(sec['rows'])>25: raise ValueError('Quá nhiều hàng')
        for row in sec['rows']:
            cols=row.get('columns',[])
            if not isinstance(cols,list) or not 1<=len(cols)<=4: raise ValueError('Số cột phải từ 1 đến 4')
            cr={'id':str(row.get('id') or secrets.token_hex(4))[:50],'columns':[],'responsive':{k:v for k,v in (row.get('responsive') or {}).items() if k in ('mobile','tablet','desktop') and isinstance(v,dict)}}
            for col in cols:
                blocks=col.get('blocks',[])
                if not isinstance(blocks,list) or len(blocks)>35: raise ValueError('Dữ liệu khối không hợp lệ')
                cc={'id':str(col.get('id') or secrets.token_hex(4))[:50], 'span':max(1,min(12,int(col.get('span',12)))),'blocks':[],'responsive':{k:v for k,v in (col.get('responsive') or {}).items() if k in ('mobile','tablet','desktop') and isinstance(v,dict)}}
                for b in blocks:
                    total+=1
                    if total>300: raise ValueError('Trang vượt quá 300 khối')
                    typ=b.get('type')
                    if typ not in BLOCK_TYPES: raise ValueError(f'Loại khối không hỗ trợ: {typ}')
                    val=b.get('content',{})
                    sty=b.get('style',{})
                    responsive=b.get('responsive',{})
                    if not isinstance(val,dict) or not isinstance(sty,dict) or not isinstance(responsive,dict): raise ValueError('Thuộc tính khối không hợp lệ')
                    val={str(k)[:50]:str(v)[:10000] if not isinstance(v,(list,dict)) else v for k,v in val.items() if str(k)[:1]!='_'}
                    if 'images' in val:
                        if not isinstance(val['images'],list):val['images']=[]
                        else:val['images']=[{'src':x.get('src',''),'alt':str(x.get('alt',''))[:250]} for x in val['images'][:30] if isinstance(x,dict) and isinstance(x.get('src'),str) and x['src'].startswith('/media/')]
                    if 'html' in val: val['html']=clean_html(val['html'])
                    if 'href' in val: val['href']=safe_href(val['href'])
                    if 'src' in val and not (isinstance(val['src'],str) and (val['src'].startswith('/media/') or val['src']=='')): val['src']=''
                    if 'poster' in val and not (isinstance(val['poster'],str) and (val['poster'].startswith('/media/') or val['poster']=='')): val['poster']=''
                    permitted={'align','padding','margin','background','color','fontSize','radius','gap','height','width','fit','ratio','objectPosition','justify'}
                    sty={k: str(v)[:80] for k,v in sty.items() if k in permitted and isinstance(v,(str,int,float))}
                    cc['blocks'].append({'id':str(b.get('id') or secrets.token_hex(4))[:50],'type':typ,'content':val,'style':sty,'responsive':{str(k)[:20]:v for k,v in responsive.items() if k in ('mobile','tablet','desktop') and isinstance(v,dict)},'locked':bool(b.get('locked',False)),'name':str(b.get('name',''))[:100]})
                cr['columns'].append(cc)
            cs['rows'].append(cr)
        clean['sections'].append(cs)
    return clean

def media_url(db,media_id):
    if not media_id: return ''
    try: row=db.get(Media,int(media_id))
    except (TypeError,ValueError): return ''
    return '/media/'+row.stored_name if row else ''

def active_promotion(db,code=None):
    t=datetime.now(timezone.utc).replace(tzinfo=None)
    candidates=db.scalars(select(Promotion).where(Promotion.active==True)).all()
    for p in candidates:
        if code is None and not p.automatic: continue
        if code is not None and (p.code.lower()!=str(code).strip().lower()): continue
        if p.starts_at and p.starts_at.replace(tzinfo=None)>t: continue
        if p.ends_at and p.ends_at.replace(tzinfo=None)<t: continue
        if 0<p.percent<=90: return p
    return None

def quote(db, items, coupon=''):
    if not isinstance(items,list) or not 1<=len(items)<=50: raise ValueError('Giỏ hàng trống hoặc vượt giới hạn')
    seen=set(); rows=[]; subtotal=0; discount=0
    promo=active_promotion(db,coupon) if coupon else active_promotion(db)
    if coupon and not promo:raise ValueError('Mã ưu đãi không tồn tại hoặc không còn hiệu lực')
    for entry in items:
        vid=int(entry.get('variant_id',0)); qty=int(entry.get('quantity',0))
        if vid in seen or not 1<=qty<=20: raise ValueError('Biến thể hoặc số lượng không hợp lệ')
        seen.add(vid)
        variant=db.get(Variant,vid)
        prod=db.get(Product,variant.product_id) if variant else None
        if not variant or not prod or not variant.active or not prod.published or variant.price<0: raise ValueError('Một sản phẩm không còn khả dụng')
        if variant.stock is not None and qty>variant.stock: raise ValueError('Số lượng vượt tồn kho được cấu hình')
        images=jloads(prod.images,[])
        if not images: raise ValueError('Sản phẩm chưa có ảnh xác thực')
        line=variant.price*qty
        reduction=(variant.price*promo.percent//100)*qty if promo else 0
        subtotal+=line; discount+=reduction
        rows.append({'product_id':prod.id,'variant_id':vid,'name':prod.name,'variant':variant.name,'sku':variant.sku,'qty':qty,'price':variant.price,'discount':reduction,'total':line-reduction,'image':media_url(db,variant.image_id or images[0])})
    fee=config(db,'shipping_flat','')
    if not fee.isdigit(): raise ValueError('Cửa hàng chưa cấu hình phí vận chuyển, chưa thể chốt đơn')
    shipping=int(fee)
    if shipping<0 or shipping>10000000: raise ValueError('Phí vận chuyển không hợp lệ')
    return {'items':rows,'subtotal':subtotal,'discount':discount,'shipping':shipping,'total':subtotal-discount+shipping,'promotion':promo.code if promo else ''}

def is_open(db): return config(db,'store_open','false')=='true'
def qr_ready(db):
    if not all(config(db,k) for k in ('qr_bank','qr_holder','qr_account','qr_media')):return False
    try:media=db.get(Media,int(config(db,'qr_media')))
    except (ValueError,TypeError):return False
    return bool(media and media.mime.startswith('image/'))

def get_session(db,request):
    cookie=request.cookies.get('chamea_session','')
    if not cookie:return None,None
    session=db.scalar(select(LoginSession).where(LoginSession.token_hash==sha(cookie)))
    if not session or session.expires.replace(tzinfo=None)<datetime.now(timezone.utc).replace(tzinfo=None): return None,None
    u=db.get(User,session.user_id)
    return (u,session) if u and u.active else (None,None)

def require(db,request,roles=('owner','content','orders'),csrf=False):
    u,s=get_session(db,request)
    if not u or u.role not in roles: raise HTTPException(status_code=403,detail='Bạn không có quyền thực hiện thao tác này')
    if csrf:
        token=request.headers.get('x-csrf-token','')
        if not token or not hmac.compare_digest(token,s.csrf): raise HTTPException(status_code=403,detail='Phiên làm việc không hợp lệ (CSRF)')
    return u,s

def safe_style(style):
    if not isinstance(style,dict):return ''
    props=[]
    for key,css in [('color','color'),('background','background-color')]:
        val=str(style.get(key,''))
        if re.fullmatch(r'#[0-9a-fA-F]{3,8}',val):props.append(f'{css}:{val}')
    for key,css,maximum in [('fontSize','font-size',96),('padding','padding',160),('margin','margin',160),('gap','gap',160),('radius','border-radius',100),('height','min-height',1000)]:
        val=str(style.get(key,''))
        if re.fullmatch(r'\d{1,4}',val) and 0<=int(val)<=maximum:props.append(f'{css}:{val}px')
    if style.get('align') in ('left','center','right'):props.append('text-align:'+style['align'])
    if style.get('fit') in ('contain','cover'):props.append('object-fit:'+style['fit'])
    return ';'.join(props)
