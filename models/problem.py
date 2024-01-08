from typing import List, TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from .contest import Contest
    from .problem_tag import ProblemTagAssociation


class Problem(Base):
    __tablename__ = 'problems'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(300))
    rating: Mapped[int]
    tags: Mapped[List['ProblemTagAssociation']] = relationship(back_populates='problem')
    search_code: Mapped[str] = mapped_column(String(50), unique=True)
    solvedCount: Mapped[int] = mapped_column(Integer)

    contest_id: Mapped[int] = mapped_column(ForeignKey('contests.id'), nullable=True)
    contest: Mapped['Contest'] = relationship(back_populates="problems")

    def __repr__(self):
        return f'{self.name} ({self.search_code})'

    # @classmethod
    # def test_methond(cls, test):
    #     print(test)
