import argparse,getpass
from sqlalchemy import select
from .seed import initialize
from .db import SessionLocal
from .models import User
from .core import hash_password

def main():
    p=argparse.ArgumentParser(description='CHAMÉA quản trị hệ thống')
    sub=p.add_subparsers(dest='cmd',required=True)
    sub.add_parser('init')
    s=sub.add_parser('create-owner'); s.add_argument('--email',required=True)
    s=sub.add_parser('reset-password'); s.add_argument('--email',required=True)
    args=p.parse_args(); initialize()
    if args.cmd=='init': print('Khởi tạo cơ sở dữ liệu hoàn tất');return
    password=getpass.getpass('Mật khẩu mới (ít nhất 12 ký tự): ')
    if len(password)<12: raise SystemExit('Mật khẩu quá ngắn')
    with SessionLocal() as db:
        email=args.email.strip().lower()
        user=db.scalar(select(User).where(User.email==email))
        if args.cmd=='create-owner':
            if user: raise SystemExit('Email đã tồn tại; dùng reset-password')
            user=User(email=email,password_hash=hash_password(password),role='owner',active=True)
            db.add(user)
        else:
            if not user: raise SystemExit('Không tìm thấy tài khoản')
            user.password_hash=hash_password(password)
        db.commit()
    print('Hoàn tất. Không có tài khoản/mật khẩu được ghi sẵn trong mã nguồn.')
if __name__=='__main__':main()
