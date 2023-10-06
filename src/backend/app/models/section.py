from pydantic import BaseModel, UUID4


# Input model for creating a new section
class SectionCreate(BaseModel):
    name: str


# Output model for reading section data
class SectionOut(BaseModel):
    id: UUID4
    name: str
