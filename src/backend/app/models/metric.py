from pydantic import BaseModel, UUID4, StringConstraints, validator
from typing import Annotated, Optional, List, Union
from enum import Enum


class DataTypeEnum(str, Enum):
    integer = "integer"
    decimal = "decimal"
    string = "string"
    list = "list"


class IntProperties(BaseModel):
    min: int = 0
    max: int = None


class ListProperties(BaseModel):
    list_values: Optional[List[str]] = None


# Input model for creating a new metric
class MetricCreate(BaseModel):
    section_name: str
    metric_name: str
    description: str
    data_type: DataTypeEnum
    # TODO add IntProperties as well. It is not working straight away.
    data_properties: Optional[ListProperties] = {}

    class Config:
        json_schema_extra = {
            "example": {
                "section_name": "Section 1",
                "metric_name": "Metric 1",
                "description": "This is a metric.",
                "data_type": "integer",
                "data_properties": {},
            }
        }

    # list_values: Optional[List[str]] = None

    @validator("data_properties", pre=True, always=True)
    def validate_data_properties(cls, data_properties, values):
        if values.get("data_type") == "list" and not data_properties.get("list_values"):
            raise ValueError(
                "data_properties.list_values is required when data_type is 'list'"
            )
        if values.get("data_type") != "list" and data_properties.get("list_values"):
            raise ValueError(
                "data_properties.list_values should only be provided when data_type is 'list'"
            )
        return data_properties


# Input model for updating a metric
class MetricUpdate(BaseModel):
    section_name: Optional[str] = None
    metric_name: Optional[str] = None
    description: Optional[str] = None
    data_type: Optional[str] = None
    data_properties: ListProperties = {}


# Output model for reading metric data
class MetricOutSectionName(BaseModel):
    id: UUID4
    section_name: str
    metric_name: str
    description: str
    data_type: str
    data_properties: ListProperties = {}


class MetricOut(BaseModel):
    id: UUID4
    section_id: UUID4
    metric_name: str
    description: str
    data_type: str
    data_properties: ListProperties = {}
