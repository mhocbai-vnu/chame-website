# Triển khai CHAMÉA từ GitHub lên Render

**Trạng thái:** Đây là hướng dẫn cấu hình triển khai, không phải bằng chứng website đã được xuất bản. Dịch vụ Render cần được chủ tài khoản kết nối/tạo và thanh toán theo bảng giá thực tế.

1. Mở [Render Dashboard](https://dashboard.render.com/) và đăng nhập. Kết nối tài khoản GitHub **mhocbai-vnu**.
2. Chọn **New → Blueprint**, chọn repository **mhocbai-vnu/chame-website** (nhánh `main`). Render sẽ đọc `render.yaml` ở thư mục gốc.
3. Xem cấu hình dịch vụ `chamea-boutique` với **gói có phí** và đĩa lưu trữ lâu dài `chamea-data` 5 GB. Không triển khai thành máy chủ miễn phí sử dụng ổ tạm: SQLite và ảnh/video sẽ mất khi dịch vụ được tạo lại.
4. Xác nhận chi phí từ Render và thực hiện kết nối; đợi trạng thái triển khai **Live**. Lấy tên miền `*.onrender.com` thật do Render cấp. Trên trang **Environment**, thêm `PUBLIC_BASE_URL` bằng đúng URL HTTPS này rồi triển khai lại. Mật khẩu và tài khoản ngân hàng **không** nhập trong GitHub.
5. Từ **Shell** của dịch vụ chạy `python -m app.manage create-owner --email EMAIL-CUA-BAN`. Nhập mật khẩu mạnh theo yêu cầu của chương trình và giữ bí mật. Nếu Shell không khả dụng, phải dùng một phương thức chạy lệnh an toàn trong môi trường dịch vụ; không đưa mật khẩu vào commit hoặc log.
6. Vào `https://TEN-MIEN/quan-tri/dang-nhap`. Tải logo, ảnh, video thật; nhập sản phẩm, giá, phí giao hàng, chính sách và cấu hình QR ngân hàng thật. Kiểm thử COD, QR và thao tác quản trị **trước** khi bật nhận đơn.
7. Cấu hình tên miền riêng tùy chọn trong Render; trỏ DNS theo hướng dẫn của Render; cập nhật `PUBLIC_BASE_URL` tương ứng.

## Lưu trữ, sao lưu và giới hạn

- `data/chamea.db` và `data/media/` được lưu vào đĩa `/opt/render/project/src/data` (không đưa lên GitHub). Đĩa này cần được sao lưu ra nơi khác thường xuyên, bao gồm cả các tệp media.
- Thiết kế SQLite/đĩa đơn không phù hợp triển khai nhiều máy chủ/replica; mở rộng quy mô cần chuyển sang PostgreSQL và object storage có chiến lược di chuyển dữ liệu.
- Khởi tạo cấu hình lần đầu ở chế độ **chưa mở bán**. QR, giá sản phẩm, liên hệ và hình ảnh chỉ được kích hoạt khi dữ liệu thật được nhập và xác minh.
- Trạng thái triển khai có mã nguồn không đồng nghĩa đã được kiểm toán an ninh hoặc đạt 100% yêu cầu 2. Trước mở bán phải kiểm thử thực tế, bảo vệ dữ liệu cá nhân, sao lưu và xác minh thanh toán.
- Repo hiện có thể là Public: quản lý quyền riêng tư tại **GitHub → Settings → General → Danger Zone → Change repository visibility** nếu bạn muốn giới hạn người xem mã nguồn.

Nguồn hướng dẫn: https://render.com/docs/blueprint-spec và https://render.com/docs/disks
