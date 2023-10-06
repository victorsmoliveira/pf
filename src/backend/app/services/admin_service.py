from fastapi import HTTPException
from app.services import database_service

async def list_collections():
    return await database_service.list_collection_names()


async def drop_collection(collection_name: str):
    # Check if the collection exists
    collections = await database_service.list_collection_names()
    if collection_name not in collections:
        raise HTTPException(
            status_code=404, detail=f"Collection {collection_name} not found"
        )

    # Drop the collection
    await database_service.drop_collection()

    return {"message": f"Collection {collection_name} successfully dropped"}
