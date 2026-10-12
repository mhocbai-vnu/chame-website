Hãy đóng vai một nhóm chuyên gia gồm: kiến trúc sư phần mềm, lập trình viên full-stack, chuyên gia thiết kế website thương mại điện tử, chuyên gia UI/UX, chuyên gia CMS và kỹ sư kiểm thử.

NHIỆM VỤ: Xây dựng website thương mại điện tử CHAMÉA hoàn chỉnh, có thể vận hành thực tế, kèm trang quản trị chuyên sâu và trình chỉnh sửa trực quan để chủ website tự quản lý nội dung, hình ảnh, video, sản phẩm, bài viết và thiết kế các trang mà không cần biết lập trình.

Phải tạo website chạy được, có cơ sở dữ liệu, lưu trữ tệp, phân quyền và luồng mua hàng thực tế. Không chỉ tạo ảnh giao diện, bản mô tả, prototype tĩnh hoặc các nút không có chức năng.

Đây là yêu cầu xây dựng bản chính thức. Không được gắn nhãn “chính thức” cho một hệ thống thực chất chỉ lưu dữ liệu cục bộ hoặc mô phỏng việc nhận đơn, gửi biểu mẫu và thanh toán.

────────────────────────

1. BỐI CẢNH VÀ NGUYÊN TẮC TRIỂN KHAI
   ────────────────────────

Thương hiệu: CHAMÉA.

Thông điệp:
“Chạm đúng người · Trao đúng quà”.

CHAMÉA là thương hiệu túi xách dành cho phụ nữ hiện đại, theo phong cách thanh lịch, nữ tính và dễ ứng dụng.

Website phục vụ hai nhóm nhu cầu:

- Khách mua túi cho bản thân.
- Khách tìm quà tặng phụ nữ, cần được hỗ trợ lựa chọn theo phong cách, nhu cầu sử dụng, ngân sách và dịp tặng.

Hành trình chính:
Khám phá thương hiệu → tìm kiểu túi phù hợp → xem chi tiết → chọn biến thể → thêm giỏ hàng → đặt hàng → theo dõi trạng thái đơn.

Ngôn ngữ toàn bộ website và trang quản trị: tiếng Việt tự nhiên, rõ ràng, ấm áp, tinh tế. Không dùng câu quảng cáo sáo rỗng hoặc thuật ngữ kỹ thuật khó hiểu trong giao diện dành cho khách hàng.

