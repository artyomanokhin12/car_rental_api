"""Add quantity for cars model

Revision ID: dfd0b3928747
Revises: dc30a9561560
Create Date: 2024-12-01 22:25:45.978936

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dfd0b3928747'
down_revision: Union[str, None] = 'dc30a9561560'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cars', sa.Column('quantity', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cars', 'quantity')
    # ### end Alembic commands ###
