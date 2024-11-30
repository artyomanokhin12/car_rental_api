"""empty message

Revision ID: 47808d54df4b
Revises: b2f9bfae88de
Create Date: 2024-11-27 20:55:46.501658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47808d54df4b'
down_revision: Union[str, None] = 'b2f9bfae88de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model', sa.String(), nullable=False),
    sa.Column('brand', sa.String(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price_per_day', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('locatioon_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_table('cars')
    # ### end Alembic commands ###