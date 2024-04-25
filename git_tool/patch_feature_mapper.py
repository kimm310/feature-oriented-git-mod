# This module is there to assign each patch a feature
# Then, the patches can be listed by feature


## Feature assignment is based on the outermost feature annotation
## This concept can vary and potentially added by a custom function

class Feature:
    name: str

def list_all_patches()->list:
    ...

def assign_feature_to_patch() -> Feature:
    ## how do I get the context of a patch
    ...

def list_all_features() -> list[Feature]:
    ...
