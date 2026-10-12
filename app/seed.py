from .models import Config,Category,Collection,Page,Post
from .core import config,setconfig,jdumps
from .db import Base,engine,SessionLocal
from uuid import uuid4
def uid(): return uuid4().hex[:12]

# Mẫu bố cục chỉ chứa nội dung thương hiệu đã được giao; không khởi tạo giá/túi/logo giả.
def b(t,**content): return {'id':uid(),'type':t,'content':content,'style':{},'responsive':{},'locked':False}
def section(*cols): return {'id':uid(),'settings':{},'rows':[{'id':uid(),'columns':[{'id':uid(),'span':12,'blocks':list(blocks)} for blocks in cols]}]}
def layout(*secs): return jdumps({'sections':list(secs)})

HOME=layout(
 section([b('hero',title='Quà tinh tế cho người đặc biệt',subtitle='Một chiếc túi. Một nét riêng.',primary='Khám phá bộ sưu tập',href='/bo-suu-tap',secondary='Tìm túi phù hợp',href2='/goi-y-chon-qua')]),
 section([b('heading',text='Chọn dáng túi, tìm nét riêng'),b('categories')]),
 section([b('heading',text='Những thiết kế dành cho bạn'),b('products')]),
 section([b('heading',text='Trao đúng quà, chạm đúng người'),b('text',text='Khám phá những thiết kế phù hợp với phong cách và những dịp đặc biệt của người bạn trân trọng.'),b('collections')]),
 section([b('gift_banner',title='Trao đúng quà, chạm đúng người',text='Khám phá những thiết kế phù hợp với phong cách và những dịp đặc biệt của người bạn trân trọng.',button='Khám phá quà tặng 20/10',href='/bo-suu-tap/qua-tang-20-10')]),
 section([b('giftquiz')]),
 section([b('brandvideo')]),
 section([b('heading',text='Món quà bắt đầu từ sự thấu hiểu'),b('text',text='CHAMÉA là thương hiệu túi xách dành cho phụ nữ hiện đại, hướng đến thiết kế thanh lịch, nữ tính và dễ ứng dụng. CHAMÉA tin rằng mỗi chiếc túi không chỉ tôn lên gu thẩm mỹ giúp phái đẹp khẳng định bản thân, mà còn là từng lời gửi gắm trân trọng đến người phụ nữ bạn yêu thương. Từ dòng túi công sở tối giản đến thiết kế nổi bật cho buổi gặp gỡ, CHAMÉA mang đến sự thấu hiểu trọn vẹn, giúp mỗi lựa chọn đều vừa vặn với phong cách, nhu cầu và câu chuyện riêng.')]),
 section([b('heading',text='Góc chọn quà'),b('articles')]),
 section([b('consult')]),
)
ABOUT=layout(section([b('heading',text='CHAMÉA — Chạm đúng người · Trao đúng quà'),b('text',text='CHAMÉA là thương hiệu túi xách dành cho phụ nữ hiện đại, hướng đến thiết kế thanh lịch, nữ tính và dễ ứng dụng. Mỗi lựa chọn được bắt đầu từ sự thấu hiểu người sử dụng và người nhận quà.')]))
CONTACT=layout(section([b('heading',text='Liên hệ CHAMÉA'),b('text',text='Thông tin liên hệ đang cập nhật.'),b('consult')]))

