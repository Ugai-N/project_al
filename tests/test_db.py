from crud.contest import *
from crud.problem import *
from crud.tag import *
from models import *


class TestTag:
    def test_tag_create(self, db_session):
        """testing 'create_tag' function"""
        tag1 = create_tag(db_session, 'tag1')
        stmt = (select(Tag))
        tags = list(db_session.scalars(stmt))
        assert len(tags) == 1
        assert tag1.name == 'tag1'

    def test_ignore_creation_if_exists(self, db_session):
        """testing 'get_tags_to_attach' function if tag already exists in DB"""
        get_tags_to_attach(db_session, ["tag1"])
        stmt = (select(Tag))
        tags = list(db_session.scalars(stmt))
        assert len(tags) == 1  # qty of Tags in DB didn't change -> see 'test_tag_create'

    def test_create_if_not_in_db(self, db_session):
        """testing 'get_tags_to_attach' function if tag is not yet in DB"""
        get_tags_to_attach(db_session, ["tag1", "tag2", "tag3"])
        stmt = (select(Tag))
        tags = list(db_session.scalars(stmt))
        assert len(tags) == 3  # qty of Tags in DB changed form 1 to 3 -> see 'test_tag_create'


class TestProblem:
    def test_problem_create(self, db_session):
        """testing 'create_problem' function"""
        tag0 = create_tag(db_session, 'tag0')
        pro = create_problem(db_session, name='TEST0', search_code="000-A", rating=800, solvedCount=1,
                             tags=[ProblemTagAssociation(tag=tag0)])
        stmt = (select(Problem))
        pros = list(db_session.scalars(stmt))
        assert pro.name == 'TEST0'
        assert len(pros) == 1

    def test_load_new_problems(self, db_session, json_problems):
        """testing 'parser_handler' function in cases when Problem is not found in DB -> create new"""
        parser_handler(db_session, json_problems)
        stmt = (select(Problem))
        pros = list(db_session.scalars(stmt))
        assert len(pros) == 4  # 3 Problems are new, 1 left from 'test_problem_create'
        assert db_session.scalars(stmt.filter(Problem.search_code == "11111111111-A")).first().name == 'TEST1'
        assert db_session.scalars(stmt.filter(Problem.search_code == "222222222222-B")).first().solvedCount == 22

    def test_update_existing_problem(self, db_session, json_problems_updated):
        """testing 'parser_handler' function in cases when Problem is found in DB -> update"""
        parser_handler(db_session, json_problems_updated)
        stmt = (select(Problem))
        pros = list(db_session.scalars(stmt))
        assert len(pros) == 4  # 3 Problems are new, 1 left from 'test_problem_create'
        assert db_session.scalars(stmt.filter(Problem.search_code == "11111111111-A")).first().name == 'TEST1_upd'
        assert db_session.scalars(stmt.filter(Problem.search_code == "222222222222-B")).first().solvedCount == 2222

    def test_search_problem_by_search_code(self, db_session):
        """testing 'search_problem_by_search_code' function, when Problem exists"""
        result = search_problem_by_search_code(db_session, '11111111111-A')
        assert len(result) == 2
        assert isinstance(result[1], Contest)
        assert result[0].name == 'TEST1_upd'

    def test_no_problem_by_search_code(self, db_session):
        """testing 'search_problem_by_search_code' function, when Problem doesn't exist"""
        result = search_problem_by_search_code(db_session, '9999-A')
        assert result is None

    def test_problem_tags(self, db_session):
        """testing that all Tags have been associated with the Problem"""
        stmt = (select(Problem)
                .filter(Problem.search_code == "33333333333-C"))
        tags = db_session.scalars(stmt).first().tags
        assert len(tags) == 3
        assert isinstance(tags[0], ProblemTagAssociation)

    def test_tag_problems(self, db_session):
        """testing that all Problems have been associated with the Tag"""

        def get_pros_with_tag(tag_name):
            stmt_tag = (
                select(Tag)
                .filter(Tag.name == tag_name)
            )
            tag_id = db_session.scalars(stmt_tag).one_or_none().id
            stmt_pros = (
                select(Problem)
                .join(ProblemTagAssociation.problem)
                .options(
                    selectinload(Problem.tags)
                )
                .filter(ProblemTagAssociation.tag_id == tag_id)
            )
            return list(db_session.scalars(stmt_pros))

        assert len(get_pros_with_tag('tag1')) == 3
        assert len(get_pros_with_tag('tag2')) == 1
        assert get_pros_with_tag('tag2')[0].search_code == "33333333333-C"


