from typing import Dict, List, Union
from fastapi import HTTPException
from pydantic import UUID4

from app.database import users_collection, metrics_collection, user_metrics_collection
from app.models.user_metric import UserMetricIn, UserMetricItem
from app.services import database_service, user_service


# async def upsert_user_metric(data: UserMetricIn):
#     # Fetch user based on user_id
#     user = await users_collection.find_one({"id": str(data.user_id)})

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Fetch the related metric based on metric_id
#     metric = await metrics_collection.find_one({"id": str(data.metric_id)})

#     if not metric:
#         raise HTTPException(status_code=404, detail="Metric not found")

#     # Validate the value based on metric's data_type
#     if metric["data_type"] == "integer":
#         try:
#             int(data.value)
#         except ValueError:
#             raise HTTPException(status_code=400, detail="Value should be an integer")

#     elif metric["data_type"] == "decimal":
#         try:
#             float(data.value)
#         except ValueError:
#             raise HTTPException(status_code=400, detail="Value should be a decimal")

#     elif metric["data_type"] == "list":
#         if data.value not in metric["list_values"]:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Value not in allowed list values. Allowed values are: {metric['list_values']}",
#             )

#     # Note: For "text" data_type, no specific validation is required as any string is valid.

#     # Check if user metric exists
#     existing_user_metric = await user_metrics_collection.find_one(
#         {"user_id": str(data.user_id), "metric_id": str(data.metric_id)}
#     )

#     # Update or insert based on existence
#     if existing_user_metric:
#         await user_metrics_collection.update_one(
#             {"_id": existing_user_metric["_id"]}, {"$set": {"value": data.value}}
#         )
#     else:
#         user_metric_data = data.model_dump()
#         user_metric_data["user_id"] = str(data.user_id)
#         user_metric_data["metric_id"] = str(data.metric_id)
#         await user_metrics_collection.insert_one(user_metric_data)

#     return {"message": "User metric successfully upserted"}


async def upsert_user_metrics_bulk(
    user_id: UUID4, user_metrics: Dict[UUID4, Union[str, int, float]]
):
    await user_service.read_user(user_id)
    # Fetch all relevant metrics and their data types
    metric_ids = [str(key) for key in user_metrics]
    metrics = await database_service.find_and_list(
        metrics_collection,
        filter={"id": {"$in": metric_ids}},
        length=len(metric_ids),
    )
    if not metrics:
        raise HTTPException(
            status_code=404, detail="No metrics were found in the database."
        )

    metric_data = {
        metric["id"]: {
            "data_type": metric["data_type"],
            "data_properties": metric["data_properties"],
        }
        for metric in metrics
    }

    # Validate data types
    for metric_id, user_value in user_metrics.items():
        metric_id_data = metric_data.get(str(metric_id))
        _validate_data_type(user_value, str(metric_id), metric_id_data)

    # Proceed with upsert logic
    for metric_id, user_value in user_metrics.items():
        # Check if a user metric exists for this user and metric_id
        existing_user_metric = await user_metrics_collection.find_one(
            {"user_id": str(user_id), "metric_id": str(metric_id)}
        )

        # Update or insert based on existence
        if existing_user_metric:
            await database_service.update_one(
                user_metrics_collection,
                {"_id": existing_user_metric["_id"]},
                {"$set": {"user_value": user_value}},
            )
        else:
            new_user_metric = {
                "user_id": str(user_id),
                "metric_id": str(metric_id),
                "user_value": user_value,
            }
            await database_service.insert_one(user_metrics_collection, new_user_metric)

    return {"message": "User metrics upserted successfully!"}


def _validate_data_type(user_value, metric_id, metric_id_data):
    """
    Validates the value against the expected data type.
    """
    data_type = metric_id_data["data_type"]
    data_properties = metric_id_data["data_properties"]

    if data_type == "string" and not isinstance(user_value, str):
        raise HTTPException(
            status_code=400,
            detail=f"Value type for metric {metric_id} should be string",
        )
    elif data_type in ("integer", "decimal") and not isinstance(
        user_value, (int, float)
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Value type for metric {metric_id} should be a number",
        )
    elif data_type == "list" and user_value not in data_properties.get("list_values"):
        raise HTTPException(
            status_code=400,
            detail=f"Value '{user_value}' for metric {metric_id} not in allowed list values. Allowed values for metric are: {data_properties.get('list_values')}",
        )
    return True


async def read_user_metric_by_id(user_metric_id: str):
    user_metric = await user_metrics_collection.find_one({"_id": user_metric_id})
    if not user_metric:
        raise HTTPException(status_code=404, detail="User metric not found")
    user_metric["id"] = str(user_metric["_id"])
    return user_metric


async def delete_user_metric_by_id(user_metric_id: str):
    result = await user_metrics_collection.delete_one({"_id": user_metric_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User metric not found")
    return {"message": "User metric deleted successfully!"}


async def get_user_metrics(user_id: UUID4):
    user_metrics = await database_service.find_and_list(
        user_metrics_collection, filter={"user_id": str(user_id)}, length=1000
    )

    return {
        "user_metrics": {
            user_metric["metric_id"]: user_metric["user_value"]
            for user_metric in user_metrics
        }
    }
