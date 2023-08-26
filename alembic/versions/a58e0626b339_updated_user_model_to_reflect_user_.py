"""updated user model to reflect user account status

Revision ID: a58e0626b339
Revises: 9529c00d6178
Create Date: 2023-08-25 18:02:40.057542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a58e0626b339'
down_revision: Union[str, None] = '9529c00d6178'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
