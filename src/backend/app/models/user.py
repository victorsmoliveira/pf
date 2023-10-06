from pydantic import BaseModel, UUID4
from typing import Optional


# Input model for creating a new user
class UserCreate(BaseModel):
    username: str
    password: str  # For simplicity, we're using plaintext. In real-world scenarios, always hash passwords.
    role: str
    leader_id: Optional[UUID4] = None # TODO: not working


# Input model for updating a user
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    leader_id: Optional[UUID4] = None


# Output model for reading user data
class UserOut(BaseModel):
    id: UUID4
    username: str
    role: str
    leader_id: Optional[UUID4]
