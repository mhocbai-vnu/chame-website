"""Sao lưu SQLite theo API backup + toàn bộ media. Không sao lưu .env hoặc mật khẩu ở dạng plaintext."""
import argparse, sqlite3, tarfile, tempfile, os, shutil
from pathlib import Path
from urllib.parse import unquote

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',required=True,help='Đường dẫn bản sao lưu .tar.gz')
    a=p.parse_args()
    base=Path(__file__).resolve().parent.parent
    url=os.getenv('DATABASE_URL','sqlite:///'+str(base/'data'/'chamea.db'))
    if not url.startswith('sqlite:///'):raise SystemExit('Công cụ backup hỗ trợ SQLite; dùng công cụ DBMS riêng nếu đổi DB')
    source=Path(url[10:])
    media=Path(os.getenv('MEDIA_DIR',str(base/'data'/'media')))
    if not source.is_file():raise SystemExit('Không tìm thấy CSDL: '+str(source))
    output=Path(a.output).resolve();output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        copied=Path(temp)/'database.db'
        src=sqlite3.connect(f'file:{source}?mode=ro',uri=True)
        dest=sqlite3.connect(str(copied))
        with dest:src.backup(dest)
        dest.close();src.close()
        with tarfile.open(output,'w:gz') as archive:
            archive.add(copied,arcname='database.db')
            if media.is_dir():archive.add(media,arcname='media')
    print('Sao lưu hoàn tất:',output)

if __name__=='__main__':main()
