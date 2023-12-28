from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from API.API_manager import APIresponse
from db.db_settings import engine, SessionLocal
from models import Base, Problem, Tag, ProblemTagAssociation, Contest

from utils import get_from_file, save_to_file, get_solvedCount

# --> вынести в конфиги и env
api_url = 'https://codeforces.com/api/problemset.problems'


def search_problem_by_search_code(db, search_code: str) -> Problem | None:
    """search a problem in DB"""
    stmt = (
        select(Problem)
        .filter(Problem.search_code == search_code)
    )
    problem: Problem | None = db.execute(stmt).scalar_one_or_none()
    return problem


def parser_handler(db, json_response) -> None:
    """initiates update:
    checking every row in json,
    getting the problem attrs,
    if problem exists in DB -> updates qty of times the problem was solved,
    if problem does not exist -> creates a new problem in DB -> initiates attachment to the contest"""

    problems = json_response['result']['problems']
    statistics = json_response['result']['problemStatistics']

    for p in problems:
        search_code: str = '-'.join([str(p['contestId']), p['index']])
        solvedCount: int = get_solvedCount(statistics, p['contestId'], p['index'])
        # tags_list = p['tags']
        problem_from_db: Problem | None = search_problem_by_search_code(db, search_code)

        if problem_from_db is None:
            print('\n\n--->>> Problem NOT FOUND. Creating a new one ...')
            tags_after_assoc: list = [ProblemTagAssociation(tag=t) for t in get_tags_to_attach(db, p['tags'])]
            new_problem: Problem = create_problem(
                db,
                name=p.get('name'),
                search_code=search_code,
                rating=p.get('rating') if p.get('rating') is not None else 0,
                solvedCount=solvedCount,
                tags=tags_after_assoc
            )
            """ initiates the problem attachment to the contest """
            choose_tag_for_contest(db, new_problem)
        else:
            """ if the problem exists in DB -> update 'solvedCount' """
            print(f'\n\n--->>> Found problem "{problem_from_db}". Updating ...')
            problem_from_db.solvedCount = solvedCount
            problem_from_db.name = p.get('name')
            db.commit()


def create_problem(db, name: str, search_code: str, rating: int, solvedCount: int, tags: list) -> Problem:
    """creates a new problem in DB"""
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


def create_tag(db, name: str) -> Tag:
    """creates a new Tag in DB"""
    new_tag = Tag(name=name)
    db.add(new_tag)
    db.commit()
    print(f'--->>> added tag to DB: {new_tag}')
    return new_tag


def get_tags_to_attach(db, tags: list) -> list:
    """check every tag for a particular Problem: if no such tag in DB yet -> add new tag to DB.
    Returns a list of Tag instances to the Problem"""
    tag_instances_to_attach = []
    for item in tags:
        """if no such tag in DB yet -> add to DB"""
        if db.query(Tag).filter(Tag.name == item).count() == 0:
            tag_to_attach = create_tag(db, name=item)
        else:
            """if such tag exists in DB -> return to Problem"""
            tag_to_attach = db.query(Tag).filter(Tag.name == item).first()
        tag_instances_to_attach.append(tag_to_attach)
    return list(set(tag_instances_to_attach))


def get_rating_group(db, pro_rating: int) -> str:
    """Basing on the rating of a Problem -> forms a rating level, which is used when grouping problems into contests
    Problem rating starts from 800 (unless is null(0)) and is usually divisible by 100 (800/900/1000 etc).
    Problems are grouped in contests by rating level step of 300 (e.g. 800-1099, 1100-1399 etc)"""
    if pro_rating is None or pro_rating < 800:
        pro_rating_level = 'N/A'
    else:
        # min_rating = db.query(Problem).filter(Problem.rating > 1).order_by(Problem.rating.asc()).first().rating
        rating_level = 800
        while True:
            if rating_level <= pro_rating <= rating_level + 300:
                pro_rating_level = f'{rating_level} - {rating_level + 300 - 1}'
                break
            else:
                rating_level += 300
    return pro_rating_level


def choose_tag_for_contest(db, db_problem: Problem) -> None:
    """Choosing the tag for contest before attaching Problem to contest"""
    chosen_tag = None
    if db_problem.contest_id is None and len(db_problem.tags) != 0:
        if len(db_problem.tags) == 1:
            """if Problem has only 1 tag - this tag is used for attaching to the contest"""
            chosen_tag = db_problem.tags[0]
            print(f'***** only one tag: tag {chosen_tag.tag.name}')
        else:
            """if Problem has more than 1 tag -> less popular tag is chosen 
            (basing of the number of times every tag is mentioned in problems)"""
            min_tag_problems = 10000000000000000000000000000000000000000
            for tag_association in db_problem.tags:    # type: ProblemTagAssociation
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
        """attaching the problem to the contest with the chosen tag"""
        add_problem_to_contest(db, db_problem, chosen_tag)
    # return chosen_tag


def add_problem_to_contest(db, db_problem: Problem, tag_assoc: ProblemTagAssociation) -> Contest:
    """choosing the contest for a problem:
    -> find all contests with appropriate rating level and chosen tag
    -> filter contests which are not filled yet (<10)
    -> if such exists -> attach problem to the first found contest
    -> if such contest does not exist -> create new contest -> attach problem to it"""
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
        active_contest = all_available_contests[0]    # or random
        print(f'***** problem {db_problem} added to existing contest')
    else:
        active_contest = create_contest(db, db_problem, tag_assoc, len(all_matching_contests))
        print(f'***** problem {db_problem} lead to creating a new contest')
    db_problem.contest_id = active_contest.id
    db.commit()
    print(f'--->>> problem {db_problem} was added to the contest: {active_contest}')
    return active_contest


def create_contest(db, db_problem: Problem, tag_assoc: ProblemTagAssociation, prev_contest_count: int) -> Contest:
    """creating a new contest. Name contains the number of the contest for the same rating level and tag"""
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


def main():
    # --> get json file from API or from file:

    results = APIresponse().get_problems(api_url)
    # save_to_file('new_db_file.json', results)
    # results = get_from_file('test_data.json')
    print('--->>> uploaded json file via API request')

    # --> create all tables for models (not needed as tables are created by migrations)
    # Base.metadata.create_all(bind=engine)
    # print('--->>> created tables in DB')

    # --> open DB session
    with SessionLocal() as db:

        # --> launch update of DB
        parser_handler(db, results)


        # --> check how many contests are ready + how many tags are available + how many problems are in DB
        stmt = (
            select(Contest)
            .options(
                selectinload(Contest.problems),
            )
            .order_by(Contest.id)
        )
        all_contests_with_problems = list(db.scalars(stmt))
        full_contests = []
        for con in all_contests_with_problems:
            if len([pro for pro in con.problems]) == 10:
                full_contests.append(con)
        print(f'qty of ready contests: {len(full_contests)}')
        full_contest_tags = [i.tag for i in full_contests]
        print(f'qty of available tags of ready contests: {len(set(full_contest_tags))}')
        stmt = (
            select(Problem)
        )
        all_problems = list(db.scalars(stmt))
        print(f'qty of problems in DB: {len(all_problems)}')

# --> check how many and what problems are in every contest
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

# --> черновое - УДАЛИТЬ
        # Problem().test_methond('dddd')

        # # pro = db.query(Problem).filter(Problem.id == 7).first() --> равнозначно строчке ниже
        # pro = db.scalar(select(Problem).where(Problem.id == 2534))   # type: Problem
        # handle_contest(db, pro)


if __name__ == '__main__':
    main()
