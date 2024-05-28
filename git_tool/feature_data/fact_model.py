from datetime import datetime
from enum import Enum

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


class ConstraintDetail(BaseModel):
    constraint_type: ConstraintChangeType
    description: str


class FeatureFactModel(BaseModel):
    commit: str
    authors: List[str]
    date: datetime
    feature: str
    changes: Union[List[ChangeDetail], List[ConstraintDetail]]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class CumulatedFactsModel(BaseModel): ...
