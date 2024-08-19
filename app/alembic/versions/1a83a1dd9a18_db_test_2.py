"""db test 2

Revision ID: 1a83a1dd9a18
Revises: 1315c9da6eb8
Create Date: 2024-08-20 01:14:31.454388

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1a83a1dd9a18'
down_revision: Union[str, None] = '1315c9da6eb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('skills', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('application',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('ix_profile_uu_id', table_name='profile')
    op.drop_column('profile', 'uu_id')
    op.drop_column('profile', 'updated_at')
    op.drop_column('profile', 'created_at')
    op.drop_index('ix_skill_uu_id', table_name='skill')
    op.drop_column('skill', 'uu_id')
    op.drop_column('skill', 'updated_at')
    op.drop_column('skill', 'created_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('skill', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('skill', sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('skill', sa.Column('uu_id', sa.UUID(), autoincrement=False, nullable=False))
    op.create_index('ix_skill_uu_id', 'skill', ['uu_id'], unique=False)
    op.add_column('profile', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('profile', sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('profile', sa.Column('uu_id', sa.UUID(), autoincrement=False, nullable=False))
    op.create_index('ix_profile_uu_id', 'profile', ['uu_id'], unique=False)
    op.drop_table('application')
    op.drop_table('project')
    # ### end Alembic commands ###
