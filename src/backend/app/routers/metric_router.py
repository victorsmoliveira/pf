from typing import Any, List

from fastapi import APIRouter
from pydantic import UUID4

from app.models.metric import (
    MetricCreate,
    MetricOutSectionName,
    MetricUpdate,
    MetricOut,
)
from app.services import metric_service


router = APIRouter()


# Create a new metric
@router.post("/", response_model=MetricOutSectionName)
async def create_metric(metric: MetricCreate):
    return await metric_service.create_metric(metric)


@router.get("/metrics_per_section/", response_model=List[Any])
async def get_metrics_per_section():
    return await metric_service.get_metrics_per_section()


# Get a metric by ID
@router.get("/id/{metric_id}", response_model=MetricOut)
async def read_metric(metric_id: UUID4):
    return await metric_service.read_metric(metric_id)


# Update a metric by ID
@router.put("/id/{metric_id}", response_model=MetricOut)
async def update_metric(metric_id: UUID4, metric: MetricUpdate):
    return await metric_service.update_metric(metric_id, metric)


# Delete a metric by ID
@router.delete("/id/{metric_id}")
async def delete_metric(metric_id: UUID4):
    return await metric_service.delete_metric(metric_id)
