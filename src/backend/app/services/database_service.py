from fastapi import HTTPException
from app.database import database


async def find_and_list(collection, filter: dict = {}, length=None):
    """Find all records based on an optional filter, then lists the results with a maximum number of length."""
    return await collection.find(filter).to_list(length)


async def insert_one(collection, data: dict):
    """Insert a new record into a collection."""
    return await collection.insert_one(data)


async def find_one(collection, filter: dict):
    """Find a single record based on a filter."""
    return await collection.find_one(filter)


async def update_one(collection, filter: dict, update: dict):
    """Update a record based on a filter."""
    return await collection.update_one(filter, update)


async def delete_one(collection, filter: dict):
    """Delete a record based on a filter."""
    return await collection.delete_one(filter)


async def list_collection_names():
    """Return the list of collection names from the database."""
    return await database.list_collection_names(database)


async def drop_collection(collection):
    """Drops the specified collection."""
    return await database[collection].drop()
