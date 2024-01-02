from sqlalchemy import select, between
from sqlalchemy.sql.functions import count


#
# def perform_contest_split(db):
#     # разделить на группы рейтинга
#     max_rating_obj = db.scalar(select(Problem).where(Problem.rating >= 800).order_by(Problem.rating.desc()))
#     loop_num = (max_rating_obj.rating - 800) / 300
#     if loop_num % 300 > 0:
#         loop_num = round(loop_num // 300 + 1)
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













    # new_contest = Contest(
    #     name=f'{tag} - {rating} - count3',
    #     rating=rating,
    #     tag_id=tag.id)
    # db.add(new_contest)
    # db.commit()
    # print(new_contest.id)
    # return new_contest.id

    # stmt = (
    #     select(Tag)
    #     .options(
    #         selectinload(Tag.problems),
    #     )
    #     # .func.count(Tag.problems) > 1
    #     .order_by(Tag.id)
    # )
    # pr = db.query(Problem).filter(Problem.id == 3)

    # stmt1 = (
    #     select(Tag)
    #     .options(
    #         selectinload(Tag.problems).joinedload(Problem.tags)
    #     )
    #     .filter(Tag.problems.contains(3))
    #     .order_by(Tag.id)
    # )

    # stmt1 = select([func.count(Problem.project_id)]).\
    #             where(ProjectMember.project_id == cls.id).\
    #             label("member_count")
    #
    # tagsss = db.scalars(stmt1)
    # print(list(tagsss))




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

    # №№№рабочий код добавления контеста и крос присвоения внешних ключей
    #
    # pr10 = db.query(Problem).filter(Problem.id == 10).first()
    # pr20 = db.query(Problem).filter(Problem.id == 20).first()
    # pr30 = db.query(Problem).filter(Problem.id == 30).first()
    # pr40 = db.query(Problem).filter(Problem.id == 40).first()
    # pr50 = db.query(Problem).filter(Problem.id == 50).first()
    # pr60 = db.query(Problem).filter(Problem.id == 60).first()
    # pr70 = db.query(Problem).filter(Problem.id == 70).first()
    # pr80 = db.query(Problem).filter(Problem.id == 80).first()
    # pr90 = db.query(Problem).filter(Problem.id == 90).first()
    # pr100 = db.query(Problem).filter(Problem.id == 100).first()
    #
    #
    # new_contest = Contest(
    #     name='test2',
    #     rating='2222',
    #     problems=[pr10, pr20, pr30, pr40, pr50, pr60, pr70, pr80, pr90, pr100],
    #     tag_id=6
    # )
    # db.add(new_contest)
    #
    # db.commit()
    # print(pr10.contest_id, pr50.contest_id, pr100.contest_id)

    # pr_test = db.query(Problem).filter(Problem.id == 1).first()
    # # pr_test.contest_id = 4 - ok
    # pr_test.contest_id = get_contest(db, pr_test.rating, pr_test.tags)
    # print(pr_test.contest_id)
