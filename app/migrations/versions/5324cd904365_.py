"""empty message

Revision ID: 5324cd904365
Revises: 3136ad60d2f8
Create Date: 2024-11-30 23:46:40.783690

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic_postgresql_enum import TableReference

# revision identifiers, used by Alembic.
revision: str = '5324cd904365'
down_revision: Union[str, None] = '3136ad60d2f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cars', sa.Column('location_id', sa.Integer(), nullable=False))
    op.drop_constraint('cars_locatioon_id_fkey', 'cars', type_='foreignkey')
    op.create_foreign_key(None, 'cars', 'locations', ['location_id'], ['id'], ondelete='SET NULL')
    op.drop_column('cars', 'locatioon_id')
    op.sync_enum_values(
        enum_schema='public',
        enum_name='status',
        new_values=['pending', 'in_process', 'confirmed', 'canceled'],
        affected_columns=[TableReference(table_schema='public', table_name='bookings', column_name='status')],
        enum_values_to_rename=[],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values(
        enum_schema='public',
        enum_name='status',
        new_values=['pending', 'confirmed', 'canceled'],
        affected_columns=[TableReference(table_schema='public', table_name='bookings', column_name='status')],
        enum_values_to_rename=[],
    )
    op.add_column('cars', sa.Column('locatioon_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'cars', type_='foreignkey')
    op.create_foreign_key('cars_locatioon_id_fkey', 'cars', 'locations', ['locatioon_id'], ['id'], ondelete='SET NULL')
    op.drop_column('cars', 'location_id')
    # ### end Alembic commands ###
