from datetime import datetime
from enum import Enum
from typing import Optional

from git import List, Union
from pydantic import BaseModel


class ChangeType(str, Enum):
    ADDED = "hinzugefügt"
    MODIFIED = "geändert"
    REMOVED = "entfernt"


class ConstraintChangeType(str, Enum):
    DELETED = "Abhängigkeit gelöscht"
    ADDED = "Abhängigkeit hinzugefügt"
    MODIFIED = "Abhängigkeit angepasst"


class ChangeDetail(BaseModel):
    change_type: ChangeType
    description: str


class UpdateName(BaseModel):
    feature_name: str


class ConstraintDetail(BaseModel):
    constraint_type: ConstraintChangeType
    description: str


class ChangeHolder(BaseModel):
    code_changes: List[ChangeDetail]
    name_change: Optional[UpdateName]
    constraint_changes: List[ConstraintDetail]


class FeatureFactModel(BaseModel):
    commit: str
    authors: list[str]
    date: datetime
    features: list[str]
    changes: ChangeHolder

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class CumulatedFactsModel(BaseModel): ...
