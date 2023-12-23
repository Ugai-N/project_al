import requests
from sqlalchemy import create_engine, text, select, func
from sqlalchemy.dialects.postgresql import psycopg2

from API.API_manager import APIresponse
from db import models
from db.db_settings import engine, SessionLocal
from db.models import Base, Problem, Tag
from services import perform_contest_split

from utils import get_from_file, save_to_file

api_url = 'https://codeforces.com/api/problemset.problems?tags=implementation'


# a = APIresponse()
# a.get_problems(api_url)
# print(len(Problem.problems_list))
# print(Problem.problems_list[35].search_code)
# print(Problem.problems_list[35].solvedCount)


# тестирование из файла а не из АПИ
# results = get_from_file('test_data.json')
#
# Problem.class_init_handler(results)
# results = Problem.problems_list
# save_to_file('new_db_file.json', results)
# print(len(Problem.problems_list))
# print(len(results))
# no_solved = []
# for i in results:
#     if not i.solvedCount:
#         no_solved.append(i)
# print(len(no_solved))


# сколько всего тегов и рейтингов
# results = get_from_file('test_data.json')
#
# Problem.class_init_handler(results)
# results = Problem.problems_list
# tags_list = []
# ratings_list = []
# for i in results:
#     tags_list += i.tags
#     ratings_list.append(i.rating if i.rating != None else 0)
# tags_set = set(tags_list)
# ratings_set = set(ratings_list)
# print(len(tags_set))
# print(tags_set)
# print(len(ratings_set))
# print(sorted(ratings_set))


# 37
# {'data structures', 'sortings', 'dsu', 'expression parsing', 'games', 'matrices', 'chinese remainder theorem', 'meet-in-the-middle', 'flows', 'brute force', '2-sat', 'schedules', 'number theory', 'binary search', 'implementation', 'hashing', 'geometry', 'trees', 'graph matchings', 'string suffix structures', 'dfs and similar', 'divide and conquer', '*special', 'interactive', 'dp', 'shortest paths', 'graphs', 'probabilities', 'greedy', 'bitmasks', 'constructive algorithms', 'strings', 'math', 'two pointers', 'ternary search', 'combinatorics', 'fft'}
# 29
# [0, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500]

#for DB:
# models.Base.metadata.create_all(bind=engine)
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# так устанавливаем подключение к БД
# with engine.connect() as connection:
#     result = connection.execute(text("select * from main_student"))
#     # print(result.all()) # выдает список кортежей
#     print(result.scalars().all()) #очищает от кортежей
#     # for i in result:
#     #     print(i)


# from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
# engine = create_engine(f'postgresql://postgres:SyncMaster11@localhost:5432/ffffffffff', echo = True)
# meta = MetaData()

#создаем пустую таблицу в имеющесйя БД
# students = Table(
#    'students', meta,
#    Column('id', Integer, primary_key = True),
#    Column('name', String),
#    Column('lastname', String),
# )
# meta.create_all(engine)

#create table
# Base.metadata.create_all(bind=engine)
# print('created')

# создаем сессию подключения к бд
# with SessionLocal(autoflush=False, bind=engine) as db:
#     # создаем объект Person для добавления в бд
#     obj = DB_problem_class(name="pro1", rating=38, tags='tagstags', search_code='seeeearch', solvedCount=123)
#     db.add(obj)     # добавляем в бд   или db.add_all([obj1, obj2])
#     db.commit()     # сохраняем изменения
#     print(obj.problem_id)   # можно получить установленный id
# print(len(DB_problem_class.problems_list))
# print(DB_problem_class.problems_list)
# print(DB_problem_class.problems_list[0].search_code)


# вытаскиваем данные из файла
results = get_from_file('test_data.json')
# print('uploaded json file via API request')

#create all tables for models
Base.metadata.create_all(bind=engine)
print('created tables in DB')
# print(Problem.__mapper__.tables)

# открываем сессию с БД
with SessionLocal() as db:
    # потрошим список проблем внутри класс-метода class_init_handler, запоминаем в список list_to_add
    # list_to_add = Problem.problem_init_handler(db, results)

    # pr = db.query(Problem).all()
    # for p in pr:
    #     print(f'{p.name} - {p.tags}')
    #
    #
    # tags = db.query(Tag).all()
    # for t in tags:
    #     print(f'{t.name} - {t.problems}')
    #
    # stmt = (select(Problem).join(Problem.tags).where(Tag.name == 'tag1'))
    # req = db.scalars(stmt).all().count
    # print(req)
    #
    # #splt for contests:
    perform_contest_split(db)
    # db.query(Problem).order_by(Problem.rating)


    # stmt = (select(func.max(Problem.rating)))
    # req = db.scalars(stmt).first()
    # print(req) #3500
    #
    # result = db.execute(text("SELECT rating FROM problems where rating > 1 ORDER BY rating DESC limit 1"))
    # print(result.scalars().first()) #3500
    #
    # all_pr = db.query(Problem).filter(Problem.rating > 1).order_by(Problem.rating.desc()).first()
    # print(all_pr.rating) #3500
    #
    # all_pr = db.scalar(select(Problem).where(Problem.rating > 1).order_by(Problem.rating.desc()))
    # print(all_pr.rating) #3500
