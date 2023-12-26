from sqlalchemy import select
from sqlalchemy.orm import selectinload

from API.API_manager import APIresponse
from db.db_settings import engine, SessionLocal
from models import Base, Problem, Tag, ProblemTagAssociation

from utils import get_from_file, save_to_file, get_solvedCount

api_url = 'https://codeforces.com/api/problemset.problems?tags=implementation'


def create_problem(db, name: str, search_code: str, rating: int, solvedCount: int, tags):
    new_problem = Problem(
        name=name,
        search_code=search_code,
        rating=rating,
        solvedCount=solvedCount,
        tags=tags
    )
    db.add(new_problem)
    db.commit()
    print(f'--->>> added problem to DB: {new_problem}')
    return new_problem


def parser_handler(db, json_response):
    problems = json_response['result']['problems']
    statistics = json_response['result']['problemStatistics']

    # check every Problem in a list, form 'search_code', form 'solvedCount' -> initialize instance Problem
    for p in problems:  # contestId, index, name, rating, tags, solvedCount
        search_code = '-'.join([str(p['contestId']), p['index']])
        solvedCount = get_solvedCount(statistics, p['contestId'], p['index'])
        tags_after_assoc = [ProblemTagAssociation(tag=t) for t in attach_tag(db, p['tags'])]

        new_problem = create_problem(
            db,
            name=p.get('name'),
            search_code=search_code,
            rating=p.get('rating'),
            solvedCount=solvedCount,
            tags=tags_after_assoc
        )
        # attach_tag(db, new_problem, p['tags'])
        return new_problem


def create_tag(db, name: str):
    new_tag = Tag(name=name)
    db.add(new_tag)
    db.commit()
    print(f'--->>> added tag to DB: {new_tag}')
    return new_tag


def attach_tag(db, tags: list):
    tag_instances_to_attach = []
    for item in tags:
        """Check every tag for a particular Problem: if no such tag in DB yet -> add to DB 
        + return to Problem as a foreign key"""
        if db.query(Tag).filter(Tag.name == item).count() == 0:
            tag_to_attach = create_tag(db, name=item)
        else:
            """if such tag exsts in DB -> return to Problem as a foreign key"""
            tag_to_attach = db.query(Tag).filter(Tag.name == item).first()
        # problem.tags.append(ProblemTagAssociation(tag=tag_to_attach))
        # problem_tag_association = ProblemTagAssociation(tag=tag_to_attach)
        # db.add(problem_tag_association)
        tag_instances_to_attach.append(tag_to_attach)
    # db.commit()
    # return problem
    return list(set(tag_instances_to_attach))


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


# create table
# Base.metadata.create_all(bind=engine)
# print('created')


# вытаскиваем данные из файла
def main():
    results = get_from_file('test_data.json')
    print('--->>> uploaded json file via API request')

    # create all tables for models
    Base.metadata.create_all(bind=engine)
    print('--->>> created tables in DB')

    # открываем сессию с БД
    with SessionLocal() as db:
        parser_handler(db, results)



if __name__ == '__main__':
    main()

    # # pr = db.query(Problem).filter(Problem.id >= 2544).all()
    # pr = db.query(Problem).all()
    # for p in pr:
    #     print(f'{p.name} - {p.tags} - {p.contest_id}')
    # # con = db.query(Tag).filter(Tag.id >= 38).all()
    # con = db.query(Tag).all()
    # for c in con:
    #     print(f'{c.name} - {c.contests}')
    # #
    # #
    # tags = db.query(Tag).all()
    # for t in tags:
    #     print(f'{t.name} - {t.problems}')
    #
    # stmt = (select(Problem).join(Problem.tags).where(Tag.name == 'tag1'))
    # req = db.scalars(stmt).all().count
    # print(req)
    #
    # #splt for contests:
    # perform_contest_split(db)
    # db.query(Problem).order_by(Problem.rating)
    # db.refresh(Contest)
