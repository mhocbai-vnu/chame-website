# Xem trước CHAMÉA riêng tư trên GitHub Codespaces

**Mục đích:** mở website thật để kiểm tra giao diện và CMS mà chưa phải mua hosting. Cấu hình `.devcontainer` tự cài Python packages, khởi tạo SQLite và chạy FastAPI. Không tạo dữ liệu sản phẩm, đơn hàng hay ngân hàng giả.

## Khởi chạy chỉ với GitHub

1. Đăng nhập tài khoản GitHub sở hữu repo `mhocbai-vnu/chame-website`.
2. Truy cập **https://codespaces.new/mhocbai-vnu/chame-website?quickstart=1**.
3. Chọn **Create codespace** (hoặc Resume nếu bạn đã có một Codespace); dùng cấu hình mặc định `.devcontainer/devcontainer.json`.
4. Khi khởi tạo xong, mở tab **PORTS**, tìm **8000 – CHAMÉA – xem trước website**, nhấn **Open in Browser**. Trường **Port Visibility** phải là **Private**.
5. Trang chủ: đường dẫn vừa mở. Trang quản trị: thêm `/quan-tri/dang-nhap` vào cuối đường dẫn.

Không cần chạy lệnh cài đặt và khởi động thủ công: `postCreateCommand` + `postStartCommand` làm việc này. Nếu Codespaces báo lỗi khởi động, xem `/tmp/chamea-preview.log` trong Terminal.

## Đăng nhập quản trị

Mở tệp `data/PREVIEW_LOGIN.txt` trong trình soạn thảo của Codespaces. Tệp này chỉ sinh ra bên trong Codespace, được **gitignore**, và chứa mật khẩu ngẫu nhiên, không cố định trong mã nguồn GitHub.

Đây chỉ là tài khoản thử nghiệm. Trước khi triển khai thật, tạo tài khoản chủ website của bạn qua `python -m app.manage create-owner --email ...` và không mang tài khoản preview sang hạ tầng bán hàng.

## An toàn và giới hạn

- Các cổng được GitHub Codespaces chuyển tiếp ở chế độ **Private theo mặc định**, tức phải đăng nhập đúng tài khoản Codespaces để truy cập. Không chuyển cổng 8000 sang Public.
- Repo GitHub hiện được đặt là **Public**, nghĩa là **mã nguồn** vẫn có thể xem công khai, khác với cổng preview Private. Nếu muốn ẩn mã nguồn, tự chuyển repo sang Private trong Settings > General > Danger Zone > Change repository visibility.
- Codespaces không phải hosting chính thức 24/7. Khi Codespace dừng, URL không còn phục vụ trang cho đến khi Resume.
- Dữ liệu thử nghiệm lưu ở `data/chamea.db` và `data/media/` bên trong Codespace. Trước khi xóa Codespace, hãy sao lưu dữ liệu/ảnh.
- Hệ thống mặc định `store_open=false`: chưa mở nhận đơn. Giá, logo, ảnh/video và QR ngân hàng phải do bạn cung cấp; không tự tạo hoặc đăng bán với dữ liệu giả.
- Hạn mức/chi phí Codespaces áp dụng theo tài khoản GitHub của bạn. Dừng Codespace khi không dùng để tránh tiêu hao hạn mức.

## Dừng / xem lại

Mở **https://github.com/codespaces** để Stop, Resume. Có thể quay lại cùng Codespace thay vì tạo một cái mới.

Tài liệu GitHub: https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/setting-up-your-repository/facilitating-quick-creation-and-resumption-of-codespaces và https://docs.github.com/en/codespaces/reference/security-in-github-codespaces
