"""add_sold_at_relisted_from_listing_id

Revision ID: 3709240f77e9
Revises: cf78aa649f8b
Create Date: 2026-05-16 01:04:42.053577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3709240f77e9'
down_revision: Union[str, Sequence[str], None] = 'cf78aa649f8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('listing', sa.Column('sold_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('listing', sa.Column('relisted_from_listing_id', sa.String(), nullable=True))
    # SQLite does not support ALTER to add FK constraints; column is a logical FK only.


def downgrade() -> None:
    op.drop_column('listing', 'relisted_from_listing_id')
    op.drop_column('listing', 'sold_at')
