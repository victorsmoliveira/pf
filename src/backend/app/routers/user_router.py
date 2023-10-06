import uuid
from fastapi import APIRouter
from fastapi import HTTPException

from app.database import users_collection
from app.models.user import UserCreate, UserOut, UserUpdate
from pydantic import UUID4


router = APIRouter()

# Mocked database (in-memory lists for this example)
users_db = []


# Create a new user
@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate):
    user_data = user.model_dump()
    user_data["id"] = str(uuid.uuid4())
    user_data["password"] = "hashed_password"  # Hash the password before saving
    await users_collection.insert_one(user_data)
    return user_data


# Get a user by ID
@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: UUID4):
    user = await users_collection.find_one({"id": str(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update a user by ID
@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: UUID4, user: UserUpdate):
    updated_data = user.model_dump(exclude_unset=True)
    if "password" in updated_data:
        updated_data["password"] = "hashed_password"  # Hash the password before saving
    result = await users_collection.update_one(
        {"id": str(user_id)}, {"$set": updated_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return await read_user(user_id)


# Delete a user by ID
@router.delete("/{user_id}")
async def delete_user(user_id: UUID4):
    result = await users_collection.delete_one({"id": str(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully!"}
