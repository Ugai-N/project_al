from typing import List, Optional

from sqlalchemy import Column, Integer, String, Table, ForeignKey, UniqueConstraint, Constraint
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from utils import get_solvedCount


# class Base(DeclarativeBase):
#     pass


# association_table = Table(
#     "association_table",
#     Base.metadata,
#     Column("problems", ForeignKey("problems.id"), primary_key=True),
#     Column("tags", ForeignKey("tags.id"), primary_key=True)
# )
# class ProblemTagAssociation(Base):
#     __tablename__ = 'problem_tag_association'
#     __table_args__ = (
#         UniqueConstraint(
#             'problem_id',
#             'tag_id',
#             name='unique_problem_tag_index',
#         ),
#     )
#
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     problem_id: Mapped[int] = mapped_column(ForeignKey('problems.id'))
#     tag_id: Mapped[int] = mapped_column(ForeignKey('tags.id'))
#
#     #association between ProblemTagAssociation -> Problem
#     problem: Mapped['Problem'] = relationship(back_populates='tags')
#
#     #association between ProblemTagAssociation -> Tag
#     tag: Mapped['Tag'] = relationship(back_populates='problems')



# class Problem(Base):
#     __tablename__ = 'problems'
#     # __table_args__ = (UniqueConstraint("search_code"),)
#     # sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation) ОШИБКА:  повторяющееся значение ключа нарушает ограничение уникальности "problems_search_code_key"
#     # DETAIL:  Ключ "(search_code)=(555-A)" уже существует.
#
#     problems_list_all = []
#
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     name: Mapped[str] = mapped_column(String(300))
#     rating: Mapped[Optional[int]]
#     # tags: Mapped[List['Tag']] = relationship(secondary='problem_tag_association', back_populates='problems')
#     tags: Mapped[List['ProblemTagAssociation']] = relationship(back_populates='problem')
#     search_code: Mapped[str] = mapped_column(String(50), unique=True)
#     solvedCount: Mapped[int] = mapped_column(Integer)
#
#     contest_id: Mapped[int] = mapped_column(ForeignKey('contests.id'), nullable=True)
#     contest: Mapped['Contest'] = relationship(back_populates="problems")
#
#     def __init__(self, name, rating, tags, search_code, solvedCount, contest_id):
#         super().__init__()
#         self.search_code = search_code
#         self.name = name
#         self.rating = rating
#         self.tags = tags
#         self.solvedCount = solvedCount
#         self.contest_id = contest_id
#         Problem.problems_list_all.append(self)
#
#     def __repr__(self):
#         return f'{self.name} ({self.search_code})'
#
#     # def get_search_code(self, contestId, index):
#     #     return '-'.join([str(contestId), index])
#
#     # @property
#     # def search_code(self):
#     #     """Геттер для приватного атрибута __search_code"""
#     #     return self.__search_code
#
#     @classmethod
#     def problem_init_handler(cls, db, json_response) -> None:
#         """для каждой задачи инициализирует экземпляр Problem"""
#         # incomng json file consists of 2 lists:
#         problems = json_response['result']['problems']
#         statistics = json_response['result']['problemStatistics']
#
#         # check every Problem in a list, form 'search_code', initiate getting tags -> initialize instance Problem
#         for p in problems:  # contestId, index, name, rating, tags, solvedCount
#             search_code = '-'.join([str(p['contestId']), p['index']])
#             # get_tags_contests = Tag.get_tags(db, p['tags'])
#             try:
#                 print(p['tags'])
#                 new_problem = cls(
#                     search_code=search_code,
#                     name=p['name'],
#                     rating=p.get('rating'),
#                     # tags=get_tags_contests[0],
#                     tags=Tag.get_tags(db, p['tags']),
#                     # tags=Contest.get_contest(db, p.get('rating'), p['tags'])[0]
#                     # checking whether there is such a tag in DB, initialize new Tag if not
#                     solvedCount=get_solvedCount(statistics, p['contestId'], p['index']),
#                     # call utils.get_solvedCount in order to form the attr from the statistics list data
#                     contest_id=None
#                     # contest_id=get_tags_contests[1],
#                     # contest_id=Contest.get_contest(db, p.get('rating'), p['tags']),
#                     # contest_id = Contest.get_contest(db, p.get('rating'), p['tags'])[0]
#                 )
#                 # add Problem to DB
#                 db.add(new_problem)
#                 db.commit()
#
#                 print(f'added {new_problem.search_code} to DB\n\n')
#             # meant to catch excepton if not Unique search_code
#             except IntegrityError as error:  # SQLAlchemyError??
#                 print(f'error {error}')
#             except PendingRollbackError as error2:
#                 print(f'error2 {error2}')

