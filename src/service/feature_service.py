import json
import MySQLdb
from src.model.feature import Feature

class FeatureService:
    def __init__(self, db):
        self.db = db

    def save_feature(self, evaluation_result):
        id = evaluation_result['id']
        sentiment = evaluation_result['sentiment']
        features = evaluation_result['features']

        feature = Feature(id, sentiment, features)
        features = json.dumps(features)
        try:
            cur = self.db.connection.cursor()
            cur.execute(
                "INSERT INTO feature (id, sentiment, features) VALUES (%s, %s, %s)",
                (feature.id, feature.sentiment, features)
            )
            self.db.connection.commit()
            cur.close()

            return True
        
        except MySQLdb.Error as e:
            print("Erro ao salvar feature:", e)
            return False
        
    def get_all_features(self):
        try:
            cur = self.db.connection.cursor()
            cur.execute("SELECT id, sentiment, features FROM feature")
            rows = cur.fetchall()
            cur.close()

            features = [Feature(row[0], row[1], row[2]) for row in rows]
            return features
        
        except MySQLdb.Error as e:
            print("Erro ao buscar features:", e)
            return []