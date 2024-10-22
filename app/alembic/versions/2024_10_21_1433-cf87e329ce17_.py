"""empty message

Revision ID: cf87e329ce17
Revises: 6dd69b84f9ec, 99b740a3fa8a
Create Date: 2024-10-21 14:33:54.536606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf87e329ce17'
down_revision: Union[str, None] = ('6dd69b84f9ec', '99b740a3fa8a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