#
# class Tag(Base):
#     __tablename__ = 'tags'
#     __table_args__ = (UniqueConstraint("name"),)
#     # __table_args__ = {'schema': 'DATA'}
#
#     # make an overall list of all tags used - not sure if needed - to delete? can be addressed directly from DB
#     tags_list_all = []
#
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     name: Mapped[str] = mapped_column(String(100))
#     # problems: Mapped[List['Problem']] = relationship(secondary='problem_tag_association', back_populates='tags')
#     problems: Mapped[List['ProblemTagAssociation']] = relationship(back_populates='tag')
#     contests: Mapped[List['Contest']] = relationship(back_populates="tag")
#
#     def __init__(self, name):
#         super().__init__()
#         self.name = name
#         Tag.tags_list_all.append(self)
#
#     def __repr__(self):
#         return f'{self.name} ({self.id})'
#
#     @classmethod
#     def get_tags(cls, db, tags_list):  ######вот сюда ввернуть потрошение по тегам относительно контеста
#         """Getting a list of tags for each particular Problem"""
#         problem_tags_objs = []
#         for item in tags_list:
#             """Check every tag for a particular Problem: if no such tag in DB yet -> add to DB + return to Problem as a foreign key"""
#             if db.query(cls).filter(cls.name == item).count() == 0:
#                 print('ok1')
#                 new_tag = cls(name=item)
#                 db.add(new_tag)
#                 # db.flush(new_tag)
#                 # db.commit()
#                 problem_tags_objs.append(new_tag)
#             else:
#                 """if such tag exsts in DB -> return to Problem as a foreign key"""
#                 print('ok2')
#                 existing_tag = db.query(cls).filter(cls.name == item).first()
#                 problem_tags_objs.append(existing_tag)
#         print(problem_tags_objs)
#         return list(set(problem_tags_objs))
#         # return list(set(problem_tags_objs)), Contest.get_contest(db, '010101', list(set(problem_tags_objs)))

#
# class Contest(Base):
#     __tablename__ = 'contests'
#     # __table_args__ = (Constraint("name"),) -> not more than 10 problems
#
#     # contests_list_all = []
#
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     name: Mapped[str] = mapped_column(String(300))
#     rating: Mapped[Optional[int]]
#     problems: Mapped[List['Problem']] = relationship(back_populates='contest')
#     tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))
#     tag: Mapped['Tag'] = relationship(back_populates="contests")
#
#     def __init__(self, name, rating, tag_id):
#         super().__init__()
#         self.name = name
#         self.rating = rating
#         self.tag_id = tag_id
#
#     def __repr__(self):
#         return f'{self.name} ({self.rating})'
#
#     @classmethod
#     def get_contest(cls, db, rating, tags_list):
#         """Attaching the contest foreign key for each particular Problem"""
#         # if problem.contest_id is not None:
#         # если таг один
#         print(len(tags_list) == 1)
#         contest_id = 0
#         if len(tags_list) == 1:
#             print(type(tags_list[0]))
#             contest_id = cls.add_to_contest(db, rating, tags_list[0])
#             print(contest_id)
#         else:
#             pass
#         return contest_id
#
#     @classmethod
#     def add_to_contest(cls, db, rating, tag):
#         # tag_instance = db.query(Tag).filter(Tag.name == tag).first()
#         # all_matching_contests = (db.query(Contest)
#         #                         .filter(Contest.tag.id == tag.id & Contest.rating == rating & Contest.problems.count() < 10)
#         #                         ).all()
#         # if all_matching_contests.exists():
#         # # choose any, get id, return contest_id
#         #     return contest_id
#         # else:
#         #     # call classmethod function of Contest -> initiate a new one, get id, return contest_id
#
#         # new_contest = cls(
#         #     name=f'{tag} - {rating} - count3',
#         #     rating=rating,
#         #     tag_id=tag.id)
#
#         new_contest = cls(
#             name=f'{tag.name} - {rating} - count3',
#             rating=rating,
#             tag_id=tag.id
#             # tag_id=Tag.get_tags(db, [tag])
#         )
#
#         db.add(new_contest)
#         db.commit()
#         # return new_contest.id
#         # return [new_contest.id, new_contest.tag_id]
