from sqlalchemy import select
from sqlalchemy.orm import selectinload

from crud.contest import choose_tag_for_contest
from crud.tag import get_tags_to_attach
from models import Problem, ProblemTagAssociation
from services.services import get_solvedCount


def search_problem_by_search_code(db, search_code: str):
    """search a problem in DB"""
    stmt = (
        select(Problem)
        .options(
            selectinload(Problem.contest)
        )
        .filter(Problem.search_code == search_code)
    )
    problem: Problem | None = db.execute(stmt).scalar_one_or_none()
    if problem is not None:
        return problem, problem.contest
    else:
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
        problem_from_db: Problem | None = search_problem_by_search_code(db, search_code)[
            0] if search_problem_by_search_code(db, search_code) is not None else None

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
