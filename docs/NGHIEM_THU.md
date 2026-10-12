# Nhật ký kiểm thử — CHAMÉA

## Phạm vi đã chạy trong môi trường xây dựng

- `python -m compileall -q app`: biên dịch cú pháp Python.
- `node --check app/static/site.js`, `admin.js`, `builder.js`: kiểm tra cú pháp JavaScript.
- `python -m pytest -q tests/test_app.py`: 2 bài kiểm thử tự động chứa nhiều bước. Đã đạt trong môi trường sandbox ngày 11/10/2026.
- Kiểm tra giao diện HTML/CSS bằng Chromium/Playwright tại viewport 390 px và 1440 px (ảnh render độc lập từ HTML + CSS). Cả hai không có scroll ngang và không phát sinh lỗi JavaScript ở lần render.
- Smoke test FastAPI TestClient các đường dẫn chính: `/`, `/san-pham`, `/bo-suu-tap`, `/goc-chon-qua`, `/gio-hang`, `/thanh-toan`, `/goi-y-chon-qua`, `/ve-chamea`, `/lien-he`, `/sitemap.xml`.

## Bước được kiểm thử tự động

1. Không thể đặt đơn khi cửa hàng chưa mở bán.
2. Chủ tài khoản đăng nhập và nhận cookie phiên làm việc thực.
3. Gửi API quản trị thiếu CSRF bị từ chối.
4. Định dạng ảnh giả bị từ chối và ảnh JPEG thật được lưu/đọc từ ổ đĩa.
5. Tạo sản phẩm qua form CMS và thêm biến thể có giá/tồn kho.
6. Lưu cấu hình phí vận chuyển và QR trong DB kiểm thử riêng; mở cửa hàng khi đã có điều kiện tối thiểu.
7. Máy chủ tự tính tổng giá cho giỏ sản phẩm, không tin giá client.
8. Từ chối phương thức thanh toán ngoài COD/QR.
9. Lưu đơn COD, tạo biên nhận có token ngẫu nhiên; gửi lại với cùng khóa không tạo đơn trùng.
10. Lưu đơn QR; nút yêu cầu đối soát không chuyển sang "đã thanh toán".
11. Trừ tồn kho sau lưu đơn.
12. Lưu nháp page builder không ảnh hưởng bản công khai; phát hiện xung đột version HTTP 409.
13. Từ chối xóa ảnh đang được tham chiếu.
14. Khử HTML script trong rich text và chặn URL javascript:.

## Chưa thể chứng nhận

- Chưa triển khai lên hosting hoặc tên miền thuộc người dùng; chưa kiểm tra HTTPS, cấu hình DNS, reverse proxy.
- Chưa có logo CHAMÉA dạng tệp gốc, ảnh sản phẩm, poster, video hoặc QR thật trong yêu cầu 2; chưa kiểm tra tính nguyên bản các ảnh.
- Chưa có giá thật, tồn kho thật, thông tin phí vận chuyển/chính sách kinh doanh hoặc thông tin ngân hàng; không thể kiểm thử giao dịch QR hoặc đối soát dòng tiền thật.
- Không có quyền truy cập mã nguồn/cơ sở dữ liệu trang ChatGPT Sites cũ: chưa có chuyển dữ liệu.
- Chưa chạy công cụ đo Lighthouse/Web Vitals hoặc kiểm tra toàn bộ mốc màn hình, thiết bị thật và trình duyệt iOS/Android.
- Chưa thực hiện pentest, thử tải lớn, kịch bản mất kết nối phức tạp, đánh giá tuân thủ pháp luật về thương mại điện tử và dữ liệu cá nhân.
- Builder chưa hỗ trợ kéo thay đổi tỷ lệ bằng tay nắm chuột, crop ảnh WYSIWYG, toàn bộ thành phần checkout cố định, UI khôi phục từ thùng rác bài viết, lịch xuất bản tự động theo worker, phân quyền thao tác cấp trường, MFA, hoặc đồng bộ email marketing. Xem bảng giới hạn README.

**Kết luận:** Bộ mã nguồn và luồng đặt hàng có kiểm thử trong môi trường phát triển; chưa đủ căn cứ gắn nhãn "website đang vận hành chính thức" hoặc "không lỗi" cho hosting thực tế.
