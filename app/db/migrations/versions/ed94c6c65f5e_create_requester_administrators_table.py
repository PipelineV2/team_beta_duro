"""create requester_administrators_table

Revision ID: ed94c6c65f5e
Revises: dafc9092aef2
Create Date: 2023-05-13 15:33:23.143240

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = 'ed94c6c65f5e'
down_revision = 'dafc9092aef2'
branch_labels = None
depends_on = None


def create_requester_administrators_table():
    from app.db.migrations.base.person import create_table_from_person

    create_table_from_person("requester_administrators", op)
    op.add_column(
        "requester_administrators",
        sa.Column("requester_id", UUID(as_uuid=True), nullable=False),
    )

    from app.db.migrations.base.authorizer import authorize_duro

    authorize_duro("requester_administrators", op)


def create_constraints():
    op.create_foreign_key(
        "fk_requesters_requester_administrators",
        "requester_administrators",
        "requesters",
        ["requester_id"],
        ["id"],
        ondelete="CASCADE",
    )


def upgrade() -> None:
    create_requester_administrators_table()
    create_constraints()


def downgrade() -> None:
    op.drop_table("requester_administrators")