Website hiện có để kế thừa nếu được cung cấp quyền truy cập và mã nguồn:
[https://chamea-boutique.sinhvienxuatsac.chatgpt.site](https://chamea-boutique.sinhvienxuatsac.chatgpt.site/)

Trang quản trị hiện có:
[https://chamea-boutique.sinhvienxuatsac.chatgpt.site/quan-tri/](https://chamea-boutique.sinhvienxuatsac.chatgpt.site/quan-tri/)

Nếu nâng cấp website hiện có:

- Kiểm tra cấu trúc, chức năng và dữ liệu trước khi sửa.
- Giữ lại nội dung, ảnh, video và các chỉnh sửa đã lưu của chủ website.
- Sao lưu trước khi thay đổi cấu trúc dữ liệu.
- Không tự ghi đè dữ liệu thật bằng dữ liệu khởi tạo.
- Không tạo website khác thay thế rồi bỏ mất dữ liệu của website cũ.
- Nếu cần thay nền tảng để đáp ứng trình chỉnh sửa chuyên sâu, đề xuất và thực hiện phương án chuyển đổi có kiểm soát, giữ đường dẫn hoặc thiết lập chuyển hướng phù hợp.

Tham khảo [https://matemade.vn/](https://matemade.vn/) về cách tổ chức website bán túi: điều hướng, danh mục dáng túi, bộ sưu tập, ảnh lớn, thẻ sản phẩm, giỏ hàng và footer.

Phát triển thiết kế riêng cho CHAMÉA. Không sao chép logo, ảnh, tên sản phẩm, tên bộ sưu tập hoặc nội dung của thương hiệu tham khảo.

────────────────────────
2\. NHẬN DIỆN VÀ ĐỊNH HƯỚNG THIẾT KẾ
────────────────────────

Bảng màu mặc định:

- Tím mận đậm: #3C2535 — chữ chính, nút chính, footer.
- Nâu champagne: #AB8A6B — chi tiết nhấn, đường kẻ, biểu tượng.
- Be ấm: #BCA388 — mảng nền phụ.
- Trắng ngà: #FEFBFD — nền chính.

Hồng phấn chỉ dùng tiết chế để đồng điệu với hình sản phẩm.

Font:

- Tiêu đề: Noto Serif Display.
- Nội dung, menu, giá và nút: Montserrat.
- Bảo đảm đầy đủ dấu tiếng Việt ở tất cả độ đậm được sử dụng.

Phong cách:

- Thời trang thanh lịch, hiện đại, nữ tính.
- Hình ảnh sản phẩm là trọng tâm.
- Khoảng trắng thoáng, phân cấp rõ, bố cục có nhịp điệu.
- Nền kem và trắng ngà chiếm phần lớn diện tích.
- Tím mận tạo điểm nhấn có chủ đích.
- Không biến cửa hàng thành dashboard.
- Không lạm dụng khung bo tròn, bóng đổ dày, hiệu ứng lấp lánh hoặc chuyển động liên tục.

Logo:

- Dùng nguyên bản logo CHAMÉA được cung cấp, gồm biểu tượng, tên thương hiệu và slogan.
- Giữ đúng màu, tỷ lệ, hình khối và chữ É.
- Không tự vẽ lại biểu tượng, thay font của logo, thêm gradient hoặc hiệu ứng nổi.
- Nếu logo nằm trong ảnh chụp Canva, chỉ lấy phần logo trên nền sạch; không đưa thanh công cụ hoặc khung ứng dụng lên website.
- Nếu thiếu tệp đủ chất lượng, đặt vị trí chờ logo và yêu cầu bổ sung trước khi mở bán; không tự tạo biểu tượng khác.

Thiết kế ban đầu phải chỉn chu ngay cả khi chủ website chưa chỉnh thêm. Khả năng tùy chỉnh không được dùng làm lý do bàn giao giao diện sơ sài.

────────────────────────
3\. TÀI NGUYÊN ẢNH, VIDEO VÀ DỮ LIỆU GỐC
────────────────────────

Sử dụng các ảnh chiến dịch, ảnh túi, logo và video CHAMÉA đã được cung cấp.

Trước khi triển khai:

- Lập danh sách tệp đọc được và tệp đang thiếu.
- Xác định vai trò của từng ảnh: banner ngang, poster dọc, banner quà tặng, ảnh thương hiệu, ảnh sản phẩm.
- Phân biệt các mẫu túi theo kiểu dáng thực tế; không mặc định các túi khác nhau trong các poster là cùng một sản phẩm.
- Không tạo thêm mẫu túi chỉ để đủ số lượng hiển thị.
- Không nhân bản sản phẩm để lấp đầy hàng hoặc bộ sưu tập.
- Nếu tệp đính kèm bị lỗi hoặc không truy cập được, báo đúng tệp cần gửi lại; không nói đã sử dụng tệp chưa đọc được.

Được phép điều chỉnh kích thước hiển thị và tỷ lệ khung bằng bố cục responsive. Không kéo méo hình, đổi màu túi bằng bộ lọc hoặc cắt mất quai, đáy túi và logo.

Video:

- Chèn video được cung cấp vào website bằng trình phát hoạt động thật.
- Giữ đúng tỷ lệ ngang hoặc dọc.
- Có ảnh bìa, nút phát/tạm dừng, điều chỉnh âm lượng và toàn màn hình.
- Hỗ trợ phát trong trang trên điện thoại.
- Không tự phát có âm thanh.
- Chỉ bật tự phát tắt tiếng khi được cấu hình.
- Tránh tải toàn bộ video ngay khi khách vừa mở trang.
- Có trạng thái tải, lỗi phát và phương án thử lại.
- Không hiển thị khung video rỗng nếu chưa có tệp.

────────────────────────
4\. HỆ THỐNG TRANG VÀ ĐIỀU HƯỚNG
────────────────────────

Xây dựng đầy đủ:

- Trang chủ.
- Tất cả túi xách.
- Trang danh mục dáng túi.
- Trang bộ sưu tập.
- Chi tiết từng bộ sưu tập.
- Chi tiết sản phẩm.
- Gợi ý chọn quà.
- Về CHAMÉA.
- Liên hệ.
- Góc chọn quà / danh sách bài viết.
- Chi tiết bài viết.
- Kết quả tìm kiếm.
- Danh sách yêu thích.
- Giỏ hàng.
- Thanh toán.
- Kết quả đặt hàng.
- Tra cứu đơn hàng có kiểm soát quyền truy cập.
- Các trang chính sách.
- Trang 404.
- Trang quản trị.

Menu chính mặc định:

TRANG CHỦ | TÚI XÁCH | BỘ SƯU TẬP | GỢI Ý CHỌN QUÀ | VỀ CHAMÉA | LIÊN HỆ.

Menu Túi xách có danh mục con dựa trên dữ liệu thực tế, chẳng hạn:

- Túi xách tay.
- Túi đeo vai.
- Túi đeo chéo.

Một sản phẩm có thể thuộc nhiều danh mục nếu có căn cứ.

Các bộ sưu tập biên tập ban đầu:

- Quà tặng 20/10.
- Thanh lịch mỗi ngày.
- Điểm nhấn dịu dàng.

Header:

- Logo.
- Menu.
- Tìm kiếm.
- Yêu thích.
- Giỏ hàng kèm số lượng.
- Cố định gọn khi cuộn, có thể bật/tắt trong quản trị.
- Điện thoại và tablet nhỏ dùng menu thu gọn phù hợp.

Tất cả menu, đường dẫn và nút phải hoạt động thật.

────────────────────────
5\. TRANG CHỦ — BỐ CỤC MẶC ĐỊNH
────────────────────────

Bố cục mặc định theo thứ tự dưới đây, nhưng chủ website có thể sắp xếp lại bằng trình chỉnh sửa.

A. Thanh thông báo

“CHAMÉA — Chạm đúng người · Trao đúng quà”.

Cho phép sửa nội dung, màu nền, màu chữ, liên kết, lịch hiển thị và bật/tắt.

Ảnh chiến dịch có ưu đãi 20%. Chỉ dùng ưu đãi trong bản chính thức khi đã cấu hình thời gian, điều kiện và sản phẩm áp dụng. Không tự bịa thời gian.

B. Banner chính

Ưu tiên banner ngang có ba túi trên bệ đá cho laptop; dùng poster dọc phù hợp trên điện thoại.

Giữ ánh sáng ấm, nền kem, tím mận, hoa và bệ đá của ảnh gốc.

Headline:
“Quà tinh tế cho người đặc biệt”.

Thông điệp phụ:
“Một chiếc túi. Một nét riêng.”

CTA chính:
“Khám phá bộ sưu tập”.

CTA phụ:
“Tìm túi phù hợp”.

Nếu ảnh đã chứa headline, không chèn thêm chữ trùng. Nếu ảnh có hình nút in sẵn, xử lý để khách không nhầm đó là nút không hoạt động; không tạo hai lớp nút hoặc chữ chồng nhau.

Ưu tiên nội dung chữ và nút là thành phần HTML có thể chỉnh sửa. Nếu cần thay ảnh để tách chữ khỏi ảnh, sử dụng tài nguyên được phê duyệt và giữ nguyên sản phẩm, logo.

C. Danh mục dáng túi

Headline:
“Chọn dáng túi, tìm nét riêng”.

Hiển thị ảnh đại diện theo các dáng túi thực có. Bấm vào danh mục mở trang sản phẩm với bộ lọc tương ứng.

D. Sản phẩm nổi bật

Headline:
“Những thiết kế dành cho bạn”.

Mặc định laptop 3–4 cột tùy số lượng; điện thoại 2 cột.

Mỗi thẻ gồm:

- Ảnh rõ, tỷ lệ đồng nhất.
- Tên sản phẩm.
- Giá bán.
- Giá trước giảm và nhãn giảm giá khi có chương trình hợp lệ.
- Màu/biến thể thực có.
- Nút yêu thích.
- Nút “Chọn túi”.

Không tự dùng nhãn “bán chạy” khi chưa có dữ liệu.

E. Bộ sưu tập quà tặng

Dùng banner tím mận có hộp quà được cung cấp.

Headline ngoài ảnh:
“Trao đúng quà, chạm đúng người”.

Mô tả:
“Khám phá những thiết kế phù hợp với phong cách và những dịp đặc biệt của người bạn trân trọng.”

CTA:
“Khám phá quà tặng 20/10”.

Nếu ảnh có chữ “10 mẫu túi” nhưng số lượng chưa được xác nhận, không tạo đủ 10 sản phẩm giả. Sử dụng vùng ảnh phù hợp không chứa con số hoặc thay bằng phiên bản ảnh được xử lý/phê duyệt, không làm biến dạng túi.

F. Công cụ chọn quà

Headline:
“Bạn đang tìm túi cho ai?”

Các bước:

- Người nhận: mẹ, người yêu, vợ, bạn bè, bản thân.
- Phong cách: tối giản, nữ tính, nổi bật.
- Nhu cầu: đi làm, đi chơi, dự tiệc.
- Ngân sách: khoảng giá phù hợp dữ liệu thực tế.
- Dịp: 20/10, 8/3, sinh nhật, kỷ niệm.

CTA:
“Tìm chiếc túi phù hợp”.

Kết quả phải dựa trên thuộc tính sản phẩm và giải thích ngắn vì sao phù hợp.

Không suy luận sở thích chỉ từ tuổi hoặc mối quan hệ. Nếu không có kết quả, gợi ý điều chỉnh tiêu chí; không đưa sản phẩm không khớp rồi khẳng định là phù hợp hoàn toàn.

G. Video thương hiệu

Bố trí video trong khối riêng phù hợp nhịp trang, mặc định không phát có âm thanh.

Có thể đặt video cạnh chữ, cạnh ảnh, toàn chiều rộng hoặc trong bố cục nhiều cột. Chủ website được thay đổi vị trí khối này.

H. Giới thiệu thương hiệu

Headline:
“Món quà bắt đầu từ sự thấu hiểu”.

Nội dung:

“CHAMÉA là thương hiệu túi xách dành cho phụ nữ hiện đại, hướng đến thiết kế thanh lịch, nữ tính và dễ ứng dụng. CHAMÉA tin rằng mỗi chiếc túi không chỉ tôn lên gu thẩm mỹ giúp phái đẹp khẳng định bản thân, mà còn là từng lời gửi gắm trân trọng đến người phụ nữ bạn yêu thương. Từ dòng túi công sở tối giản đến thiết kế nổi bật cho buổi gặp gỡ, CHAMÉA mang đến sự thấu hiểu trọn vẹn, giúp mỗi lựa chọn đều vừa vặn với phong cách, nhu cầu và câu chuyện riêng.”

Kết hợp ảnh và chữ. Không đặt cả đoạn dài trực tiếp lên ảnh.

I. Góc chọn quà

Ba bài viết ban đầu:

1. “20/10 tặng gì cho phụ nữ? Cách chọn quà phù hợp với người nhận”.
2. “Bí kíp chọn túi 20/10: Chuẩn gu phái đẹp, vừa vặn ngân sách”.
3. “Khám phá những mẫu túi CHAMÉA làm quà tặng 20/10”.

Mỗi thẻ có ảnh, tóm tắt và liên kết đến bài viết hoàn chỉnh. Nội dung bài có thể sửa, bổ sung và xuất bản từ quản trị.

J. Khối tư vấn

Headline:
“Chưa biết chọn mẫu nào?”

Nội dung:
“CHAMÉA giúp bạn cân nhắc theo phong cách, nhu cầu và ngân sách.”

CTA:
“Nhận tư vấn chọn túi”.

────────────────────────
6\. DANH MỤC, BỘ SƯU TẬP VÀ TÌM KIẾM
────────────────────────

Trang danh mục và bộ sưu tập có:

- Banner.
- Tiêu đề.
- Mô tả ngắn.
- Số lượng sản phẩm thực tế.
- Bộ lọc.
- Sắp xếp.
- Phân trang hoặc tải thêm phù hợp.

Bộ lọc:

- Dáng túi.
- Màu.
- Khoảng giá.
- Nhu cầu sử dụng.
- Các thuộc tính khác chỉ khi có dữ liệu.

Sắp xếp:

- Giá tăng dần.
- Giá giảm dần.
- Mới nhất chỉ khi có ngày tạo/xuất bản.
- Không thêm “bán chạy” khi chưa có dữ liệu đơn hàng phù hợp.

Bộ lọc trên điện thoại dùng bảng trượt, có áp dụng, xóa bộ lọc và số kết quả.

Tìm kiếm:

- Theo tên, mã sản phẩm và nội dung phù hợp.
- Hỗ trợ tìm tiếng Việt có dấu/không dấu.
- Có trạng thái đang tìm, không tìm thấy và lỗi.
- Không mất bộ lọc một cách khó hiểu khi chuyển trang hoặc quay lại.

────────────────────────
7\. CHI TIẾT SẢN PHẨM
────────────────────────

Đây là khu vực ưu tiên cao.

Đầu trang có breadcrumb; laptop chia thư viện ảnh bên trái và thông tin mua hàng bên phải. Điện thoại sắp xếp lại hợp lý.

Thư viện ảnh theo thứ tự:

1. Tổng quan toàn bộ túi.
2. Góc nghiêng, mặt sau hoặc bên trong nếu có.
3. Cận chất liệu, đường may, khóa, quai.
4. Hàng đi kèm đã xác nhận.

Có thumbnail, chuyển ảnh, phóng to và thao tác chạm phù hợp.

Không dùng một ảnh cho mọi góc. Không suy đoán cấu tạo bên trong, chất liệu hoặc phụ kiện từ poster.

Trong quá trình chuẩn bị, ảnh thiếu phải có trạng thái rõ ràng. Bản mở bán không được có ảnh hỏng. Ảnh minh họa phải ghi đúng tính chất, không dùng làm bằng chứng chất liệu.

Thông tin mua hàng:

- Tên.
- Mã.
- Giá.
- Giá trước giảm khi hợp lệ.
- Màu/biến thể đang chọn.
- Tình trạng khả dụng dựa trên dữ liệu thật.
- Chọn biến thể và số lượng.
- “Thêm vào giỏ hàng”.
- “Mua ngay”.
- “Nhận tư vấn mẫu này”.

Đổi màu chỉ đổi ảnh khi có ảnh đúng của biến thể. Không dùng bộ lọc để giả lập màu sản phẩm.

Nội dung bên dưới theo thứ tự:

- Tổng quan.
- Chất liệu và chi tiết.
- Hàng đi kèm.
- Bảo quản.
- Giao hàng, đổi trả, thanh toán.
- Sản phẩm liên quan.

Thông số có trường dữ liệu riêng:

- Chất liệu thân túi.
- Lớp lót.
- Khóa.
- Quai/dây đeo.
- Kích thước.
- Trọng lượng.

Hàng đi kèm phải phân biệt món nằm trong giá và lựa chọn mua thêm.

Thông tin chưa xác nhận không được tự điền. Không bịa da thật, chống nước, độ bền, bảo hành, chứng nhận hoặc đánh giá.

────────────────────────
8\. GIỎ HÀNG VÀ ĐẶT HÀNG THẬT
────────────────────────

Có giỏ hàng dạng bảng trượt và trang riêng.

Mỗi dòng gồm:

- Ảnh.
- Tên túi.
- Biến thể/màu.
- Đơn giá.
- Số lượng.
- Thành tiền.
- Xóa.

Có tạm tính, giảm giá, phí vận chuyển và tổng thanh toán.

Giỏ hàng được giữ khi tải lại trang. Khi đặt hàng, máy chủ phải kiểm tra lại giá, ưu đãi, biến thể và khả năng cung cấp; không tin số tiền do trình duyệt gửi lên.

Nếu giảm giá 20%:
Giá bán = giá niêm yết × 0,8.

Không giảm thêm lần nữa ở giỏ hàng.

Checkout gồm:

- Họ tên.
- Số điện thoại.
- Email không bắt buộc, trừ trường hợp một chức năng thực tế cần email và đã giải thích rõ.
- Địa chỉ giao hàng.
- Ghi chú.
- Lời nhắn tặng quà.
- Phương thức thanh toán.
- Tóm tắt đơn.
- Phí vận chuyển.
- Giảm giá.
- Tổng tiền.
- Liên kết chính sách liên quan.

Cho phép khách đặt hàng không bắt buộc tạo tài khoản.

Đơn hàng phải lưu vào cơ sở dữ liệu và xuất hiện trong quản trị.

Nút đặt hàng có trạng thái đang xử lý và ngăn gửi lặp. Máy chủ có cơ chế chống tạo trùng khi khách bấm nhiều lần hoặc mạng gửi lại yêu cầu.

Chỉ hiển thị đặt hàng thành công sau khi máy chủ xác nhận lưu đơn thành công.

Nếu gửi thông báo email thất bại nhưng đơn đã lưu, không làm khách đặt lại một đơn trùng. Thông báo đúng trạng thái và cho quản trị xử lý.

Phí vận chuyển:

- Cấu hình được theo mô hình thực tế của cửa hàng.
- Không mặc định miễn phí khi chưa có dữ liệu.
- Nếu chưa xác định, ghi rõ “Chưa xác định”.
- Không trình bày số tiền hàng như tổng cuối cùng đã gồm vận chuyển.
- Nếu nhận đơn trước để báo phí sau, phải nêu rõ và có bước khách xác nhận tổng tiền trước khi yêu cầu chuyển tiền.

────────────────────────
9\. THANH TOÁN — CHỈ COD VÀ QR
────────────────────────

Toàn website chỉ có hai phương thức:

1. COD — thanh toán khi nhận hàng.
2. QR — chuyển khoản bằng mã QR.

Không có lựa chọn thứ ba như thẻ, ví điện tử, thanh toán trực tuyến hoặc “chuyển khoản” tách thành phương thức riêng.

COD:

- Khách chọn COD và đặt hàng.
- Đơn được lưu với trạng thái thanh toán chưa thu tiền.
- Chỉ cập nhật đã thu tiền khi có xác nhận thực tế phù hợp.

QR:

- Dùng thông tin ngân hàng và mã QR do chủ website cung cấp hoặc cấu hình hợp lệ.
- Có tên ngân hàng, chủ tài khoản, số tài khoản, số tiền và nội dung chuyển khoản theo đơn khi được hỗ trợ.
- Có nút sao chép số tài khoản, số tiền và nội dung chuyển khoản.
- Không tự bịa ngân hàng, số tài khoản hoặc QR.
- QR cố định phải được ghi đúng là QR cố định; không khẳng định đã gắn số tiền/mã đơn nếu thực tế chưa có.
- Nếu dùng QR tạo theo đơn, triển khai bằng giải pháp hợp lệ và kiểm tra số tiền, tài khoản nhận, nội dung chuyển khoản.
- Mã QR phải xuất phát từ cấu hình được máy chủ kiểm soát, không cho khách tự thay tài khoản nhận tiền qua dữ liệu đầu vào.

Trạng thái thanh toán:

- Chưa thanh toán.
- Chờ xác minh.
- Đã thanh toán.
- Các trạng thái hoàn tiền nếu quy trình thực tế có hỗ trợ.

Nút “Tôi đã chuyển khoản”, nếu có, chỉ gửi yêu cầu xác minh. Không được tự đánh dấu đã thanh toán.

Xác nhận tiền:

- Thủ công bởi người có quyền, có lịch sử thao tác; hoặc
- Tự động qua tích hợp đã cấu hình, kiểm tra tính xác thực và đối chiếu chính xác.

Không giả lập webhook hoặc xác nhận thanh toán tự động khi chưa tích hợp.

Nếu chưa có cấu hình QR hợp lệ, QR ở trạng thái chưa khả dụng và không cho khách chuyển tiền. Khi bàn giao để mở bán đầy đủ hai phương thức, phải bổ sung cấu hình này.

────────────────────────
10\. TRANG QUẢN TRỊ — YÊU CẦU CỐT LÕI
────────────────────────

Chủ website phải được quyền quản lý toàn bộ nội dung và thiết kế trình bày thông thường của website.

Không chỉ làm vài ô sửa tên, giá và ảnh.

Không được đóng gói toàn bộ trang thành một khối “nội dung gốc” không thể chỉnh bên trong rồi gọi đó là quyền chỉnh toàn bộ.

Cần cung cấp:

- Bảng tổng quan sử dụng dữ liệu thật.
- Quản lý trang.
- Trình thiết kế trực quan.
- Quản lý sản phẩm và biến thể.
- Danh mục.
- Bộ sưu tập.
- Bài viết.
- Thư viện ảnh/video.
- Menu.
- Header và footer.
- Thương hiệu và liên hệ.
- Ưu đãi.
- Giao hàng.
- COD và QR.
- Đơn hàng.
- Yêu cầu tư vấn và đăng ký nhận tin.
- SEO.
- Người dùng quản trị và phân quyền.
- Sao lưu, lịch sử phiên bản và khôi phục.

Giao diện quản trị phải dễ dùng trên laptop, iPad và điện thoại. Trên màn hình nhỏ vẫn thực hiện được các thao tác chính, không bắt buộc dùng chuột.

Có tìm kiếm, lọc, sắp xếp và thao tác hàng loạt phù hợp.

Không đưa số liệu doanh thu, đơn hàng hoặc biểu đồ giả để trang quản trị trông “đầy”.

────────────────────────
11\. TRÌNH THIẾT KẾ TRỰC QUAN CHO TOÀN WEBSITE
────────────────────────

Xây dựng page builder có cấu trúc:

Trang → khu vực → hàng → cột → khối nội dung.

Có thể kéo thả, chọn khối trực tiếp trên bản xem trước và chỉnh bằng bảng thuộc tính.

Bắt buộc hỗ trợ các bố cục:

- Một cột.
- Hai cột bằng nhau: 1 | 1.
- Ba cột bằng nhau: 1 | 1 | 1.
- Bốn cột bằng nhau nếu phù hợp.
- Hai cột lệch: 2 | 1 hoặc 1 | 2.
- Các tỷ lệ khác do người dùng chỉnh.
- Xếp ngang hoặc dọc.
- Khối toàn chiều rộng.
- Khối giới hạn chiều rộng.
- Ảnh bên trái, chữ bên phải và ngược lại.
- Video cạnh ảnh hoặc cạnh chữ.
- Ba ảnh cạnh nhau.
- Lưới ảnh.
- Nội dung có nền màu hoặc ảnh nền.
- Bố cục lồng trong cột ở mức hợp lý, không gây khó sử dụng.

Người dùng được:

- Thêm, xóa, nhân bản khối.
- Kéo thả đổi thứ tự.
- Di chuyển khối giữa các cột/hàng.
- Thêm hoặc bớt cột.
- Chỉnh tỷ lệ cột bằng tay nắm và ô nhập số.
- Đổi ngang/dọc.
- Căn trái, giữa, phải.
- Căn trên, giữa, dưới.
- Chỉnh khoảng cách giữa cột.
- Chỉnh padding, margin, chiều rộng và chiều cao.
- Chọn nền, viền, bo góc và bóng đổ.
- Bật/tắt khối theo thiết bị.
- Lưu khối hoặc bố cục làm mẫu để tái sử dụng.
- Khóa khối để tránh sửa nhầm.
- Hoàn tác và làm lại.
- Đổi tên khối trong cây cấu trúc.

Các loại khối tối thiểu:

- Tiêu đề.
- Đoạn văn.
- Văn bản có định dạng.
- Ảnh.
- Video.
- Thư viện ảnh.
- Nút.
- Đường phân cách.
- Khoảng trống.
- Banner.
- Sản phẩm đơn.
- Lưới sản phẩm.
- Danh mục.
- Bộ sưu tập.
- Danh sách bài viết.
- Bài viết nổi bật.
- Công cụ chọn quà.
- Biểu mẫu tư vấn.
- Đăng ký nhận tin.
- FAQ dạng mở/đóng.
- Biểu tượng kèm nội dung.
- Các thành phần mua hàng chuyên dụng.

Với trang sản phẩm, giỏ hàng và checkout:

- Cho phép chỉnh cách bố trí, thứ tự và định dạng các thành phần.
- Nội dung, ảnh và thông số có trường chỉnh riêng.
- Giữ liên kết dữ liệu giữa giá, biến thể, giỏ hàng và đơn hàng.
- Không cho việc chỉnh giao diện làm sai phép tính hoặc bỏ kiểm tra bắt buộc.
- Nếu một thao tác có thể vô hiệu hóa luồng mua hàng, giải thích rõ và kiểm tra trước khi xuất bản.

Responsive:

- Có chế độ laptop, tablet/iPad và điện thoại.
- Cho nhập chiều rộng xem trước cụ thể.
- Cho cấu hình riêng số cột, thứ tự xếp, căn chỉnh, khoảng cách, cỡ chữ và tỷ lệ ảnh theo từng nhóm màn hình.
- Cho phép kế thừa cấu hình chung hoặc ghi đè trên từng thiết bị.
- Thay đổi cấu hình điện thoại không tự phá bố cục laptop.
- Luôn có bố cục tự thích ứng khi chưa cấu hình riêng.

Không giới hạn quyền chỉnh thiết kế vào một bảng CSS khó dùng. CSS nâng cao là công cụ bổ sung cho người có chuyên môn; các thao tác phổ biến phải thực hiện được bằng giao diện.

────────────────────────
12\. CHỈNH ẢNH VÀ VIDEO TRONG PAGE BUILDER
────────────────────────

Mỗi khối ảnh/video có thể:

- Chọn từ thư viện.
- Tải tệp mới.
- Thay tệp.
- Gỡ tệp.
- Thêm văn bản thay thế hoặc chú thích phù hợp.
- Chọn tỷ lệ gốc hoặc tỷ lệ khung.
- Chọn 1:1, 4:3, 3:2, 16:9, 21:9, 9:16 và tỷ lệ tùy chỉnh.
- Chọn giữ trọn nội dung hoặc lấp đầy khung.
- Chỉnh điểm lấy nét/vị trí hiển thị khi cắt.
- Xem vùng bị cắt trước khi lưu.
- Chỉnh chiều rộng, chiều cao tối đa và căn chỉnh.
- Chọn ảnh riêng cho điện thoại.
- Gắn liên kết cho ảnh nếu cần.

Mặc định ảnh sản phẩm dùng chế độ giữ trọn túi. Không tự cắt mất quai hoặc đáy.

Video có thêm:

- Ảnh bìa.
- Bật/tắt điều khiển khi phù hợp.
- Tự phát tắt tiếng.
- Lặp lại.
- Phát trong trang.
- Phụ đề nếu có.
- Thiết lập tải trước phù hợp.
- Nhúng từ nguồn được cho phép hoặc tải tệp trực tiếp.

Không nhúng tùy ý mã script hoặc iframe không được kiểm soát.

────────────────────────
13\. QUẢN LÝ BÀI VIẾT CHUYÊN SÂU
────────────────────────

Chủ website phải dễ dàng tạo bài mới, không chỉ sửa ba bài có sẵn.

Có đầy đủ:

- Thêm bài.
- Sửa.
- Nhân bản.
- Lưu nháp.
- Xem trước.
- Hẹn giờ xuất bản.
- Xuất bản.
- Gỡ xuất bản.
- Chuyển vào thùng rác.
- Khôi phục.
- Xóa vĩnh viễn với xác nhận rõ ràng.

Trường bài viết:

- Tiêu đề.
- Slug.
- Tóm tắt.
- Ảnh đại diện.
- Nội dung.
- Danh mục.
- Thẻ.
- Tác giả được cấu hình.
- Thời gian xuất bản.
- Bài liên quan.
- Sản phẩm/bộ sưu tập liên quan.
- SEO title.
- Meta description.
- Ảnh chia sẻ.

Trình soạn bài hỗ trợ:

- H2, H3 và phân cấp tiêu đề.
- Đậm, nghiêng, danh sách, liên kết.
- Trích dẫn.
- Bảng có khả năng hiển thị tốt trên điện thoại.
- Chèn ảnh/video tại vị trí bất kỳ.
- Chú thích ảnh.
- Album.
- Nút CTA.
- Khối sản phẩm liên quan.
- Bố cục 1 cột, 2 cột, 3 cột, tỷ lệ lệch.
- Kéo thả sắp xếp nội dung.
- Mục lục nếu bài dài.
- Lưu tự động bản nháp.
- Khôi phục phiên bản trước.

Nội dung dán từ Word/Google Docs phải được làm sạch định dạng thừa, không phá font, màu và khoảng cách của website.

Không dùng một textarea duy nhất cho toàn bộ bài dài.

────────────────────────
14\. QUẢN LÝ SẢN PHẨM, DANH MỤC VÀ BỘ SƯU TẬP
────────────────────────

Cho phép thêm sản phẩm mới, sửa, nhân bản thành bản nháp, ẩn, lưu trữ và xóa theo điều kiện dữ liệu.

Không khóa cứng danh sách sản phẩm vào số mẫu ban đầu.

Sản phẩm có:

- Tên.
- Slug.
- Mã sản phẩm.
- Mô tả ngắn/dài.
- Giá.
- Danh mục.
- Biến thể.
- Màu.
- Ảnh theo biến thể.
- Thư viện ảnh có thứ tự.
- Video nếu có.
- Thông số.
- Hàng đi kèm.
- Bảo quản.
- Nhu cầu sử dụng.
- Phong cách.
- SEO.
- Trạng thái hiển thị.
- Dữ liệu tồn kho nếu cửa hàng sử dụng quản lý tồn kho.

Không tự bật quản lý tồn kho bằng số giả. Nếu chưa có dữ liệu, không hiển thị thông báo khan hiếm.

Bộ sưu tập:

- Thêm/sửa/ẩn/xóa.
- Chọn sản phẩm bằng giao diện.
- Kéo thả thứ tự.
- Chỉnh banner ngang/dọc.
- Chỉnh mô tả và bố cục.
- Hẹn giờ hiển thị khi cần.

Không xóa dữ liệu lịch sử đơn hàng khi sản phẩm bị ẩn hoặc lưu trữ. Đơn hàng lưu bản chụp tên, biến thể và giá tại thời điểm đặt.

────────────────────────
15\. THƯ VIỆN TỆP
────────────────────────

Có thư viện ảnh/video tập trung với:

- Tải nhiều tệp.
- Kéo thả tải lên.
- Thanh tiến trình.
- Thông báo lỗi cụ thể.
- Tìm kiếm.
- Lọc ảnh/video.
- Thư mục hoặc nhãn.
- Tên tệp, dung lượng, kích thước, thời lượng video nếu xác định được.
- Chú thích và alt text.
- Thông tin tệp đang được dùng ở đâu.
- Cảnh báo trước khi xóa tệp đang được sử dụng.
- Thay tệp có kiểm soát và xem trước phạm vi ảnh hưởng.

Tệp phải được lưu trên hệ thống lưu trữ lâu dài, không chỉ trong bộ nhớ trình duyệt hoặc đường dẫn tạm.

Có giới hạn dung lượng và loại tệp rõ ràng, phù hợp với video thực tế được cung cấp. Không đặt giới hạn thấp khiến video gốc không thể sử dụng mà không có phương án xử lý.

Tối ưu ảnh để tải nhanh, giữ bản gốc phục vụ chỉnh sửa. Không nén đến mức logo, chữ và chi tiết túi bị nhòe.

────────────────────────
16\. HEADER, FOOTER, MENU VÀ THIẾT LẬP CHUNG
────────────────────────

Chủ website chỉnh được:

- Logo.
- Kích thước logo.
- Thanh thông báo.
- Mục menu.
- Menu con.
- Thứ tự.
- Thêm/xóa mục.
- Liên kết.
- Cách hiển thị theo thiết bị.
- Header cố định.
- Nội dung và số cột footer.
- Thông tin liên hệ.
- Mạng xã hội.
- Màu, font, cỡ chữ, nút và khoảng cách chung.

Footer mặc định nền tím mận, chữ sáng, gồm:

- Logo và slogan.
- Khám phá.
- Hỗ trợ.
- Liên hệ.
- Mạng xã hội.
- Đăng ký nhận tin.
- Thông tin COD và QR phù hợp cấu hình.

Không bịa hotline, địa chỉ, email, tài khoản xã hội, mã số doanh nghiệp hoặc chứng nhận Bộ Công Thương.

Trong giai đoạn chuẩn bị có thể ghi “Thông tin đang cập nhật”. Trước mở bán phải rà soát các thông tin bắt buộc và chính sách thực tế.

────────────────────────
17\. LƯU NHÁP, XUẤT BẢN VÀ KHÔI PHỤC
────────────────────────

Phân biệt rõ:

- Nội dung đang chỉnh.
- Bản nháp đã lưu.
- Bản đang công khai.

Lưu tự động chỉ lưu nháp, không tự xuất bản mọi thao tác kéo thả.

Có nút:

- Lưu nháp.
- Xem trước.
- Xuất bản/Cập nhật.
- Bỏ thay đổi.
- Hoàn tác/Làm lại.
- Xem lịch sử.
- Khôi phục phiên bản.

Có cảnh báo khi rời trang với thay đổi chưa lưu.

Nếu hai phiên cùng sửa một nội dung, phát hiện xung đột; không âm thầm ghi đè.

Khôi phục phiên bản giao diện hoặc bài viết không được làm mất đơn hàng, yêu cầu tư vấn hoặc dữ liệu vận hành mới phát sinh.

────────────────────────
18\. PHÂN QUYỀN, QUYỀN SỞ HỮU VÀ BẢO MẬT
────────────────────────

Chủ website có tài khoản quản trị cao nhất và được bàn giao cách truy cập.

Phân quyền tối thiểu:

- Chủ website.
- Quản trị nội dung.
- Nhân viên xử lý đơn.

Kiểm tra quyền ở máy chủ cho tất cả thao tác quản trị, tải tệp và cập nhật thanh toán. Không chỉ ẩn nút ở giao diện.

Không hardcode tài khoản của lập trình viên thành chủ sở hữu duy nhất khiến người dùng không thể tiếp quản.

Có cơ chế đăng nhập, đăng xuất, quản lý phiên và bảo vệ tài khoản phù hợp nền tảng. Hỗ trợ xác thực tăng cường nếu nền tảng cho phép.

Các yêu cầu kỹ thuật:

- Kiểm tra dữ liệu đầu vào.
- Bảo vệ chống XSS, CSRF và truy cập trái phép.
- Làm sạch rich text và nội dung nhúng.
- Không cho tải tệp thực thi.
- Giới hạn yêu cầu nhạy cảm và chống spam.
- Không đưa khóa bí mật vào mã frontend.
- Không đưa dữ liệu cá nhân vào log không cần thiết.
- Không cho tra cứu đơn chỉ bằng mã dễ đoán mà lộ tên, số điện thoại, địa chỉ.
- Lưu lịch sử thay đổi quan trọng: tài khoản nhận QR, giá, trạng thái thanh toán và quyền quản trị.

Chủ website được bàn giao:

- Mã nguồn.
- Cấu trúc dữ liệu.
- Cách sao lưu và xuất dữ liệu.
- Cách quản lý tên miền, hosting và tài nguyên liên quan.
- Danh sách dịch vụ bên ngoài và chi phí nếu có.

Quyền chỉnh toàn bộ nội dung/giao diện thông thường phải thực hiện được trong CMS. Thay đổi chức năng nghiệp vụ mới ngoài phạm vi CMS cần có mã nguồn và quy trình triển khai, không giả vờ rằng một trình kéo thả có thể chỉnh mọi hành vi phần mềm.

────────────────────────
19\. QUẢN LÝ ĐƠN VÀ BIỂU MẪU THỰC TẾ
────────────────────────

Đơn hàng:

- Danh sách, tìm kiếm, bộ lọc.
- Chi tiết sản phẩm và biến thể.
- Thông tin người nhận.
- Ghi chú/lời nhắn.
- Phương thức COD hoặc QR.
- Số tiền.
- Trạng thái thanh toán.
- Trạng thái xử lý/giao hàng.
- Lịch sử thay đổi.
- Ghi chú nội bộ.
- Xuất dữ liệu phù hợp quyền.

Tách trạng thái đơn hàng khỏi trạng thái thanh toán.

Không tự coi “đã giao” là “đã thanh toán” nếu chưa có căn cứ từ quy trình thực tế.

Biểu mẫu tư vấn và đăng ký nhận tin:

- Lưu dữ liệu thật vào hệ thống.
- Chỉ báo gửi thành công khi đã lưu/tiếp nhận thành công.
- Có chống spam và kiểm tra đầu vào.
- Quản trị xem được dữ liệu gửi đến.
- Nếu có gửi email hoặc thông báo, dùng dịch vụ được cấu hình thật.
- Đăng ký nhận tin có cơ chế đồng ý và hủy đăng ký phù hợp.

────────────────────────
20\. SEO VÀ KHẢ NĂNG TIẾP CẬN
────────────────────────

Tiêu đề trang chủ:
“CHAMÉA – Món Quà Cho Người Bạn Trân Trọng”.

Mô tả đề xuất:
“Khám phá những thiết kế túi xách CHAMÉA thanh lịch, dễ ứng dụng và phù hợp với nhiều phong cách, nhu cầu sử dụng và dịp tặng quà.”

Đếm ký tự thực tế, gồm khoảng trắng, bảo đảm không vượt 155 ký tự. Nếu cần rút gọn, giữ ý chính.

Yêu cầu:

- Tiêu đề và mô tả riêng cho từng trang.
- Một H1 phù hợp mỗi trang.
- H2/H3 đúng cấu trúc.
- Slug ngắn, không dấu.
- Alt text.
- Canonical.
- Sitemap.
- Robots phù hợp.
- Open Graph và ảnh chia sẻ.
- Dữ liệu có cấu trúc chỉ dùng thông tin thật.
- Không tạo rating/review schema giả.
- Trang nháp, quản trị và nội dung riêng tư không được đưa vào chỉ mục.
- Đổi slug có phương án chuyển hướng để tránh hỏng liên kết.

Khả năng tiếp cận:

- Dùng được bằng bàn phím.
- Focus rõ.
- Form có nhãn.
- Thông báo lỗi dễ hiểu và gắn với trường liên quan.
- Dialog và menu có quản lý focus.
- Không chỉ dùng màu để báo trạng thái.
- Tôn trọng tùy chọn giảm chuyển động.
- Nút chạm đủ dễ thao tác.
- Nội dung vẫn đọc được khi phóng to.

Tên miền chamea.vn chỉ là đề xuất, không mặc định thuộc sở hữu thương hiệu.

────────────────────────
21\. RESPONSIVE VÀ HIỆU NĂNG
────────────────────────

Tối ưu cho:

- Laptop.
- Desktop.
- iPad dọc/ngang.
- Điện thoại dọc/ngang.

Kiểm tra các chiều rộng đại diện như 360, 390, 430, 768, 820, 1024, 1280 và 1440 px; đồng thời bảo đảm bố cục thích ứng giữa các mốc.

Không:

- Tràn ngang ngoài ý muốn.
- Chữ quá nhỏ.
- Nút che nội dung.
- Header chiếm quá nhiều diện tích điện thoại.
- Ảnh méo.
- Video vượt khung.
- Bảng hoặc hàng cột làm vỡ bố cục.
- Nội dung nhảy mạnh khi ảnh tải xong.

Ảnh có kích thước dành trước, tải theo nhu cầu và biến thể kích thước phù hợp. Ảnh quan trọng đầu trang được ưu tiên hợp lý.

Video tải có kiểm soát. Không dùng hiệu ứng hoặc thư viện nặng không cần thiết.

Đo hiệu năng thực tế trên môi trường đã triển khai khi có công cụ; không tự công bố điểm hiệu năng chưa đo.

────────────────────────
22\. DỮ LIỆU THẬT VÀ ĐIỀU KIỆN MỞ BÁN
────────────────────────

Tập trung dữ liệu sản phẩm, giá, ảnh, ưu đãi, nội dung, liên hệ, QR và thiết kế vào cấu trúc dễ quản lý, có kiểm tra hợp lệ.

Không bịa:

- Giá thật.
- Tồn kho.
- Lượng bán.
- Đánh giá.
- Chứng nhận.
- Năm hoạt động.
- Chính sách bảo hành.
- Người nổi tiếng sử dụng.
- Phí vận chuyển.
- Thông tin ngân hàng.

Trong môi trường phát triển có thể dùng tên/giá minh họa khi cần, nhưng phải đánh dấu và tách khỏi dữ liệu sản xuất.

Không công khai bán hàng bằng giá minh họa mà khiến khách hiểu là giá chính thức.

Nếu thiếu dữ liệu bắt buộc:

- Hoàn thiện hệ thống kỹ thuật và CMS.
- Giữ nội dung liên quan ở bản nháp hoặc trạng thái chưa mở bán.
- Cung cấp danh sách chính xác thông tin cần bổ sung.
- Không tự điền để vượt qua bước kiểm tra.

Bản chính thức phải có luồng nhận đơn thật. Nếu hạ tầng, cơ sở dữ liệu hoặc tích hợp chưa hoạt động, báo đúng phần chưa hoàn thành, không thay bằng thông báo thành công giả.

────────────────────────
23\. KIỂM THỬ VÀ ĐIỀU KIỆN NGHIỆM THU
────────────────────────

Kiểm thử các luồng thực tế:

A. Khách hàng

- Menu và chuyển trang.
- Tìm kiếm có dấu/không dấu.
- Bộ lọc và sắp xếp.
- Yêu thích.
- Chọn biến thể.
- Thêm/sửa/xóa giỏ hàng.
- Giá nhất quán.
- Giảm giá đúng một lần.
- Phí vận chuyển đúng cấu hình.
- Đặt đơn COD.
- Đặt đơn QR.
- Yêu cầu xác minh chuyển khoản.
- Không tự đánh dấu đã thanh toán.
- Chống đặt trùng.
- Biểu mẫu tư vấn/nhận tin.
- Trạng thái trống, lỗi và mất kết nối.

B. Quản trị

- Đăng nhập và phân quyền.
- Thêm sản phẩm/biến thể.
- Tải ảnh/video.
- Thêm bài viết hoàn chỉnh.
- Chèn ảnh, video và khối sản phẩm vào bài.
- Đổi bố cục 1 cột, 1|1, 1|1|1 và 2|1.
- Kéo thả giữa các cột.
- Chỉnh riêng điện thoại và laptop.
- Lưu nháp không ảnh hưởng bản công khai.
- Xuất bản cập nhật đúng.
- Tải lại vẫn giữ dữ liệu.
- Xung đột nhiều tab.
- Khôi phục phiên bản.
- Xóa tệp đang được tham chiếu.
- Cập nhật QR đúng quyền.
- Xử lý đơn và lịch sử thao tác.

C. Hình thức và nội dung

- Logo nguyên bản.
- Đúng bảng màu.
- Không lỗi dấu.
- Không ảnh hỏng.
- Không sản phẩm nhân bản vô lý.
- Không cắt mất túi.
- Không chữ/nút chồng nhau.
- Không đánh giá hoặc số liệu giả.
- Không xuất hiện phương thức thanh toán thứ ba.
- Không có nội dung bài tập, bảng chấm điểm, SERP Audit, phân công nhóm hoặc nhật ký AI trên cửa hàng.

Không chỉ kiểm tra việc build thành công rồi tuyên bố website không có lỗi.

Nêu rõ đã kiểm thử bằng công cụ nào, trên môi trường nào và phần nào chưa kiểm chứng. Chỉ đánh dấu đạt khi có kết quả thực tế.

────────────────────────
24\. BÀN GIAO
────────────────────────

Bàn giao đầy đủ:

1. Website chạy được.
2. Đường dẫn quản trị.
3. Tài khoản/quyền sở hữu của chủ website.
4. Cơ sở dữ liệu và nơi lưu ảnh/video.
5. Mã nguồn.
6. Hướng dẫn ngắn bằng tiếng Việt cho các thao tác:
   - Sửa banner.
   - Chèn video.
   - Chia 2 hoặc 3 cột.
   - Chỉnh bố cục điện thoại.
   - Thêm sản phẩm.
   - Thêm bài viết.
   - Lưu nháp và xuất bản.
   - Cấu hình COD/QR.
   - Xử lý đơn.
   - Sao lưu và khôi phục.
7. Danh sách cấu hình còn thiếu nếu có.
8. Kết quả kiểm thử và giới hạn còn tồn tại.

Ưu tiên triển khai:

Nhận diện và bố cục → hệ dữ liệu và phân quyền → trang chủ → danh mục/bộ sưu tập → sản phẩm → giỏ hàng/đặt hàng COD–QR → CMS và page builder đầy đủ → responsive → kiểm thử → triển khai.

Chủ động hoàn thiện những quyết định triển khai thông thường. Chỉ yêu cầu bổ sung khi thiếu tài nguyên, dữ liệu kinh doanh, thông tin thanh toán hoặc quyền truy cập thực sự cần thiết.

KẾT QUẢ MONG MUỐN:

Một website CHAMÉA đẹp, có cá tính thương hiệu, vận hành được và dễ tự quản lý. Chủ website có thể tự thay ảnh, video, banner, thêm bài, thêm sản phẩm, chia cột và thiết kế lại cách trình bày của các trang mà không phải nhờ lập trình viên cho từng thay đổi thông thường.

Toàn bộ hệ thống chỉ sử dụng hai phương thức thanh toán: COD và QR.