class TestCreateContest:
    def test_create_contest(self, db_session):
        """testing 'create_contest' function. Note: contest has not been associated with Problem yet"""
        tag0 = create_tag(db_session, 'tag0')
        pro = create_problem(db_session, name='TEST0', search_code="000-A", rating=800, solvedCount=1,
                             tags=[ProblemTagAssociation(tag=tag0)])
        cont = create_contest(db_session, [t for t in pro.tags][0], 0, pro.rating)
        assert cont.name == 'tag0 (800 - 1099) - #1'
        assert pro.contest_id is None


class TestAttachContest:
    def test_choose_tag_if_1(self, db_session):
        """testing 'choose_tag_for_contest' function in cases when Problem has only 1 Tag.
        Note: Contest gets associated with Problem"""
        tag4 = create_tag(db_session, 'tag4')
        pro = create_problem(db_session, name='TEST4', search_code="444-A", rating=800, solvedCount=1,
                             tags=[ProblemTagAssociation(tag=tag4)])
        choose_tag_for_contest(db_session, pro)
        contest_with_thi_pro = search_problem_by_search_code(db_session, '444-A')[1]

        assert contest_with_thi_pro.tag.name == 'tag4'
        assert contest_with_thi_pro.tag_id == pro.tags[0].id
        assert contest_with_thi_pro.id == pro.contest_id

    def test_choose_tag_if_many(self, db_session):
        """testing 'choose_tag_for_contest' function in cases when Problem has more than 1 Tag.
        Note: less popular Tag is chosen"""
        tag4 = db_session.scalars(select(Tag).filter(Tag.name == 'tag4')).one_or_none()
        # tag4 was mentioned once in problem within 'test_choose_tag_if_1'
        tag5 = create_tag(db_session, 'tag5')
        # tag5 is new and less popular -> is to be chosen for attaching to the contest
        pro = create_problem(db_session, name='TEST5', search_code="555-A", rating=1000, solvedCount=5,
                             tags=[ProblemTagAssociation(tag=t) for t in [tag4, tag5]])
        choose_tag_for_contest(db_session, pro)
        contest_with_thi_pro = search_problem_by_search_code(db_session, '555-A')[1]
        assert contest_with_thi_pro.tag.name == 'tag5'
        assert contest_with_thi_pro.tag_id == pro.tags[0].id
        assert contest_with_thi_pro.id == pro.contest_id


class TestProblemsInContest:
    def test_exceed_10_pro(self, db_session, json_problems_11_items):
        """testing that if the Contest is full (has 10 Problems of the same rating level and tag) ->
        -> a new Contest is initialized"""
        parser_handler(db_session, json_problems_11_items)
        stmt = (select(Contest))
        cons = db_session.scalars(stmt)
        con1 = db_session.scalars(stmt.filter(Contest.name == 'tag11 (800 - 1099) - #1')).one_or_none()
        con2 = db_session.scalars(stmt.filter(Contest.name == 'tag11 (800 - 1099) - #2')).one_or_none()
        assert len(list(cons)) == 2
        assert len(con1.problems) == 10
        assert len(con2.problems) == 1

    def test_same_tag_other_rating(self, db_session, json_problems_another_rating):
        """testing that if the Contest has different rating level, but the same tag -> a new Contest is initialized"""
        parser_handler(db_session, json_problems_another_rating)
        stmt = (select(Contest))
        cons = db_session.scalars(stmt)
        con = db_session.scalars(stmt.filter(Contest.rating == 1100)).one_or_none()
        assert len(list(cons)) == 3    # added 1 comparatively to results seen in 'test_exceed_10_pro'
        assert con.name == 'tag11 (1100 - 1399) - #1'


class TestServices:
    def test_get_rating_group(self):
        """testing 'choose_tag_for_contest' function"""
        assert get_rating_group(0) == 0
        assert get_rating_group(800) == 800
        assert get_rating_group(900) == 800
        assert get_rating_group(1000) == 800
        assert get_rating_group(1099) == 800
        assert get_rating_group(1100) == 1100
        assert get_rating_group(24000) == 23900

# @pytest.mark.usefixtures("set_up_db")
