"""created post table

Revision ID: 48fd3b9cbf02
Revises: 
Create Date: 2024-02-04 23:10:02.779413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48fd3b9cbf02'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('post', 
                    sa.Column ('id' , sa.Integer(), nullable= False, primary_key= True), 
                    sa.Column('post', sa.String(), nullable= False))
    pass


def downgrade() -> None:
    pass
