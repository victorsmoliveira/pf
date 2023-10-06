import uuid
from fastapi import APIRouter
from fastapi import HTTPException

from app.database import users_collection
from app.models.user import UserCreate, UserUpdate
from pydantic import UUID4
from app.services import database_service

router = APIRouter()

# Mocked database (in-memory lists for this example)
users_db = []


async def create_user(user: UserCreate):
    user_data = user.model_dump()
    user_data["id"] = str(uuid.uuid4())
    user_data["password"] = "hashed_password"  # Hash the password before saving
    await database_service.insert_one(users_collection, user_data)
    return user_data


async def read_user(user_id: UUID4):
    user = await database_service.find_one(users_collection, {"id": str(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def update_user(user_id: UUID4, user: UserUpdate):
    updated_data = user.model_dump(exclude_unset=True)
    if "password" in updated_data:
        updated_data["password"] = "hashed_password"  # Hash the password before saving
    result = await database_service.update_one(
        users_collection, {"id": str(user_id)}, {"$set": updated_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return await read_user(user_id)


async def delete_user(user_id: UUID4):
    result = await database_service.delete_one(users_collection, {"id": str(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully!"}
