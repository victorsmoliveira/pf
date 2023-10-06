import uuid

from fastapi import HTTPException
from pydantic import UUID4

from app.database import (
    metrics_collection,
    sections_collection,
)
from app.models.metric import (
    MetricCreate,
    MetricOut,
    MetricUpdate,
)
from app.models.section import SectionOut
from app.services import database_service


async def create_metric(metric: MetricCreate):
    # Check if the section exists
    section = await database_service.find_one(
        sections_collection, {"name": metric.section_name}
    )

    if not section:
        raise HTTPException(
            status_code=400,
            detail="The specified section does not exist. Please create the section first.",
        )
    else:
        section_id = section["id"]

    # Check if a metric with the same name exists in the specified section
    existing_metric = await database_service.find_one(
        metrics_collection,
        {"section_id": section_id, "metric_name": metric.metric_name},
    )

    if existing_metric:
        raise HTTPException(
            status_code=400,
            detail="A metric with this name already exists in the specified section.",
        )

    metric_data = metric.model_dump()
    metric_data["id"] = str(uuid.uuid4())

    # We want to store section id and not name
    metric_data_in = metric_data.copy()
    metric_data_in.pop("section_name")
    metric_data_in["section_id"] = section["id"]
    await database_service.insert_one(metrics_collection, metric_data_in)

    return metric_data


async def get_metrics_per_section():
    metrics = await database_service.find_and_list(metrics_collection, length=10000)

    if not metrics:
        raise HTTPException(status_code=404, detail="Metrics not found")

    # Group metrics by section
    response = {}
    for metric in metrics:
        metric_data = MetricOut(**metric)
        section_id = str(metric_data.section_id)

        section = await database_service.find_one(
            sections_collection, {"id": section_id}
        )
        section_data = SectionOut(**section)
        section_name = section_data.name

        if section_id not in response:
            response[section_id] = {"name": section_name, "metrics": []}

        metric_data_json = metric_data.model_dump()
        metric_data_json.pop("section_id")
        response[section_id]["metrics"].append(metric_data_json)

    return [
        {
            "section_id": section,
            "section_name": response[section]["name"],
            "metrics": response[section]["metrics"],
        }
        for section in response
    ]


async def read_metric(metric_id: UUID4):
    metric = await database_service.find_one(metrics_collection, {"id": str(metric_id)})
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric


async def update_metric(metric_id: UUID4, metric: MetricUpdate):
    updated_data = metric.model_dump(exclude_unset=True)
    result = await database_service.update_one(
        metrics_collection, {"id": str(metric_id)}, {"$set": updated_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Metric not found")
    return await read_metric(metric_id)


async def delete_metric(metric_id: UUID4):
    result = await database_service.delete_one(
        metrics_collection, {"id": str(metric_id)}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Metric not found")
    return {"message": "Metric deleted successfully!"}
