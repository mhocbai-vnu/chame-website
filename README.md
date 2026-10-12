# CHAMÉA — Bộ mã nguồn website thương mại điện tử độc lập

**Bàn giao phát triển (11/10/2026)**. FastAPI + Jinja2 + vanilla JavaScript + SQLAlchemy + SQLite, không dùng ChatGPT Sites khi chạy. Code frontend, backend, mô hình dữ liệu, CSS/JS, CMS, media upload, đơn hàng và file triển khai đều ở trong ZIP.

Website có thể chạy trên máy riêng hoặc VPS của bạn. **Không được coi là đã mở bán chính thức** khi thiếu tài nguyên và cấu hình thật. Trạng thái ban đầu `store_open=false`, QR chưa khả dụng. Không có tài khoản/mật khẩu quản trị cài sẵn. Không có giá bán, ảnh sản phẩm hay ngân hàng mẫu trên dữ liệu thật.

## 1. Cấu trúc dự án

```text
app/main.py            Trang công khai, sản phẩm, giỏ hàng, checkout, đơn, gợi ý chọn quà, SEO
app/admin.py           Đăng nhập, quản trị, chỉnh nội dung, media, settings, builder API
app/models.py          Bảng CSDL SQLAlchemy
app/core.py            Mật khẩu, phiên, CSRF, giá, ưu đãi, làm sạch nội dung, bố cục
app/seed.py            Khởi tạo không ghi đè dữ liệu hiện có
app/manage.py          CLI tạo owner, thay mật khẩu
app/templates/         HTML công khai và trang quản trị
app/static/            CSS và JavaScript (site/admin/builder)
data/chamea.db         SQLite cài sẵn, không chứa đơn hoặc giá giả
data/media/            Chỗ chứa hình và video chủ website tải lên
scripts/backup.py      Sao lưu database và media
scripts/restore.py     Khôi phục bản sao lưu
tests/test_app.py      Kiểm thử tích hợp tự động
docs/                  Checklist tài nguyên và nhật ký kiểm thử
Dockerfile             Image Python chạy FastAPI
docker-compose.yml     Máy chủ một ứng dụng, dữ liệu lưu ra volume host
```

## 2. Chạy trên máy tính để xem trước

Yêu cầu: Python 3.11+, pip. Tại thư mục chứa README:

```bash
python -m venv .venv
# Linux/Mac: source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python -m app.manage init
python -m app.manage create-owner --email ban@example.com
SESSION_SECURE=false uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Mở `http://127.0.0.1:8000` để xem website và `http://127.0.0.1:8000/quan-tri/dang-nhap` để đăng nhập. Khi tạo chủ website, CLI yêu cầu tự nhập mật khẩu ≥12 ký tự; không ghi vào file cấu hình hay lịch sử câu lệnh. Trên Windows, đặt biến `SESSION_SECURE=false` bằng PowerShell `$env:SESSION_SECURE='false'` trước khi chạy.

## 3. Triển khai hosting riêng

**Cần VPS (hoặc hosting có Python ASGI và quyền cấu hình tiến trình), KHÔNG tương thích nguyên trạng với gói shared hosting chỉ có PHP.** Khuyến nghị Ubuntu 22.04/24.04 có Docker Compose, tên miền và Nginx/Caddy trước cổng 8000. Nếu chỉ thuê shared hosting cPanel không có Python ASGI hoặc Docker, cần nâng cấp gói hosting hoặc chuyển nền tảng có hỗ trợ.

Sao chép thư mục nguồn lên VPS bằng SFTP/SSH. Cấu hình:

```bash
cp .env.example .env
nano .env
# sửa PUBLIC_BASE_URL=https://ten-mien-cua-ban.vn
# DATABASE_URL=sqlite:////srv/chamea/data/chamea.db
# MEDIA_DIR=/srv/chamea/data/media
# SESSION_SECURE=true (bắt buộc khi chạy HTTPS)
mkdir -p data/media
sudo chown -R 10001:10001 data
sudo chmod 700 data
sudo chmod 600 .env
sudo docker compose up -d --build
sudo docker compose exec web python -m app.manage create-owner --email ban@example.com
```

