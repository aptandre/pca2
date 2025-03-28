class FeedbackResponse:
    def __init__(self, id: str, sentiment: str, features: list[dict]):
        self.id = id
        self.sentiment = sentiment
        self.features = features

    def __str__(self):
        return f"id: {self.id}\nsentiment:{self.sentiment}\nfeatures:{self.features}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'sentiment': self.sentiment,
            'features': self.features
        }