POSTS=[
 ('20/10 tặng gì cho phụ nữ? Cách chọn quà phù hợp với người nhận','20-10-tang-gi-cho-phu-nu','Chọn quà theo người nhận, nhu cầu sử dụng và ngân sách.',[
  ('Chọn quà dựa trên sự thấu hiểu','Trước khi quyết định món quà, hãy tìm hiểu người nhận thường sử dụng đồ gì, phong cách yêu thích và điều gì giúp họ thấy thuận tiện trong cuộc sống.'),
  ('Xác định dịp tặng và ngân sách','Một món quà phù hợp không nhất thiết là món quà đắt nhất. Hãy đặt một khoảng ngân sách rõ ràng và cân nhắc thông điệp muốn gửi gắm.'),
  ('Khi nào túi xách là lựa chọn phù hợp?','Túi xách là một gợi ý nếu người nhận có nhu cầu sử dụng. Cần xem kỹ kích thước, kiểu đeo, màu sắc và chính sách đổi trả trước khi chọn.')]),
 ('Bí kíp chọn túi 20/10: Chuẩn gu phái đẹp, vừa vặn ngân sách','bi-kip-chon-tui-20-10','Các tiêu chí thực tế để cân nhắc dáng túi và mức giá.',[
  ('Bắt đầu từ mục đích sử dụng','Đi làm có thể cần đủ chỗ cho các vật dụng thường mang theo; đi chơi hoặc dự tiệc có thể ưu tiên sự gọn nhẹ. Kiểm tra kích thước thật thay vì suy đoán từ ảnh.'),
  ('Phối hợp kiểu dáng và thói quen','Một người thường mang túi đeo vai có thể không thích dùng túi xách tay. Hãy dựa trên cách họ sử dụng túi hằng ngày.'),
  ('Đối chiếu ngân sách và thông tin sản phẩm','So sánh giá bán, phụ kiện đi kèm và các điều kiện ưu đãi đã được cửa hàng công bố. Không nên suy đoán chất liệu hoặc tính năng khi thiếu thông số.')]),
 ('Khám phá những mẫu túi CHAMÉA làm quà tặng 20/10','kham-pha-tui-chamea-20-10','Định hướng chọn túi CHAMÉA theo phong cách và nhu cầu.',[
  ('Khám phá theo kiểu dáng','Bắt đầu bằng danh mục túi xách tay, túi đeo vai hoặc túi đeo chéo khi đã có mẫu đang bán.'),
  ('Chọn theo điều người nhận cần','Lọc túi theo hoàn cảnh sử dụng, phong cách và khoảng giá. Xem hình ảnh từng mẫu trước khi quyết định.'),
  ('Đừng quên lời nhắn','Khi đặt hàng, bạn có thể gửi lời nhắn tặng quà để cửa hàng ghi nhận cùng đơn hàng.')])
]

def initialize():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        defaults={'store_open':'false','shipping_flat':'','announcement':'CHAMÉA — Chạm đúng người · Trao đúng quà','announcement_enabled':'true','sticky_header':'true','brand_logo':'','hero_image':'','hero_mobile':'','gift_image':'','brand_video':'','brand_video_poster':'','qr_bank':'','qr_holder':'','qr_account':'','qr_media':'','email':'','phone':'','address':'','facebook':'','instagram':'','seo_title':'CHAMÉA – Món Quà Cho Người Bạn Trân Trọng','seo_description':'Khám phá những thiết kế túi xách CHAMÉA thanh lịch, dễ ứng dụng và phù hợp với nhiều phong cách, nhu cầu sử dụng và dịp tặng quà.','theme_primary':'#3C2535','theme_accent':'#AB8A6B','theme_bg':'#FEFBFD','menu':'[]'}
        for k,v in defaults.items():
            if db.get(Config,k) is None: setconfig(db,k,v)
        for title,slug in [('Túi xách tay','tui-xach-tay'),('Túi đeo vai','tui-deo-vai'),('Túi đeo chéo','tui-deo-cheo')]:
            if not db.query(Category).filter_by(slug=slug).first(): db.add(Category(name=title,slug=slug))
        for title,slug in [('Quà tặng 20/10','qua-tang-20-10'),('Thanh lịch mỗi ngày','thanh-lich-moi-ngay'),('Điểm nhấn dịu dàng','diem-nhan-diu-dang')]:
            if not db.query(Collection).filter_by(slug=slug).first():db.add(Collection(name=title,slug=slug))
        for name,slug,kind,body,publish in [('Trang chủ','trang-chu','home',HOME,True),('Về CHAMÉA','ve-chamea','page',ABOUT,True),('Liên hệ','lien-he','page',CONTACT,True),('Chính sách giao hàng','giao-hang','policy',layout(section([b('heading',text='Chính sách giao hàng'),b('text',text='Chưa công bố: chủ website cần nhập chính sách thực tế.') ])),False),('Chính sách đổi trả','doi-tra','policy',layout(section([b('heading',text='Chính sách đổi trả'),b('text',text='Chưa công bố: chủ website cần nhập chính sách thực tế.') ])),False),('Chính sách bảo mật','bao-mat','policy',layout(section([b('heading',text='Chính sách bảo mật'),b('text',text='Chưa công bố: chủ website cần nhập chính sách thực tế.') ])),False)]:
            if not db.query(Page).filter_by(slug=slug).first():db.add(Page(name=name,slug=slug,kind=kind,draft=body,live=body if publish else '{"sections":[]}',published=publish))
        for title,slug,summary,topics in POSTS:
            if not db.query(Post).filter_by(slug=slug).first():
                body=layout(section([b('heading',text=title)]+[x for h,p in topics for x in (b('heading',text=h),b('text',text=p))]))
                db.add(Post(title=title,slug=slug,summary=summary,draft=body,live=body,published=True))
        db.commit()
