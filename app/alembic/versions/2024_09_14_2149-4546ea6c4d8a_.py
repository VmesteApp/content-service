"""empty message

Revision ID: 4546ea6c4d8a
Revises: ad6f24cfe32d
Create Date: 2024-09-14 21:49:36.035248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4546ea6c4d8a'
down_revision: Union[str, None] = 'ad6f24cfe32d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pulse', sa.Column('category', sa.String(), nullable=True))
    op.add_column('pulse', sa.Column('description', sa.String(), nullable=True))
    op.add_column('pulse', sa.Column('short_description', sa.String(), nullable=True))
    op.drop_column('pulse', 'catrgory')
    op.drop_column('pulse', 'decription')
    op.drop_column('pulse', 'short_decription')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pulse', sa.Column('short_decription', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('pulse', sa.Column('decription', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('pulse', sa.Column('catrgory', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('pulse', 'short_description')
    op.drop_column('pulse', 'description')
    op.drop_column('pulse', 'category')
    # ### end Alembic commands ###