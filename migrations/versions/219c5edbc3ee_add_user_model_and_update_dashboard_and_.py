"""Add User model and update Dashboard and Chart models

Revision ID: 219c5edbc3ee
Revises: 86d56950d328
Create Date: 2024-08-07 05:07:59.891936

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '219c5edbc3ee'
down_revision = '86d56950d328'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dashboard',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('date_filter', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('chart',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('dashboard_name', sa.String(), nullable=False),
    sa.Column('chart_type', sa.String(), nullable=False),
    sa.Column('sql_query', sa.Text(), nullable=False),
    sa.Column('x_axis_field', sa.String(), nullable=False),
    sa.Column('y_axis_field', sa.String(), nullable=False),
    sa.Column('date_field', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.ForeignKeyConstraint(['dashboard_name'], ['dashboard.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chart')
    op.drop_table('dashboard')
    # ### end Alembic commands ###
