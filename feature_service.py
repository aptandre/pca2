from feature import Feature

class FeatureService:
    def __init__(self):
        pass

    def save_feature(self, evaluation_result):
        id = evaluation_result['id']
        sentiment = evaluation_result['sentiment']
        features = evaluation_result['features']

        feature = Feature(id, sentiment, features)
        print("FEATURE PERSISTIDO!")
        print(feature)