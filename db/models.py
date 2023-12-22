from typing import List, Optional

from sqlalchemy import Column, Integer, String, Table, ForeignKey, UniqueConstraint
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

    def __init__(self, name, rating, tags, search_code, solvedCount):
        super().__init__()
        self.search_code = search_code
        self.name = name
        self.rating = rating
        self.tags = tags
        self.solvedCount = solvedCount
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
        problems = json_response['result']['problems']
        statistics = json_response['result']['problemStatistics']

        for p in problems:  # contestId, index, name, rating, tags, solvedCount
            search_code = '-'.join([str(p['contestId']), p['index']])
            try:
                new_problem = cls(
                    search_code=search_code,
                    name=p['name'],
                    rating=p.get('rating'),
                    # tags=p['tags'],
                    tags=Tag.get_tags(db, p['tags']),
                    solvedCount=get_solvedCount(statistics, p['contestId'], p['index'])
                )
                db.add(new_problem)
                db.commit()
                print(f'added {new_problem.search_code} to DB')
            except IntegrityError as error:
            # except SQLAlchemyError as err:
                print('error')
            except PendingRollbackError as error2:
            # except SQLAlchemyError as err:
                print('error2')

class Tag(Base):
    __tablename__ = 'tags'
    __table_args__ = (UniqueConstraint("name"),)
    # __table_args__ = {'schema': 'DATA'}

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
        problem_tags_objs = []
        for item in tags_list:
            if db.query(cls).filter(cls.name == item).count() == 0:
                new_tag = cls(name=item)
                db.add(new_tag)
                db.commit()
                problem_tags_objs.append(new_tag)
            else:
                existing_tag = db.query(cls).filter(cls.name == item).first()
                problem_tags_objs.append(existing_tag)
        print(problem_tags_objs)
        return list(set(problem_tags_objs))
