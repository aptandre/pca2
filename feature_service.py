import MySQLdb
from feature import Feature

class FeatureService:
    def __init__(self, db):
        self.db = db

    def save_feature(self, evaluation_result):
        id = evaluation_result['id']
        sentiment = evaluation_result['sentiment']
        features = evaluation_result['features']

        feature = Feature(id, sentiment, features)
        try:
            cur = self.db.connection.cursor()
            cur.execute(
                "INSERT INTO feature (id, sentiment, features) VALUES (%s, %s, %s)",
                (feature.id, feature.sentiment, str(feature.features))
            )
            self.db.connection.commit()
            cur.close()

            return True
        except MySQLdb.Error as e:
            print("Erro ao salvar feature:", e)
            return False