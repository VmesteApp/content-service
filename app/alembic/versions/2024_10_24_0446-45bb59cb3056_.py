"""empty message

Revision ID: 45bb59cb3056
Revises: 6a6b01bdb263
Create Date: 2024-10-24 04:46:15.525238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45bb59cb3056'
down_revision: Union[str, None] = '6a6b01bdb263'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('full_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('images', 'full_name')
    # ### end Alembic commands ###
