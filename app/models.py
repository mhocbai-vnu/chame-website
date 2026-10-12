from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, Boolean, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

def now(): return datetime.now(timezone.utc)

class User(Base):
    __tablename__='users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200),unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String(30),default='content')  # owner, content, orders
    active: Mapped[bool] = mapped_column(Boolean,default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=now)

class LoginSession(Base):
    __tablename__='login_sessions'
    id: Mapped[int] = mapped_column(primary_key=True)
    token_hash: Mapped[str] = mapped_column(String(64),unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    csrf: Mapped[str] = mapped_column(String(64))
    expires: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class Config(Base):
    __tablename__='config'
    key: Mapped[str] = mapped_column(String(100),primary_key=True)
    value: Mapped[str] = mapped_column(Text,default='')

class Media(Base):
    __tablename__='media'
    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String(255))
    stored_name: Mapped[str] = mapped_column(String(100),unique=True)
    mime: Mapped[str] = mapped_column(String(100))
    size: Mapped[int] = mapped_column(Integer)
    width: Mapped[int|None] = mapped_column(Integer,nullable=True)
    height: Mapped[int|None] = mapped_column(Integer,nullable=True)
    alt: Mapped[str] = mapped_column(String(500),default='')
    folder: Mapped[str] = mapped_column(String(100),default='')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=now)

class Category(Base):
    __tablename__='categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(180),unique=True)
    description: Mapped[str] = mapped_column(Text,default='')
    image_id: Mapped[int|None] = mapped_column(ForeignKey('media.id'),nullable=True)
    active: Mapped[bool] = mapped_column(Boolean,default=True)

class Collection(Base):
    __tablename__='collections'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(180),unique=True)
    description: Mapped[str] = mapped_column(Text,default='')
    image_id: Mapped[int|None] = mapped_column(ForeignKey('media.id'),nullable=True)
    active: Mapped[bool] = mapped_column(Boolean,default=True)

class Product(Base):
    __tablename__='products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(200),unique=True)
    sku: Mapped[str] = mapped_column(String(100),unique=True)
    summary: Mapped[str] = mapped_column(Text,default='')
    description: Mapped[str] = mapped_column(Text,default='')
    specs: Mapped[str] = mapped_column(Text,default='{}')
    styles: Mapped[str] = mapped_column(Text,default='[]')
    uses: Mapped[str] = mapped_column(Text,default='[]')
    occasions: Mapped[str] = mapped_column(Text,default='[]')
    receivers: Mapped[str] = mapped_column(Text,default='[]')
    images: Mapped[str] = mapped_column(Text,default='[]')
    video_id: Mapped[int|None] = mapped_column(ForeignKey('media.id'),nullable=True)
    published: Mapped[bool] = mapped_column(Boolean,default=False)
    featured: Mapped[bool] = mapped_column(Boolean,default=False)
    seo_title: Mapped[str] = mapped_column(String(200),default='')
    seo_description: Mapped[str] = mapped_column(String(180),default='')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=now)

class ProductCategory(Base):
    __tablename__='product_categories'
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id',ondelete='CASCADE'),primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'),primary_key=True)

class CollectionProduct(Base):
    __tablename__='collection_products'
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id',ondelete='CASCADE'),primary_key=True)
    collection_id: Mapped[int] = mapped_column(ForeignKey('collections.id'),primary_key=True)
    position: Mapped[int] = mapped_column(Integer,default=0)

class Variant(Base):
    __tablename__='variants'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    name: Mapped[str] = mapped_column(String(160))
    sku: Mapped[str] = mapped_column(String(100),unique=True)
    price: Mapped[int] = mapped_column(Integer)  # VND integer, never float
    image_id: Mapped[int|None] = mapped_column(ForeignKey('media.id'),nullable=True)
    stock: Mapped[int|None] = mapped_column(Integer,nullable=True)  # NULL = not tracked
    active: Mapped[bool] = mapped_column(Boolean,default=True)

class Promotion(Base):
    __tablename__='promotions'
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(80),unique=True)
    label: Mapped[str] = mapped_column(String(200),default='')
    percent: Mapped[int] = mapped_column(Integer,default=0)
    starts_at: Mapped[datetime|None] = mapped_column(DateTime(timezone=True),nullable=True)
    ends_at: Mapped[datetime|None] = mapped_column(DateTime(timezone=True),nullable=True)
    active: Mapped[bool] = mapped_column(Boolean,default=False)
    automatic: Mapped[bool] = mapped_column(Boolean,default=False)

