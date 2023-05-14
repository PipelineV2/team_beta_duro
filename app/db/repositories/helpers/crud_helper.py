import uuid

from databases import Database

from app.models.core import DeletedCount


async def delete_by_id(
    id: uuid.UUID,
    query: str,
    db: Database,
) -> DeletedCount:
    query_values = {
        "id": id,
    }
    deleted_count = await db.fetch_one(query=query, values=query_values)
    count = 0 if deleted_count is None else len(deleted_count)
    return DeletedCount(count=count)
