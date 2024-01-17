from random import choice

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.settings import SessionLocal
from models import Problem, ProblemTagAssociation, Contest, Tag
from services.services import get_rating_group


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
        """attaching the problem to the contest with the chosen tag"""
        add_problem_to_contest(db, db_problem, chosen_tag)


def add_problem_to_contest(db, db_problem: Problem, tag_assoc: ProblemTagAssociation) -> Contest:
    """choosing the contest for a problem:
    -> find all contests with appropriate rating level and chosen tag
    -> filter contests which are not filled yet (<10)
    -> if such exists -> attach problem to the first found contest
    -> if such contest does not exist -> create new contest -> attach problem to it"""
    db_problem_rating_level = get_rating_group(db_problem.rating)  # type: int
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
        active_contest = choice(all_available_contests)  # random or all_available_contests[0]
        print(f'***** problem {db_problem} added to existing contest')
    else:
        active_contest = create_contest(db, tag_assoc, len(all_matching_contests), db_problem_rating_level)
        print(f'***** problem {db_problem} lead to creating a new contest')
    db_problem.contest_id = active_contest.id
    db.commit()
    print(f'--->>> problem {db_problem} was added to the contest: {active_contest}')
    return active_contest


def create_contest(db, tag_assoc: ProblemTagAssociation, prev_contest_count: int,
                   db_problem_rating_level: int) -> Contest:
    """creating a new contest. Name contains the number of the contest for the same rating level and tag"""
    new_contest = Contest(
        name=f'{tag_assoc.tag.name} '
             f'({db_problem_rating_level} - {db_problem_rating_level + 300 - 1}) '
             f'- #{prev_contest_count + 1}',
        rating=db_problem_rating_level,
        tag_id=tag_assoc.tag.id
    )
    db.add(new_contest)
    db.commit()
    print(f'--->>> added contest to DB: {new_contest}')
    return new_contest


def get_contests_info() -> tuple:
    """getting the information about the available contests (contests with 10 problems set).
     Returning:
     - all available rating levels
     - all available tags
     - ready contests"""
    with SessionLocal() as user_db:
        stmt = (
            select(Contest)
            .options(
                selectinload(Contest.problems),
            )
            .order_by(Contest.rating)
        )
        all_contests_with_problems = list(user_db.scalars(stmt))
        full_contests = []
        for con in all_contests_with_problems:
            if len([pro for pro in con.problems]) == 10:
                full_contests.append(con)
        # print(f'qty of ready contests: {len(full_contests)}')
        full_contest_tags = list(set([i.tag for i in full_contests]))
        # print(f'qty of available tags of ready contests: {len(full_contest_tags)}')
        full_contest_rating_groups = list(set([i.rating for i in full_contests]))
        return full_contest_rating_groups, full_contest_tags, full_contests


def find_contests_with_rating(rating) -> list:
    """returns tags of ready contests for specific rating level"""
    with SessionLocal() as user_db:
        stmt = (
            select(Contest)
            .options(
                selectinload(Contest.problems),
            )
            .filter(Contest.rating == rating)
        )
        all_contests_with_this_rating = list(user_db.scalars(stmt))

        full_contests = []
        for con in all_contests_with_this_rating:
            if len([pro for pro in con.problems]) == 10:
                full_contests.append(con)

        available_tags = []
        for con in full_contests:
            available_tags.append(con.tag)
        available_tags_set = list(set(available_tags))
        # print(f'available tags: {available_tags_set}')
        return available_tags_set


def find_contests_with_rating_and_tag(tag, rating) -> tuple:
    """chooses random ready contest with chosen tag and rating level
     Returning:
     - randomly chosen contest
     - problems of the chosen contest
     - qty of ready contests that fit the request (tag & rating level)"""
    with SessionLocal() as user_db:
        stmt_tag = (
            select(Tag)
            .filter(Tag.name == tag)
        )
        tag_found = user_db.scalars(stmt_tag).one_or_none()

        stmt = (
            select(Contest)
            .options(
                selectinload(Contest.problems),
                selectinload(Contest.tag)
            )
            .filter(Contest.rating == rating)
            .filter(Contest.tag_id == tag_found.id)
        )
        all_contests_with_this_rating_and_tag = list(user_db.scalars(stmt))

        full_contests = []
        for con in all_contests_with_this_rating_and_tag:
            if len([pro for pro in con.problems]) == 10:
                full_contests.append(con)

        chosen_contest = choice(full_contests)
        problems = []
        for pro in chosen_contest.problems:
            problems.append(pro)
        return chosen_contest, problems, len(full_contests)
