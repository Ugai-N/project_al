from typing import List, Optional

from sqlalchemy import Column, Integer, String, Table, ForeignKey, UniqueConstraint, Constraint
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from utils import get_solvedCount


class Base(DeclarativeBase):
    pass


association_table = Table(
    "association_table",
    Base.metadata,
    Column("problems", ForeignKey("problems.id"), primary_key=True),
    Column("tags", ForeignKey("tags.id"), primary_key=True)
)


class Problem(Base):
    __tablename__ = 'problems'
    __table_args__ = (UniqueConstraint("search_code"),)
    # sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation) ОШИБКА:  повторяющееся значение ключа нарушает ограничение уникальности "problems_search_code_key"
    # DETAIL:  Ключ "(search_code)=(555-A)" уже существует.

    problems_list_all = []

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(300))
    rating: Mapped[Optional[int]]
    tags: Mapped[List['Tag']] = relationship(secondary=association_table, back_populates='problems')
    search_code: Mapped[str] = mapped_column(String(50))
    solvedCount: Mapped[int] = mapped_column(Integer)
    contest_id: Mapped[int] = mapped_column(ForeignKey('contests.id'), nullable=True)
    contest: Mapped['Contest'] = relationship(back_populates="problems")

    def __init__(self, name, rating, tags, search_code, solvedCount, contest_id):
        super().__init__()
        self.search_code = search_code
        self.name = name
        self.rating = rating
        self.tags = tags
        self.solvedCount = solvedCount
        self.contest_id = contest_id
        Problem.problems_list_all.append(self)

    def __repr__(self):
        return f'{self.name} ({self.search_code})'

    # def get_search_code(self, contestId, index):
    #     return '-'.join([str(contestId), index])


    # @property
    # def search_code(self):
    #     """Геттер для приватного атрибута __search_code"""
    #     return self.__search_code

    @classmethod
    def problem_init_handler(cls, db, json_response) -> None:
        """для каждой задачи инициализирует экземпляр Problem"""
        #incomng json file consists of 2 lists:
        problems = json_response['result']['problems']
        statistics = json_response['result']['problemStatistics']

        #check every Problem in a list, form 'search_code', initiate getting tags -> initialize instance Problem
        for p in problems:  # contestId, index, name, rating, tags, solvedCount
            search_code = '-'.join([str(p['contestId']), p['index']])
            try:
                new_problem = cls(
                    search_code=search_code,
                    name=p['name'],
                    rating=p.get('rating'),
                    # tags=p['tags'],
                    tags=Tag.get_tags(db, p['tags']), #checking whether there is such a tag in DB, initialize if not
                    solvedCount=get_solvedCount(statistics, p['contestId'], p['index']), #call utils.get_solvedCount in order to form the attr from the statistics list data
                    contest_id=None
                )
                #add Problem to DB
                db.add(new_problem)
                db.commit()
                print(f'added {new_problem.search_code} to DB')
            #meant to catch excepton if not Unique search_code
            except IntegrityError as error: #  SQLAlchemyError??
                print(f'error {error}')
            except PendingRollbackError as error2:
                print(f'error2 {error2}')


class Tag(Base):
    __tablename__ = 'tags'
    __table_args__ = (UniqueConstraint("name"),)
    # __table_args__ = {'schema': 'DATA'}

    # make an overall list of all tags used - not sure if needed - to delete? can be addressed directly from DB
    tags_list_all = []

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    problems: Mapped[List['Problem']] = relationship(secondary=association_table, back_populates='tags')

    def __init__(self, name):
        super().__init__()
        self.name = name
        Tag.tags_list_all.append(self)

    def __repr__(self):
        return f'{self.name} ({self.id})'

    @classmethod
    def get_tags(cls, db, tags_list):
        """Getting a list of tags for each particular Problem"""
        problem_tags_objs = []
        for item in tags_list:
            """Check every tag for a particular Problem: if no such tag in DB yet -> add to DB + return to Problem as a foreign key"""
            if db.query(cls).filter(cls.name == item).count() == 0:
                new_tag = cls(name=item)
                db.add(new_tag)
                db.commit()
                problem_tags_objs.append(new_tag)
            else:
                """if such tag exsts in DB -> return to Problem as a foreign key"""
                existing_tag = db.query(cls).filter(cls.name == item).first()
                problem_tags_objs.append(existing_tag)
        print(problem_tags_objs)
        return list(set(problem_tags_objs))


class Contest(Base):
    __tablename__ = 'contests'
    # __table_args__ = (Constraint("name"),) -> not more than 10 problems

    # contests_list_all = []

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(300))
    # rating: Mapped[Optional[int]]
    # tag: Mapped[List['Tag']] = relationship(secondary=association_table, back_populates='problems')
    problems: Mapped[List['Problem']] = relationship(back_populates='contest')

    # def __init__(self, rating, tags, search_code, solvedCount):
    #     super().__init__()
    #     self.search_code = search_code
    #     self.name = name
    #     self.rating = rating
    #     self.tags = tags
    #     self.solvedCount = solvedCount
    #     Problem.problems_list_all.append(self)
    #
    # def __repr__(self):
    #     return f'{self.name} ({self.search_code})'