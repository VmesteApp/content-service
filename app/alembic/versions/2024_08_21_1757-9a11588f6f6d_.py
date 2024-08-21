"""empty message

Revision ID: 9a11588f6f6d
Revises: 688948ddf29c
Create Date: 2024-08-21 17:57:31.589140

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '9a11588f6f6d'
down_revision: Union[str, None] = '688948ddf29c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('application', sa.Column('candidate_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('application', 'candidate_id')
    # ### end Alembic commands ###
