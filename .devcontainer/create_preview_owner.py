"""Tạo riêng tài khoản quản trị Codespaces, KHÔNG dùng cho production."""
from pathlib import Path
import secrets
from sqlalchemy import select
from app.db import ROOT, SessionLocal
from app.seed import initialize
from app.core import hash_password
from app.models import User

EMAIL = "preview-owner@chamea.invalid"
CREDENTIALS = ROOT / "data" / "PREVIEW_LOGIN.txt"

def main():
    initialize()
    CREDENTIALS.parent.mkdir(parents=True, exist_ok=True)
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == EMAIL))
        if user is None:
            password = secrets.token_urlsafe(28)
            db.add(User(email=EMAIL, password_hash=hash_password(password), role="owner", active=True))
            db.commit()
            CREDENTIALS.write_text(
                "CHAMÉA — CHỈ DÙNG TRONG GITHUB CODESPACES\n"
                "Trang quản trị: /quan-tri/dang-nhap\n"
                f"Email: {EMAIL}\n"
                f"Mật khẩu: {password}\n"
                "KHÔNG đưa tài khoản này vào website vận hành chính thức.\n",
                encoding="utf-8"
            )
            CREDENTIALS.chmod(0o600)
            print("Đã tạo tài khoản quản trị thử nghiệm và lưu mật khẩu ngẫu nhiên tại data/PREVIEW_LOGIN.txt.")
        elif CREDENTIALS.exists():
            print("Tài khoản Codespaces đã tồn tại. Xem data/PREVIEW_LOGIN.txt để đăng nhập.")
        else:
            print("Tài khoản đã tồn tại nhưng thiếu tệp thông tin. Dùng: python -m app.manage reset-password --email " + EMAIL)

if __name__ == "__main__":
    main()
