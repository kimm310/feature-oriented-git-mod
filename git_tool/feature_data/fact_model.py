from datetime import datetime
from enum import Enum
from typing import Optional

from git import List, Union
from pydantic import BaseModel, ValidationError

from git_tool.feature_data.repo_context import FEATURE_BRANCH_NAME, repo_context


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


def get_fact_from_featurefile(filename: str) -> FeatureFactModel | None:
    print("evaluating", filename)
    with repo_context() as repo:
        try:
            file_content = repo.git.show(f"{FEATURE_BRANCH_NAME}:{filename}")
            return FeatureFactModel.model_validate_json(file_content)
        except ValidationError as e:
            print(
                "Validation didn't work",
            )
            print(e)
        finally:
            return None
