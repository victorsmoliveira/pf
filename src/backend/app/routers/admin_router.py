from fastapi import APIRouter, HTTPException
from app.database import database
from app.services import admin_service

router = APIRouter()


@router.get("/list_collections/")
async def list_collections():
    return await admin_service.list_collections(database)


@router.delete("/drop_collection/{collection_name}/")
async def drop_collection(collection_name: str):
    return await admin_service.drop_collection(collection_name)
