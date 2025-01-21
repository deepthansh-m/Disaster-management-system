"""Added parameters

Revision ID: 79c70d5ca604
Revises: c79bdabb0c71
Create Date: 2024-12-09 16:01:30.806241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79c70d5ca604'
down_revision = 'c79bdabb0c71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('disaster_history', sa.Column('parameters', sa.JSON(), nullable=True))
    op.add_column('disaster_history', sa.Column('prediction', sa.String(), nullable=True))
    op.add_column('disaster_history', sa.Column('confidence', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('disaster_history', 'confidence')
    op.drop_column('disaster_history', 'prediction')
    op.drop_column('disaster_history', 'parameters')
    # ### end Alembic commands ###
