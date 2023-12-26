from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

HOST_DB = 'localhost'
PORT = 5432
POSTGRES_DB = 'project_al'
POSTGRES_PASSWORD = 'SyncMaster11'
POSTGRES_USER = 'postgres'

SQALCHEMY_DB_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}'

engine = create_engine(
    SQALCHEMY_DB_URL,
    echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
