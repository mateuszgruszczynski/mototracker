"""add_mileage_to_to_saved_search

Revision ID: e8f0564be245
Revises: 0ca7a4825a02
Create Date: 2026-05-16 12:26:17.641445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8f0564be245'
down_revision: Union[str, Sequence[str], None] = '0ca7a4825a02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('saved_search', sa.Column('mileage_to', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('saved_search', 'mileage_to')
