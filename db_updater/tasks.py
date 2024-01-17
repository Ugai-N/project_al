from API.API_manager import APIresponse
from core.settings import api_url, SessionLocal
from crud.problem import parser_handler
from db_updater.celery import app


@app.task
def testing_celery():
    print('every hour update DB')


@app.task
def update_db():
    results = APIresponse().get_problems(api_url)
    with SessionLocal() as db:
        parser_handler(db, results)
