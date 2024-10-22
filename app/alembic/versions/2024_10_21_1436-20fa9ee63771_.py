"""empty message

Revision ID: 20fa9ee63771
Revises: b9434025efcd
Create Date: 2024-10-21 14:36:27.821058

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20fa9ee63771'
down_revision: Union[str, None] = 'b9434025efcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tag', 'decription')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tag', sa.Column('decription', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###