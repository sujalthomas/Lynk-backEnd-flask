"""Added password_reset_code to User table

Revision ID: 9529c00d6178
Revises: e1ebc0966392
Create Date: 2023-08-25 16:17:46.459124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9529c00d6178'
down_revision: Union[str, None] = 'e1ebc0966392'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
