from db_updater.celery import app


@app.task
def testing_celery():
    print('every hour update DB')
    # results = APIresponse().get_problems(api_url)
    # with SessionLocal() as db:
    #     parser_handler(db, results)
        # return parser_handler(db, results)
