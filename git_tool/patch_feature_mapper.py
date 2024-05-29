# This module is there to assign each patch a feature
# Then, the patches can be listed by feature


## Feature assignment is based on the outermost feature annotation
## This concept can vary and potentially added by a custom function
import subprocess
from unidiff import PatchSet


class Feature:
    name: str


def get_diff_output():
    result = subprocess.run(["git", "diff"], stdout=subprocess.PIPE, text=True)
    return PatchSet(result.stdout)


def list_all_patches() -> list: ...


def assign_feature_to_patch() -> Feature:
    ## how do I get the context of a patch
    ...


def list_all_features() -> list[Feature]: ...
