"""Added2

Revision ID: fe568c5ff55d
Revises: c45bc6bd8e49
Create Date: 2023-12-28 18:45:06.762210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fe568c5ff55d"
down_revision: Union[str, None] = "c45bc6bd8e49"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_tags_id"), "tags", ["id"], unique=False)
    op.create_table(
        "contests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=300), nullable=False),
        sa.Column("rating", sa.String(), nullable=True),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tags.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contests_id"), "contests", ["id"], unique=False)
    op.create_table(
        "problems",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=300), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column("search_code", sa.String(length=50), nullable=False),
        sa.Column("solvedCount", sa.Integer(), nullable=False),
        sa.Column("contest_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["contest_id"],
            ["contests.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("search_code"),
    )
    op.create_index(op.f("ix_problems_id"), "problems", ["id"], unique=False)
    op.create_table(
        "problem_tag_association",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("problem_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["problem_id"],
            ["problems.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tags.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("problem_id", "tag_id", name="unique_problem_tag_index"),
    )
    op.create_index(
        op.f("ix_problem_tag_association_id"),
        "problem_tag_association",
        ["id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_problem_tag_association_id"), table_name="problem_tag_association"
    )
    op.drop_table("problem_tag_association")
    op.drop_index(op.f("ix_problems_id"), table_name="problems")
    op.drop_table("problems")
    op.drop_index(op.f("ix_contests_id"), table_name="contests")
    op.drop_table("contests")
    op.drop_index(op.f("ix_tags_id"), table_name="tags")
    op.drop_table("tags")
    # ### end Alembic commands ###
