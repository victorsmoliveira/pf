import uuid
from fastapi import HTTPException

from app.database import (
    sections_collection,
)
from app.models.section import SectionCreate
from app.services import database_service


async def list_sections():
    sections_list = await database_service.find_and_list(
        sections_collection, length=10000
    )
    return sections_list


async def create_section(section: SectionCreate):
    # Check if a section with the same name exists
    existing_section = await database_service.find_one(
        sections_collection, {"name": section.name}
    )

    if existing_section:
        raise HTTPException(
            status_code=400, detail="A section with this name already exists."
        )

    section_data = section.model_dump()
    section_data["id"] = str(uuid.uuid4())
    await database_service.insert_one(sections_collection, section_data)
    return section_data
