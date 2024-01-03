"""update contest rating type

Revision ID: 77b987043a30
Revises: fe568c5ff55d
Create Date: 2024-01-03 18:21:20.543363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "77b987043a30"
down_revision: Union[str, None] = "fe568c5ff55d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "contests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=300), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tags.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contests_id"), "contests", ["id"], unique=False)
    op.alter_column("problems", "rating", existing_type=sa.INTEGER(), nullable=False)
    op.create_foreign_key(None, "problems", "contests", ["contest_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "problems", type_="foreignkey")
    op.alter_column("problems", "rating", existing_type=sa.INTEGER(), nullable=True)
    op.drop_index(op.f("ix_contests_id"), table_name="contests")
    op.drop_table("contests")
    # ### end Alembic commands ###
