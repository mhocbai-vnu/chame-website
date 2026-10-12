import os
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

ROOT = Path(__file__).resolve().parent.parent
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///' + str(ROOT / 'data' / 'chamea.db'))
if DATABASE_URL.startswith('sqlite:'):
    dbfile = DATABASE_URL.removeprefix('sqlite:///')
    Path(dbfile).parent.mkdir(parents=True, exist_ok=True)
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False, 'timeout': 30} if DATABASE_URL.startswith('sqlite:') else {}, pool_pre_ping=True)
if DATABASE_URL.startswith('sqlite:'):
    @event.listens_for(engine, 'connect')
    def sqlite_config(con, record):
        cur = con.cursor()
        cur.execute('PRAGMA foreign_keys=ON')
        cur.execute('PRAGMA journal_mode=WAL')
        cur.execute('PRAGMA busy_timeout=30000')
        cur.close()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db:
        yield db
