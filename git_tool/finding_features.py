import re
from dataclasses import dataclass

from git import Diff


@dataclass
class FeatureMatches:
    name: str
    code: str


def extract_features(text: str) -> list[FeatureMatches]:
    """Extract Features as well as information about their location in code depending on
    &begin[] und &end[] Tags.

    @param text: content from which features are extracted
    """
    # regex for regex101.com
    # &begin\[(?<FeatureName>.*?)\](?<FeatureCode>.*?)&end\[\1\]
    # with flags gms
    feature_pattern = r"&begin\[(?P<FeatureName>.*?)\](?P<FeatureCode>.*?)&end\[(?P=FeatureName)\]"
    feature_matches = re.finditer(
        pattern=feature_pattern, string=text, flags=re.DOTALL
    )
    feature_list = [
        FeatureMatches(
            name=match.group("FeatureName"),
            code=match.group("FeatureCode").strip(),
        )
        for match in feature_matches
    ]

    return feature_list


def get_features_for_diff(diff: Diff) -> list[FeatureMatches]:
    str_diff = (
        diff.diff.decode("utf-8") if isinstance(diff.diff, bytes) else diff.diff
    )
    features = extract_features(str_diff)
    # features can also be assigned from the file itself as well as from file and folder mappings
    # skip that for now
    return features
