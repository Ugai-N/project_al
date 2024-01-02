from db_updater.celery import app


# api_url = 'https://codeforces.com/api/problemset.problems'
#
# app = Celery('tasks', backend='redis://localhost:6379', broker='redis://localhost:6379')
#
# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'tasks.testing_celery',
#         'schedule': 30.0
#     },
# }
# app.conf.timezone = 'UTC'


@app.task
def testing_celery():
    print('every hour update DB')
    # results = APIresponse().get_problems(api_url)
    # with SessionLocal() as db:
    #     parser_handler(db, results)
        # return parser_handler(db, results)
