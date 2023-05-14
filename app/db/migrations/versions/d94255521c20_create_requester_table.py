"""create requester_table

Revision ID: d94255521c20
Revises: 
Create Date: 2023-05-13 12:02:37.632776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd94255521c20'
down_revision = None
branch_labels = None
depends_on = None

requester_status_type = sa.Enum("active", "inactive", name="requester_status_type")


def create_requesters_table() -> None:
    from app.db.migrations.base.corporation import create_table_from_corporation

    create_table_from_corporation("requesters", op)

    # create the enum
    requester_status_type.create(op.get_bind())

    # alter table
    op.add_column(
        "requesters",
        sa.Column(
            "status",
            requester_status_type,
            nullable=False,
            server_default=sa.text("'active'::requester_status_type"),
        ),
    )

    from app.db.migrations.base.authorizer import authorize_duro

    authorize_duro("requesters", op)

def upgrade() -> None:
    create_requesters_table()


def downgrade() -> None:
    op.drop_table("requesters")
    requester_status_type.drop(op.get_bind())
