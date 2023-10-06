from typing import List
from fastapi import APIRouter

from app.models.section import SectionCreate, SectionOut
from app.services import section_service

router = APIRouter()


# List sections
@router.get("/list/", response_model=List[SectionOut])
async def list_sections():
    return await section_service.list_sections()


# Create a new section
@router.post("/", response_model=SectionOut)
async def create_section(section: SectionCreate):
    return await section_service.create_section(section)
