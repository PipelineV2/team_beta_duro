import sqlalchemy as sa
from alembic import op as Op
from sqlalchemy.dialects.postgresql import UUID


def create_table_from_corporation(table_name: str, op: Op) -> None:
    op.create_table(
        table_name,
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("email", sa.VARCHAR, nullable=False),
        sa.Column("name", sa.VARCHAR, nullable=False),
        sa.Column("description", sa.VARCHAR, nullable=True),
        sa.Column("legal_name", sa.VARCHAR, nullable=True),
        sa.Column("duns", sa.VARCHAR, nullable=True),
        sa.Column("email", sa.VARCHAR, nullable=True),
        sa.Column("telephone", sa.VARCHAR, nullable=True),
        sa.Column("url", sa.VARCHAR, nullable=True),
        sa.Column("tax_id", sa.VARCHAR, nullable=True),
        sa.Column("vat_id", sa.VARCHAR, nullable=True),
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
        sa.Column("deleted_at", sa.TIMESTAMP, nullable=True),
        sa.UniqueConstraint("email"),
    )
