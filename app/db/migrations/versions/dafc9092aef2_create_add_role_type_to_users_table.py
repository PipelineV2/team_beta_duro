"""create add_role_type_to_users_table

Revision ID: dafc9092aef2
Revises: 7fcd133b2755
Create Date: 2023-05-13 15:18:44.800526

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID



# revision identifiers, used by Alembic.
revision = 'dafc9092aef2'
down_revision = '7fcd133b2755'
branch_labels = None
depends_on = None


user_role_type = sa.Enum("platform", "requester", "waiting", name="user_role_type")


def add_role_type_to_users() -> None:
    op.add_column(
        "users",
        sa.Column(
            "role_type",
            user_role_type,
            nullable=False,
            server_default=sa.text("'platform'::user_role_type"),
        ),
    )
    op.add_column(
        "users",
        sa.Column("role_reference_id", UUID(as_uuid=True), nullable=True),
    )


def upgrade() -> None:
    user_role_type.create(op.get_bind())
    add_role_type_to_users()


def downgrade() -> None:
    op.drop_column("users", "role_type")
    op.drop_column("users", "role_reference_id")
    user_role_type.drop(op.get_bind())
    pass