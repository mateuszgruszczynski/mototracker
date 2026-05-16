"""cascade_delete_and_saved_search_autoincrement

Revision ID: 0ca7a4825a02
Revises: 3709240f77e9
Create Date: 2026-05-16 10:33:51.825265

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ca7a4825a02'
down_revision: Union[str, Sequence[str], None] = '3709240f77e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # SQLite cannot ALTER FK constraints or add AUTOINCREMENT via ALTER TABLE.
    # Both tables are rebuilt via copy-and-move.

    # 1. Rebuild saved_search with AUTOINCREMENT (prevents ID reuse after delete).
    op.execute("""
        CREATE TABLE saved_search_new (
            id      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name    VARCHAR NOT NULL,
            make    VARCHAR NOT NULL,
            model   VARCHAR NOT NULL,
            year_from   INTEGER,
            year_to     INTEGER,
            country_of_origin VARCHAR NOT NULL,
            condition   VARCHAR NOT NULL,
            created_at  DATETIME NOT NULL,
            updated_at  DATETIME NOT NULL
        )
    """)
    op.execute("INSERT INTO saved_search_new SELECT * FROM saved_search")
    op.execute("DROP TABLE saved_search")
    op.execute("ALTER TABLE saved_search_new RENAME TO saved_search")

    # 2. Rebuild listing to change saved_search_id FK from SET NULL to CASCADE.
    op.execute("""
        CREATE TABLE listing_new (
            id          VARCHAR NOT NULL PRIMARY KEY,
            saved_search_id INTEGER REFERENCES saved_search(id) ON DELETE CASCADE,
            make        VARCHAR,
            model       VARCHAR,
            year        INTEGER,
            mileage     INTEGER,
            fuel        VARCHAR,
            gearbox     VARCHAR,
            vin         VARCHAR,
            seller_id   VARCHAR,
            url         VARCHAR NOT NULL,
            title       VARCHAR,
            location    VARCHAR,
            first_seen_at   DATETIME NOT NULL,
            last_seen_at    DATETIME NOT NULL,
            status          VARCHAR NOT NULL,
            sold_at         DATETIME,
            relisted_from_listing_id VARCHAR
        )
    """)
    op.execute("INSERT INTO listing_new SELECT * FROM listing")
    op.execute("DROP TABLE listing")
    op.execute("ALTER TABLE listing_new RENAME TO listing")


def downgrade() -> None:
    pass  # not worth reversing
