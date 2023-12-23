from sqlalchemy import select, between
from sqlalchemy.sql.functions import count

from db.models import Problem, Tag, Contest

#
# def perform_contest_split(db):
#     # разделить на группы рейтинга
#     max_rating_obj = db.scalar(select(Problem).where(Problem.rating >= 800).order_by(Problem.rating.desc()))
#     loop_num = (max_rating_obj.rating - 800) / 300
#     if loop_num % 300 > 0:
#         loop_num = round(loop_num % 300 + 1)
#     rating_level = 800
#     # for i in range(1):
#     for i in range(loop_num):
#         problems_list = db.scalars(select(Problem).where(between(Problem.rating, rating_level, rating_level + 300)).order_by(Problem.rating.asc())).all()
#         #
#         #https://stackoverflow.com/questions/15362149/how-use-alias-in-sqlachemy
#         # single_tag_pro_lst = (db.query(Problem)
#         #                       .join(Tag, Problem.tags)
#         #                       .filter(between(Problem.rating, rating_level, rating_level + 300))
#         #                       .filter(count(Problem.tags) == 1)
#         #                       .order_by(Problem.rating.asc())).all()
#     #     print(single_tag_pro_lst)
#         #отправляем ранжированный по рейтингу список для дальнейшей сортировки по тагам и дроблению на контесты
#         print(rating_level)
#         perform_contest_tag_split(db, problems_list, rating_level)
#         rating_level += 300
#
#
# def perform_contest_tag_split(db, rated_list, rating_level):
#     # в каждой группе рейтинга выделить с одним тагом - поделить на 10 - присвоить атрибут контеста
#     one_tag_list = rated_list.where(Problem.tags.count() == 1)
#     print(one_tag_list)
#     # for problem in rated_list:
#     #     print(f'рейтинг {rating_level}-{rating_level + 300}: {problem.name} | {problem.rating}|{problem.tags}')


    # те что с несколькими тагами - смотреть по каждому из тагов каких меньше чего контестов



def get_contest(db, rating, tags_list):
    # если таг один
    if len(tags_list) == 1:
        add_to_contest(db, rating, tags_list[0])

    #десь еще бы разбить по группам рейтинга?

    #если тег не один
    if len(tags_list) > 1: #else -пустфм вроде не может быть
        min_contests_qty = 100000000000000000000000
        poor_tag = None
        for tag in tags_list:
            tag_contests_qty = (db.query(Contest).filter(Contest.tag == tag & Contest.rating == rating)
                                 ).count()
            if tag_contests_qty < min_contests_qty:
                min_contests_qt = tag_contests_qty
                poor_tag = tag
                return add_to_contest(db, rating, poor_tag)

def add_to_contest(db, rating, tag):
    all_similar_contests = (db.query(Contest)
                            .filter(Contest.tag.id == tag.id & Contest.rating == rating & Contest.problems < 10)
                            ).all()
    if all_similar_contests.exists():
    # choose any, get id, return contest_id
        return contest_id
    else:
        # call classmethod function of Contest -> initiate a new one, get id, return contest_id
        return contest_id
