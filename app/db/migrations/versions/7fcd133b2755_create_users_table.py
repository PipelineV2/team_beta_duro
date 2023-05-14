"""create users_table

Revision ID: 7fcd133b2755
Revises: d94255521c20
Create Date: 2023-05-13 14:23:22.070097

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '7fcd133b2755'
down_revision = 'd94255521c20'
branch_labels = None
depends_on = None


def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("email", sa.VARCHAR, nullable=False),
        sa.Column("hashed_password", sa.VARCHAR, nullable=False),
        sa.Column("is_active", sa.BOOLEAN, nullable=False),
        sa.Column("is_superuser", sa.BOOLEAN, nullable=False),
        sa.Column("is_verified", sa.BOOLEAN, nullable=False),
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
        sa.Column("deleted_at", sa.TIMESTAMP, nullable=True),
        sa.UniqueConstraint("email"),
    )

    from app.db.migrations.base.authorizer import authorize_duro

    authorize_duro("users", op)


def upgrade() -> None:
    create_users_table()


def downgrade() -> None:
    op.drop_table("users")
