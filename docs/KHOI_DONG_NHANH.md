# CHAMÉA — Khởi động nhanh

1. Giải nén ZIP, mở Terminal trong thư mục `CHAMEA_SOURCE`.
2. Cài Python 3.12+, chạy `pip install -r requirements.txt`.
3. Khởi tạo (chỉ khi cần): `python -m app.manage init`.
4. Tạo chủ cửa hàng: `python -m app.manage create-owner --email email-cua-ban@domain.vn`.
5. Chạy local: `uvicorn app.main:app --host 127.0.0.1 --port 8000` (mặc định SESSION_SECURE=false nếu không khai báo).
6. Mở trang `http://127.0.0.1:8000` và admin `http://127.0.0.1:8000/quan-tri/dang-nhap`.
7. Đưa lên VPS theo hướng dẫn Docker/Nginx/HTTPS trong `README.md`. Chưa thể chuyển dữ liệu site cũ nếu không có mã nguồn/backup site cũ.

**Trước mở bán:** Tải logo, ảnh/video thật, tạo sản phẩm và giá thật, điền phí ship, ngân hàng & QR cố định đã xác minh, công bố đủ chính sách, kiểm tra đơn hàng thực tế và bật cửa hàng trong quản trị.

**Giới hạn:** Đơn lưu thật xuống SQLite khi máy chủ hoạt động; thanh toán QR trong bản này chỉ đối soát thủ công. Website chưa thay thế một nền tảng thương mại điện tử đã qua kiểm định vận hành/bảo mật. Chưa hoàn thành toàn bộ tính năng builder nâng cao trong yêu cầu 2. Đọc README để đánh giá trước khi triển khai công khai.