`Dockerfile` chạy bằng user không có quyền root (UID 10001). Docker Compose bind thư mục `./data` của host tới `/srv/chamea/data`, vì vậy **phải có quyền ghi UID 10001**. Container chỉ xuất cổng `127.0.0.1:8000` nên cần reverse proxy công khai HTTPS.

Ví dụ Nginx (sửa tên miền thật):

```nginx
server {
  listen 80;
  server_name ten-mien-cua-ban.vn www.ten-mien-cua-ban.vn;
  client_max_body_size 260m;
  location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 240s;
  }
}
```

Cấp chứng chỉ TLS (Let's Encrypt/Certbot hoặc Caddy), chuyển hướng HTTP→HTTPS, bật backup lịch và giới hạn tấn công tại proxy. Đăng nhập với cookie Secure khi đã có TLS. Không đặt file `.env` hoặc database vào web root. Nếu dùng proxy/tải nhiều tiến trình, cần thiết kế thêm rate-limit phân tán (Redis/WAF), không dựa vào bộ nhớ của một tiến trình. Chạy 1 worker với SQLite là cấu hình mẫu.

Tên miền đề xuất nào cũng phải được đăng ký và xác nhận quyền sở hữu riêng. Không thể xuất bản từ link `*.chatgpt.site` lên hosting mới mà không có mã nguồn/dữ liệu của site cũ.

## 4. Sử dụng trang quản trị

Truy cập: `https://ten-mien-cua-ban.vn/quan-tri/dang-nhap`.

- **Thay ảnh/banner/video:** vào *Thư viện ảnh & video* để tải tệp; sao chép ID. Vào *Cấu hình cửa hàng*, chọn logo, hero desktop/mobile, banner quà hoặc video thương hiệu bằng ID. Trình thiết kế có nút chọn tài nguyên và tải tệp ngay tại bảng thuộc tính khối.
- **Thêm sản phẩm:** *Sản phẩm → Thêm sản phẩm*; điền tên, SKU, mô tả, thuộc tính thật, chọn ảnh từ thư viện bằng thumbnail, sắp ảnh bằng nút ↑ ↓; lưu. Tiếp tục vào *Biến thể và giá* để thêm tên màu/SKU/giá VNĐ và tồn kho (nếu có). Chỉ xuất bản khi xác minh dữ liệu.
- **Thêm bài viết:** *Bài viết → Thêm bài*, lưu, mở *Thiết kế*. Dùng khối H2/H3, văn bản, rich text có nút định dạng, ảnh, video, gallery, sản phẩm liên quan, CTA. *Lưu bản nháp* không thay bản công khai; *Xuất bản* mới làm thay đổi trang khách xem.
- **Chỉnh trang chủ:** *Trang & thiết kế → Trang chủ → Thiết kế*. Thêm Khu vực → Hàng → các cột. Menu bố cục cho phép chọn `1`, `1|1`, `1|1|1`, `1|1|1|1`, `2|1`, `1|2`. Kéo khối qua các cột bằng chuột, hoặc chọn cột và thêm khối trên điện thoại. Tại bảng Thuộc tính, chỉnh chữ, ảnh, video, nền, màu, padding, margin, hình thức hiển thị, ẩn/hiện theo thiết bị.
- **Điều chỉnh điện thoại:** trong builder chọn *Điện thoại*, nhập chiều rộng xem trước và tại thuộc tính hàng đặt số cột muốn hiển thị. Tại thuộc tính khối đặt ẩn/hiện và font riêng theo thiết bị. Laptop và iPad/Tablet có chế độ xem riêng.
- **Khôi phục:** nút *Lịch sử* hiển thị các bản nháp cũ, chọn khôi phục vào bản nháp. Sau khi kiểm tra mới bấm *Xuất bản*. Khôi phục bố cục **không ảnh hưởng đơn hàng**.
- **Cấu hình COD/QR:** *Cấu hình cửa hàng* → phí vận chuyển, ngân hàng, chủ tài khoản, số tài khoản, ảnh QR thật. COD luôn là một trong hai lựa chọn. QR chỉ khả dụng sau khi nhập đủ thông tin, phải kiểm tra QR trên điện thoại trước mở bán. QR trong bản này **là QR cố định**, khách tự nhập số tiền và nội dung chuyển khoản, không có tích hợp xác nhận tiền tự động.
- **Xử lý đơn:** *Đơn hàng*, mở từng đơn để xem snapshot SKU, màu, tổng tiền, ghi chú; thay đổi trạng thái xử lý và thanh toán độc lập. Chỉ chuyển *Đã thanh toán* khi đối chiếu tiền thực tế; thao tác có ghi nhật ký.
- **Quyền nhân sự:** *Tài khoản & phân quyền*, chủ website tạo tài khoản Content hoặc Orders. Chỉ Owner chỉnh cấu hình ngân hàng/giao hàng và quản trị nhân sự.

## 5. Lưu dữ liệu, sao lưu và khôi phục

Cơ sở dữ liệu sử dụng SQLite với WAL, quyền thư mục phù hợp và lưu thật xuống `data/chamea.db`; video/ảnh được lưu riêng trong `data/media`. Các dữ liệu ban đầu được tạo khi DB trống, **không ghi đè nội dung đã chỉnh khi restart**.

Trước nâng cấp hoặc thay hosting, dừng luồng cập nhật dữ liệu quan trọng và sao lưu theo lệnh:

```bash
# Máy local: python scripts/backup.py --output backups/chamea-YYYYMMDD.tar.gz
# Docker chạy từ host:
sudo docker compose exec web python scripts/backup.py --output /srv/chamea/data/backup.tar.gz
```

Dockerfile đã copy thư mục `scripts` vào image. File backup này nằm trong `data/backup.tar.gz`, cần chép thêm ra vùng lưu trữ ngoại vi. Khi khôi phục phải dừng web, giữ bản backup hiện tại trước, sau đó chạy `python scripts/restore.py --input backup.tar.gz --confirm-offline`, khởi động lại và kiểm tra integrity.

Để xuất dữ liệu đơn hàng theo CSV cho hệ thống vận hành riêng, có thể đọc SQLite bằng công cụ DB; phiên bản này chưa có nút export CSV trực tiếp trong quản trị.

## 6. Các cấu hình thực sự còn thiếu

Xem `docs/TAI_NGUYEN_CAN_BO_SUNG.md`. Trong tin nhắn yêu cầu 2 không có ảnh/logo/video/giá/tài khoản ngân hàng thành tệp riêng: chúng **không thể tự động tái sử dụng từ các cuộc trò chuyện trước**. Giữ trống là quyết định nhằm không tạo sản phẩm hoặc dữ liệu kinh doanh giả.

Để mở bán: cung cấp logo và tài nguyên gốc, thêm sản phẩm + biến thể giá thật, nhập liên hệ và phí vận chuyển, xuất bản nội dung chính sách thật, tải QR đã kiểm tra, cấu hình domain+HTTPS, tự kiểm tra giao dịch và vận chuyển. Sau đó chủ website bật *Cho phép nhận đơn hàng* tại Settings. Chỉ khi backend xác nhận lưu DB thì khách mới thấy màn hình đặt hàng thành công.

## 7. Phần nào đã làm và giới hạn còn lại

**Đã có và đã kiểm thử tự động:** điều hướng chính, trang chủ theo bố cục block, danh mục, bộ sưu tập, chi tiết túi, bộ lọc/tìm kiếm cơ bản, cart localStorage (máy chủ tính lại giá), khách đặt hàng không tài khoản, COD/QR cố định, xác nhận QR thủ công, idempotency, form tư vấn/nhận tin lưu DB, quản lý ảnh/video, nội dung/bài viết/pages, thư viện phiên bản nháp, page builder kéo thả khối, mức CSS responsive cơ bản, 3 vai trò và kiểm tra quyền máy chủ, sitemap, chống CSRF admin, kiểm tra loại tệp.

**Giới hạn phải hiểu đúng:**

1. Page builder không phải Elementor hoàn chỉnh: chưa có kéo giãn cột bằng *tay nắm*, pixel-perfect crop preview, tự do lồng layout không giới hạn, mọi thuộc tính responsive, form đa bước, công cụ bố trí header/footer kéo thả. Trang sản phẩm, checkout và giỏ dùng template nghiệp vụ được khóa an toàn; chỉ dữ liệu/nội dung chung đổi qua CMS, chưa thể kéo bố trí mọi thành phần checkout.
2. Menu có thể sửa qua cấu hình JSON, nhưng chưa có UI kéo thả menu con nhiều cấp. Bảng media chưa có quản lý thay thế phiên bản, phát hiện chính xác mọi tham chiếu trong nested JSON, và chưa xuất bulk.
3. Sản phẩm hỗ trợ lọc tên/mã, giá, dáng túi; tìm tiếng Việt không dấu dựa vào slug, **không phải full-text search tiếng Việt chuyên sâu**.
4. Khuyến mãi hỗ trợ một ưu đãi tự động theo phần trăm hoặc mã, thời gian áp dụng; chưa có logic ưu đãi giới hạn theo SKU, dùng một lần, hoặc tổ hợp phức tạp.
5. Chưa có quản lý vận chuyển theo vùng hoặc tích hợp hãng vận chuyển, chỉ phí cố định do owner cấu hình. Không tự đặt miễn phí ship.
6. QR hiện tại là **QR tĩnh do owner tải lên**; chưa có tự động kiểm chứng tài khoản, VietQR động hoặc webhook ngân hàng. Khách bấm xác minh không đủ căn cứ để đánh dấu đã nhận tiền.
7. Chưa tích hợp gửi email thông báo, xác nhận đôi đăng ký nhận tin/hủy đăng ký qua email, job định kỳ để đăng bài hẹn giờ, CAPTCHA hoặc 2FA; cần cấu hình dịch vụ hợp pháp tương ứng.
8. Không có công cụ chuyển dữ liệu tự động từ link ChatGPT Sites: cần export mã nguồn/dữ liệu hoặc cấp quyền thực tế. Không dùng logo/ảnh/video của thương hiệu tham khảo.
9. Chưa đánh giá an ninh độc lập, kiểm thử tải thực tế hoặc chứng nhận tuân thủ; trước giao dịch công khai cần rà soát bổ sung (đặc biệt bảo mật tài khoản, đối soát dòng tiền, dữ liệu cá nhân, đơn có tranh chấp).

**Tóm lại:** Mã nguồn là một ứng dụng thật có thể tự host và lưu đơn trong DB, **không phải prototype tĩnh**. Tuy nhiên vẫn là bản triển khai kỹ thuật cần cấu hình/thẩm định thêm, **chưa đạt 100% mọi tính năng nâng cao trong tài liệu yêu cầu 2**; không tuyên bố đã chuyển dữ liệu cũ hay đã hoạt động trên hosting của bạn.

## 8. Chạy kiểm thử

```bash
pip install -r requirements.txt
python -m pytest -q tests/test_app.py
```

Bài test dùng SQLite và media trong thư mục tạm ngẫu nhiên, **không thêm dữ liệu sản phẩm mẫu vào DB production**. Kết quả kiểm thử/giới hạn trong `docs/NGHIEM_THU.md`.