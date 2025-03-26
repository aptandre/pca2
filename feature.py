class Feature:
    def __init__(self, id: str, sentiment: str, features: list):
        self.id = id
        self.sentiment = sentiment
        self.features = features

    def __str__(self):
        return f"id: {self.id}\nsentiment:{self.sentiment}\nfeatures:{self.features}"