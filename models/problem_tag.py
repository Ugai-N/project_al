from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base
if TYPE_CHECKING:
    from .problem import Problem
    from .tag import Tag


class ProblemTagAssociation(Base):
    __tablename__ = 'problem_tag_association'
    __table_args__ = (
        UniqueConstraint(
            'problem_id',
            'tag_id',
            name='unique_problem_tag_index',
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey('problems.id'))
    tag_id: Mapped[int] = mapped_column(ForeignKey('tags.id'))

    #association between ProblemTagAssociation -> Problem
    problem: Mapped['Problem'] = relationship(back_populates='tags')

    #association between ProblemTagAssociation -> Tag
    tag: Mapped['Tag'] = relationship(back_populates='problems')
