from typing import List
from fastapi import APIRouter
from pydantic import UUID4

from app.models.user_metric import (
    UserMetricOut,
    UserMetricIn,
    UserMetricsBulkUpdate,
    UserMetricItem,
    UserMetricDict,
)
from app.services import user_metric_service

router = APIRouter()

# Mocked database (in-memory lists for this example)
users_db = []


@router.post("/")
async def upsert_user_metric(data: UserMetricIn):
    return await user_metric_service.upsert_user_metric(data)


@router.post("/bulk")
async def upsert_user_metrics_bulk(data: UserMetricsBulkUpdate):
    return await user_metric_service.upsert_user_metrics_bulk(
        data.user_id, data.user_metrics
    )


@router.get("/user/{user_id}", response_model=UserMetricDict)
async def get_user_metrics(user_id: UUID4):
    return await user_metric_service.get_user_metrics(user_id)


# Get a user metric by ID
@router.get("/id/{user_metric_id}", response_model=UserMetricOut)
async def read_user_metric_by_id(user_metric_id: str):
    return await user_metric_service.read_user_metric_by_id(user_metric_id)


# Delete a user metric by ID
@router.delete("/id/{user_metric_id}", response_model=dict)
async def delete_user_metric_by_id(user_metric_id: str):
    return await user_metric_service.delete_user_metric_by_id(user_metric_id)
