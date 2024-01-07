from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base
if TYPE_CHECKING:
    from .tag import Tag
    from .problem import Problem


class Contest(Base):
    __tablename__ = 'contests'
    # __table_args__ = (Constraint("name"),) -> not more than 10 problems -> if 0 - cascade cancel

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(300))
    rating: Mapped[int]
    problems: Mapped[List['Problem']] = relationship(back_populates='contest')
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))
    tag: Mapped['Tag'] = relationship(back_populates="contests")

    def __repr__(self):
        return f'{self.name}'
