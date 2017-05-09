"""demo tables

Revision ID: fe0810e2ff7e
Revises: 
Create Date: 2017-05-09 15:03:26.386457

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'fe0810e2ff7e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('car',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('engine', sa.JSON(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('plan',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('order_item_id', sa.String(), nullable=True),
                    sa.Column('graph', sa.JSON(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    pass
