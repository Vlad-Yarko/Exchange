"""Update User

Revision ID: 15632b10d652
Revises: 9a1816f60667
Create Date: 2025-04-26 00:41:09.688000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15632b10d652'
down_revision: Union[str, None] = '9a1816f60667'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'users',
        'password',
        existing_type=sa.LargeBinary(),
        nullable=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
