import os

from alembic import op as Op


def authorize_duro(table_name: str, op: Op) -> None:
    postgres_op_user = os.environ.get("POSTGRES_OP_USER", None)

    if postgres_op_user is not None:
        grant_op_user_sql = "GRANT ALL ON {} to {}".format(table_name, postgres_op_user)
        op.execute(grant_op_user_sql)
