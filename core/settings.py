import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

# API
api_url = 'https://codeforces.com/api/problemset.problems'

# TG
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# celery
broker_url = os.getenv('broker_url')
result_backend = os.getenv('result_backend')

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = False

# DB
HOST_DB = os.getenv('HOST_DB')
PORT = os.getenv('PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
TEST_DB = os.getenv('TEST_DB')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_USER = os.getenv('POSTGRES_USER')

SQALCHEMY_DB_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST_DB}:{PORT}/{POSTGRES_DB}'
TEST_DB_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST_DB}:{PORT}/{TEST_DB}'

engine = create_engine(
    SQALCHEMY_DB_URL,
    # echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
