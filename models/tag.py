from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base
if TYPE_CHECKING:
    from .contest import Contest
    from .problem_tag import ProblemTagAssociation


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    problems: Mapped[List['ProblemTagAssociation']] = relationship(back_populates='tag')
    contests: Mapped[List['Contest']] = relationship(back_populates="tag")

    def __repr__(self):
        return f'{self.name} ({self.id})'

    def __str__(self):
        return f'{self.name}'
