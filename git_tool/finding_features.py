from dataclasses import dataclass
import re

@dataclass
class FeatureMatches:
    name: str
    code: str


def extract_features(text: str) -> list[FeatureMatches]:
    """Extract Features as well as information about their location in code depending on 
    &begin[] und &end[] Tags.

    @param text: content from which features are extracted
    """
    # regex for regex101.com &begin\[(?<FeatureName>.*?)\](?<FeatureCode>.*?)&end\[\1\] with flags gms
    feature_pattern = r'&begin\[(?P<FeatureName>.*?)\](?P<FeatureCode>.*?)&end\[(?P=FeatureName)\]'
    feature_matches = re.finditer(pattern=feature_pattern, string=text, flags=re.DOTALL)
    feature_list = [FeatureMatches(name=match.group('FeatureName'), code=match.group('FeatureCode').strip()) for match in feature_matches]
    
    return feature_list

