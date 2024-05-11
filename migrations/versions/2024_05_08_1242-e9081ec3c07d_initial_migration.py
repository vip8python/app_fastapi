"""Initial migration

Revision ID: e9081ec3c07d
Revises: 
Create Date: 2024-05-08 12:42:33.667596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e9081ec3c07d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hotels',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('location', sa.String(), nullable=False),
                    sa.Column('services', sa.JSON(), nullable=True),
                    sa.Column('rooms_quantity', sa.Integer(), nullable=False),
                    sa.Column('image_id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('rooms',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('hotel_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('price', sa.Integer(), nullable=False),
                    sa.Column('services', sa.JSON(), nullable=False),
                    sa.Column('quantity', sa.Integer(), nullable=False),
                    sa.Column('image_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('surname', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('user_id', name='users_pkey'),
                    sa.UniqueConstraint('email', name='users_email_key')
                    )
    op.drop_table('rooms')
    op.drop_table('hotels')
    # ### end Alembic commands ###