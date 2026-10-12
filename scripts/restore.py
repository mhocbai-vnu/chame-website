"""Khôi phục từ backup. DỪNG dịch vụ web trước, tự giữ bản backup cũ."""
import argparse, os, tarfile, shutil, tempfile, sqlite3
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True)
    p.add_argument('--confirm-offline',action='store_true',help='Xác nhận đã dừng server và đã sao lưu dữ liệu hiện tại')
    a=p.parse_args()
    if not a.confirm_offline:raise SystemExit('Dừng server, sao lưu bản hiện tại và chạy lại với --confirm-offline')
    base=Path(__file__).resolve().parent.parent
    url=os.getenv('DATABASE_URL','sqlite:///'+str(base/'data'/'chamea.db'))
    if not url.startswith('sqlite:///'):raise SystemExit('Chỉ hỗ trợ SQLite')
    target=Path(url[10:]);media=Path(os.getenv('MEDIA_DIR',str(base/'data'/'media')))
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp)
        with tarfile.open(a.input,'r:gz') as tf:
            members=tf.getmembers()
            for member in members:
                name=Path(member.name)
                if name.is_absolute() or '..' in name.parts or member.issym() or member.islnk() or not (str(name)=='database.db' or str(name)=='media' or str(name).startswith('media/')):
                    raise SystemExit('Bản backup chứa đường dẫn không hợp lệ')
            tf.extractall(root,filter='data')
        db_src=root/'database.db'
        if not db_src.is_file():raise SystemExit('Thiếu database.db trong bản backup')
        con=sqlite3.connect(db_src)
        if con.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise SystemExit('Database bản backup hỏng')
        con.close()
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(db_src,target)
        if (root/'media').is_dir():
            if media.exists():shutil.rmtree(media)
            shutil.copytree(root/'media',media)
    print('Khôi phục xong. Khởi động lại website và kiểm tra.')

if __name__=='__main__':main()
