from git_tool import finding_features

TESTSTRING = """
    Hier ist etwas Code &begin[FEATURE1]
    Code für FEATURE1
    weiterer Code für FEATURE1
    &end[FEATURE1]
    &begin[FEATURE2]
    Code für FEATURE2
    &end[FEATURE2]
    """

def test_extract_features():
    features = finding_features.extract_features(TESTSTRING)
    feature_names = list(map(lambda x: x.name, features))
    assert feature_names == ["FEATURE1", "FEATURE2"]