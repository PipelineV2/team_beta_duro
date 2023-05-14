import sqlalchemy as sa
from alembic import op as Op
from sqlalchemy.dialects.postgresql import ENUM, UUID


def flow_direction_enum() -> sa.Enum:
    return sa.Enum("inbound", "outbound", name="web_api_flow_direction")


def create_table_from_apikey(table_name: str, op: Op) -> None:
    op.create_table(
        table_name,
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("client_id", sa.VARCHAR, nullable=False),
        sa.Column("client_secret", sa.VARCHAR, nullable=False),
        sa.Column(
            "flow_direction",
            ENUM(name=flow_direction_enum().name, create_type=False),
            nullable=True,
        ),
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.text("now()")
        ),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
        sa.Column("deleted_at", sa.TIMESTAMP, nullable=True),
        sa.UniqueConstraint("client_id"),
    )
