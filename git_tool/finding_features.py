from dataclasses import dataclass

@dataclass
class FeatureMatches:
    name: str


def extract_features(text: str) -> list[FeatureMatches]:
    """Extract Features as well as information about their location in code depending on 
    &begin[] und &end[] Tags.

    @param text: content from which features are extracted
    """
    
    return [FeatureMatches(name="FEATURE1"), FeatureMatches(name="FEATURE2")]

