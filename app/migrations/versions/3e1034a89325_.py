"""empty message

Revision ID: 3e1034a89325
Revises: 36af51010eac
Create Date: 2024-03-05 15:31:21.458280

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e1034a89325'
down_revision: Union[str, None] = '36af51010eac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
