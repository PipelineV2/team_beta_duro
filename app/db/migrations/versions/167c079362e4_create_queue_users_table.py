"""create queue_users_table

Revision ID: 167c079362e4
Revises: ed94c6c65f5e
Create Date: 2023-05-16 05:26:42.131050

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '167c079362e4'
down_revision = 'ed94c6c65f5e'
branch_labels = None
depends_on = None

queue_status_type = sa.Enum("active", "inactive", name="queue_status_type")


def create_queue_users_table():
    op.create_table(
        "queue_users",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("email", sa.VARCHAR, nullable=False),
        sa.Column("device_id", UUID(as_uuid=True), nullable=False),
        sa.Column("given_name", sa.VARCHAR, nullable=True),
        sa.Column("family_name", sa.VARCHAR, nullable=True),
        sa.Column("display_name", sa.VARCHAR, nullable=True),
        sa.Column("telephone", sa.VARCHAR, nullable=True),
        sa.Column("job_title", sa.VARCHAR, nullable=True),
        sa.Column(
            "status", sa.VARCHAR, nullable=False, server_default=sa.text("'active'")
        ),
        
        sa.Column("time_queued", sa.TIMESTAMP(), nullable=True),
        sa.Column("time_dequeued", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
        sa.Column("created_by_requester_id", UUID(as_uuid=True), nullable=False),
        sa.Column("created_by_administrator_id", UUID(as_uuid=True), nullable=False),
    )
    
    from app.db.migrations.base.authorizer import authorize_duro

    authorize_duro("queue_users", op)


def create_constraints():
    op.create_unique_constraint(
        "uq_queue_users_email",
        "queue_users",
        ["email"]
    )

    op.create_unique_constraint(
        "uq_queue_users_telephone",
        "queue_users",
        ["telephone"]
    )
    op.create_unique_constraint(
        "uq_queue_users_device_id",
        "queue_users",
        ["device_id"]
    )
    op.create_foreign_key(
        "fk_queue_users_requesters",
        "queue_users",
        "requesters",
        ["created_by_requester_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_queue_users_administrators",
        "queue_users",
        "requester_administrators",
        ["created_by_administrator_id"],
        ["id"],
        ondelete="CASCADE",
    )

def upgrade() -> None:
    create_queue_users_table()
    create_constraints()


def downgrade() -> None:
    op.drop_table("queue_users")