class Page(Base):
    __tablename__='pages'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(200),unique=True)
    kind: Mapped[str] = mapped_column(String(30),default='page')
    draft: Mapped[str] = mapped_column(Text,default='{"sections":[]}')
    live: Mapped[str] = mapped_column(Text,default='{"sections":[]}')
    draft_version: Mapped[int] = mapped_column(Integer,default=1)
    published: Mapped[bool] = mapped_column(Boolean,default=False)
    seo_title: Mapped[str] = mapped_column(String(200),default='')
    seo_description: Mapped[str] = mapped_column(String(180),default='')
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=now)

class Post(Base):
    __tablename__='posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(220))
    slug: Mapped[str] = mapped_column(String(220),unique=True)
    summary: Mapped[str] = mapped_column(Text,default='')
    cover_id: Mapped[int|None] = mapped_column(ForeignKey('media.id'),nullable=True)
    tags: Mapped[str] = mapped_column(Text,default='')
    draft: Mapped[str] = mapped_column(Text,default='{"sections":[]}')
    live: Mapped[str] = mapped_column(Text,default='{"sections":[]}')
    draft_version: Mapped[int] = mapped_column(Integer,default=1)
    published: Mapped[bool] = mapped_column(Boolean,default=False)
    publish_at: Mapped[datetime|None] = mapped_column(DateTime(timezone=True),nullable=True)
    deleted: Mapped[bool] = mapped_column(Boolean,default=False)
    seo_title: Mapped[str] = mapped_column(String(200),default='')
    seo_description: Mapped[str] = mapped_column(String(180),default='')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=now)

class Revision(Base):
    __tablename__='revisions'
    id: Mapped[int] = mapped_column(primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(20))
    entity_id: Mapped[int] = mapped_column(Integer)
    version: Mapped[int] = mapped_column(Integer)
    layout: Mapped[str] = mapped_column(Text)
    actor_id: Mapped[int|None] = mapped_column(ForeignKey('users.id'),nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=now)

class LayoutPreset(Base):
    __tablename__='layout_presets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200),unique=True)
    layout: Mapped[str] = mapped_column(Text)

class Order(Base):
    __tablename__='orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(30),unique=True)
    lookup_token_hash: Mapped[str] = mapped_column(String(64),unique=True)
    receipt_token: Mapped[str] = mapped_column(String(100))
    idem_hash: Mapped[str] = mapped_column(String(64),unique=True)
    customer_name: Mapped[str] = mapped_column(String(150))
    phone: Mapped[str] = mapped_column(String(35))
    email: Mapped[str] = mapped_column(String(200),default='')
    address: Mapped[str] = mapped_column(Text)
    note: Mapped[str] = mapped_column(Text,default='')
    gift_message: Mapped[str] = mapped_column(Text,default='')
    method: Mapped[str] = mapped_column(String(3))
    payment_snapshot: Mapped[str] = mapped_column(Text,default='{}')
    status: Mapped[str] = mapped_column(String(30),default='new')
    payment_status: Mapped[str] = mapped_column(String(30),default='unpaid')
    subtotal: Mapped[int] = mapped_column(Integer)
    discount: Mapped[int] = mapped_column(Integer,default=0)
    shipping: Mapped[int] = mapped_column(Integer)
    total: Mapped[int] = mapped_column(Integer)
    internal_note: Mapped[str] = mapped_column(Text,default='')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=now)

class OrderItem(Base):
    __tablename__='order_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int|None] = mapped_column(ForeignKey('products.id'),nullable=True)
    variant_id: Mapped[int|None] = mapped_column(ForeignKey('variants.id'),nullable=True)
    product_name: Mapped[str] = mapped_column(String(200))
    variant_name: Mapped[str] = mapped_column(String(160))
    sku: Mapped[str] = mapped_column(String(100))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[int] = mapped_column(Integer)
    line_discount: Mapped[int] = mapped_column(Integer)

class Lead(Base):
    __tablename__='leads'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    phone: Mapped[str] = mapped_column(String(35))
    message: Mapped[str] = mapped_column(Text,default='')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=now)

class Newsletter(Base):
    __tablename__='newsletter'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200),unique=True)
    consent: Mapped[bool] = mapped_column(Boolean,default=True)
    unsubscribe_hash: Mapped[str] = mapped_column(String(64),unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=now)

class Audit(Base):
    __tablename__='audit'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int|None] = mapped_column(ForeignKey('users.id'),nullable=True)
    action: Mapped[str] = mapped_column(String(100))
    entity: Mapped[str] = mapped_column(String(120))
    entity_id: Mapped[str] = mapped_column(String(100),default='')
    detail: Mapped[str] = mapped_column(Text,default='')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=now)

class Redirect(Base):
    __tablename__='redirects'
    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(300),unique=True)
    destination: Mapped[str] = mapped_column(String(300))

Index('ix_orders_created',Order.created_at)
Index('ix_revisions_entity',Revision.entity_type,Revision.entity_id)
