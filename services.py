from sqlalchemy import select, between
from sqlalchemy.sql.functions import count

from db.models import Problem, Tag


def perform_contest_split(db):
    # разделить на группы рейтинга
    max_rating_obj = db.scalar(select(Problem).where(Problem.rating >= 800).order_by(Problem.rating.desc()))
    loop_num = (max_rating_obj.rating - 800) / 300
    if loop_num % 300 > 0:
        loop_num = round(loop_num % 300 + 1)
    rating_level = 800
    # for i in range(1):
    for i in range(loop_num):
        problems_list = db.scalars(select(Problem).where(between(Problem.rating, rating_level, rating_level + 300)).order_by(Problem.rating.asc())).all()
        #
        #https://stackoverflow.com/questions/15362149/how-use-alias-in-sqlachemy
        # single_tag_pro_lst = (db.query(Problem)
        #                       .join(Tag, Problem.tags)
        #                       .filter(between(Problem.rating, rating_level, rating_level + 300))
        #                       .filter(count(Problem.tags) == 1)
        #                       .order_by(Problem.rating.asc())).all()
    #     print(single_tag_pro_lst)
        #отправляем ранжированный по рейтингу список для дальнейшей сортировки по тагам и дроблению на контесты
        print(rating_level)
        perform_contest_tag_split(db, problems_list, rating_level)
        rating_level += 300


def perform_contest_tag_split(db, rated_list, rating_level):
    # в каждой группе рейтинга выделить с одним тагом - поделить на 10 - присвоить атрибут контеста
    one_tag_list = rated_list.where(Problem.tags.count() == 1)
    print(one_tag_list)
    # for problem in rated_list:
    #     print(f'рейтинг {rating_level}-{rating_level + 300}: {problem.name} | {problem.rating}|{problem.tags}')




    # те что с несколькими тагами - смотреть по каждому из тагов каких меньше чего контестов