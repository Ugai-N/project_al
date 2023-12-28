from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from API.API_manager import APIresponse
from db.db_settings import engine, SessionLocal
from models import Base, Problem, Tag, ProblemTagAssociation, Contest

from utils import get_from_file, save_to_file, get_solvedCount

api_url = 'https://codeforces.com/api/problemset.problems?tags=implementation'


def search_problem_by_search_code(db, search_code):
    stmt = (
        select(Problem)
        .filter(Problem.search_code == search_code)
    )
    problem: Problem | None = db.execute(stmt).scalar_one_or_none()
    return problem


def parser_handler(db, json_response):
    problems = json_response['result']['problems']
    statistics = json_response['result']['problemStatistics']

    # check every Problem in a list, form 'search_code', form 'solvedCount' -> initialize instance Problem
    for p in problems:  # contestId, index, name, rating, tags, solvedCount
        search_code = '-'.join([str(p['contestId']), p['index']])
        solvedCount = get_solvedCount(statistics, p['contestId'], p['index'])
        problem_from_db = search_problem_by_search_code(db, search_code)
        if problem_from_db is None:
            print('\n\n--->>> Problem NOT FOUND. Creating a new one ...')
            tags_after_assoc = [ProblemTagAssociation(tag=t) for t in attach_tag(db, p['tags'])]
            new_problem = create_problem(
                db,
                name=p.get('name'),
                search_code=search_code,
                rating=p.get('rating') if p.get('rating') is not None else 0,
                solvedCount=solvedCount,
                tags=tags_after_assoc
            )
            # attach_tag(db, new_problem, p['tags'])
            handle_contest(db, new_problem)
        else:
            print(f'\n\n--->>> Found problem "{problem_from_db}". Updating ...')
            problem_from_db.solvedCount = solvedCount
            db.commit()


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
    print(f'\n--->>> added problem to DB: {new_problem}')
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


def get_rating_group(db, pro_rating):
    if pro_rating is None or pro_rating < 800:
        pro_rating_level = 'N/A'
    else:
        # min_rating = db.query(Problem).filter(Problem.rating > 1).order_by(Problem.rating.asc()).first().rating
        rating_level = 800
        while True:
            # print(f'from {rating_level} to {rating_level + 299}')
            if rating_level <= pro_rating <= rating_level + 300:
                pro_rating_level = f'{rating_level} - {rating_level + 300 - 1}'
                break
            else:
                rating_level += 300
    return pro_rating_level

def handle_contest(db, db_problem):
    chosen_tag = None
    if db_problem.contest_id is None:
    # если таг один
        if len(db_problem.tags) == 1:
            # print(f'*******************{db_problem.tags[0]}')
            chosen_tag = db_problem.tags[0]
            print(f'***** only one tag: tag {chosen_tag.tag.name}')
    #если таг не один
        else:
            #check popularity of ech tag in problem.tags
            min_tag_problems = 10000000000000000000000000000000000000000
            for tag_association in db_problem.tags:  # type: ProblemTagAssociation
                stmt = (
                    select(Problem)
                    .join(ProblemTagAssociation.problem)
                    .options(
                        selectinload(Problem.tags)
                    )
                    .filter(ProblemTagAssociation.tag == tag_association.tag)
                )
                pros_with_tag_qty = len(list(db.scalars(stmt)))
                print(f'***** tag {tag_association.tag.name} has {pros_with_tag_qty} pros')
                if pros_with_tag_qty < min_tag_problems:
                    min_tag_problems = pros_with_tag_qty
                    chosen_tag = tag_association
            print(f'***** tag {chosen_tag.tag.name} was chosen for contest')
                # print(f'tag {tag_association.tag} has {pros_qty} pros:')
                # for pr in pros_with_tag:
                #     print(f'[+] {pr.name}({pr.id})')
        add_problem_to_contest(db, db_problem, chosen_tag)
    return chosen_tag

    # десь еще бы разбить по группам рейтинга?

def add_problem_to_contest(db, db_problem, tag_assoc): #tag not list, 1 instance of Problem_tag_association
    db_problem_rating_level = get_rating_group(db, db_problem.rating)
    stmt = (
        select(Contest)
        .filter(Contest.tag_id == tag_assoc.tag.id)
        .filter(Contest.rating == db_problem_rating_level)
        .order_by(Contest.id)
    )
    all_matching_contests = list(db.scalars(stmt))
    all_available_contests = []

    for con in all_matching_contests:
        if len([pro for pro in con.problems]) < 10:
            all_available_contests.append(con)
    if len(all_available_contests) != 0:
        active_contest = all_available_contests[0] #or random
        print(f'***** problem {db_problem} added to existing contest')
    else:
        active_contest = create_contest(db, db_problem, tag_assoc, len(all_matching_contests))
        print(f'***** problem {db_problem} lead to creating a new contest')
    db_problem.contest_id = active_contest.id
    db.commit()
    print(f'--->>> problem {db_problem} was added to the contest: {active_contest}')
    return active_contest


def create_contest(db, db_problem, tag_assoc, prev_contest_count):
    db_problem_rating_level = get_rating_group(db, db_problem.rating)
    new_contest = Contest(
        name=f'{tag_assoc.tag.name} ({db_problem_rating_level}) - #{prev_contest_count + 1}',
        rating=db_problem_rating_level,
        tag_id=tag_assoc.tag.id
    )
    db.add(new_contest)
    db.commit()
    print(f'--->>> added contest to DB: {new_contest}')
    return new_contest


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
    results = get_from_file('test_one.json')
    print('--->>> uploaded json file via API request')

    # create all tables for models
    # Base.metadata.create_all(bind=engine)
    # print('--->>> created tables in DB')

    # открываем сессию с БД
    with SessionLocal() as db:
        # print(results)
        # parser_handler(db, results)
        # pr = search_problem_by_search_code(db, '22222-B')
        # pr = search_problem_by_search_code(db, '33333333333-A')
        # print(pr)

        # parser_handler(db, results)
        Problem().test_methond('dddd')


        # # pro = db.query(Problem).filter(Problem.id == 7).first() --> равнозначно строчке ниже
        # pro = db.scalar(select(Problem).where(Problem.id == 2534))   # type: Problem
        # handle_contest(db, pro)


###--> посмотреть сколько и какие задачи в контестах
        # stmt = (
        #     select(Contest)
        #     .options(
        #         selectinload(Contest.problems),
        #     )
        #     .order_by(Contest.id)
        # )
        # all_contests_with_problems = list(db.scalars(stmt))
        # for con in all_contests_with_problems:
        #     print(f'\n{con}')
        #     for pr in con.problems:
        #         print(f'@{pr}')





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
