import json
from typing import Counter


class MetricsService:
    def __init__(self, database):
        self.database = database

    def get_percentage_feedbacks(self):

        features = self.database.get_all_features()

        sentiment_count = Counter([f.sentiment.upper() for f in features])

        total = sum(sentiment_count.values())
        percents = {
            'POSITIVO': round(sentiment_count.get('POSITIVO', 0) / total * 100, 1),
            'NEGATIVO': round(sentiment_count.get('NEGATIVO', 0) / total * 100, 1),
            'INCONCLUSIVO': round(sentiment_count.get('INCONCLUSIVO', 0) / total * 100, 1)
        }

        return percents
    
    def get_most_wanted_features(self):
        
        all_feature_codes = []

        features = self.database.get_all_features()

        for f in features:
            feature_list = f.features
            if isinstance(feature_list, str):
                try:
                    feature_list = json.loads(feature_list)
                except json.JSONDecodeError:
                    continue

            for item in feature_list:
                if isinstance(item, dict) and 'code' in item:
                    all_feature_codes.append(item['code'])

        feature_ranking = Counter(all_feature_codes).most_common(10)

        return feature_ranking