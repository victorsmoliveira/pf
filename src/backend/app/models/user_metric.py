from pydantic import UUID4, BaseModel
from typing import Dict, List, Union


class UserMetricItem(BaseModel):
    metric_id: UUID4
    user_value: Union[str, int, float]


class UserMetricsBulkUpdate(BaseModel):
    user_id: UUID4
    user_metrics: Dict[UUID4, Union[str, int, float]]
    # user_metrics: Dict[UUID4, Union[str, float, int]]


class UserMetricIn(BaseModel):
    user_id: str
    metric_id: str
    value: str


# Output model for reading user metric data
class UserMetricOut(BaseModel):
    metric_id: UUID4
    user_id: str
    metric_id: str
    value: str

class UserMetricDict(BaseModel):
    user_metrics: Dict[UUID4, Union[str, int, float]]