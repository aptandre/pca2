import json
import MySQLdb
from src.model.feedback_response import FeedbackResponse

class FeedbackResponseService:
    def __init__(self, db):
        self.db = db

    def save_feedback_response(self, evaluation_result):
        id = evaluation_result['id']
        sentiment = evaluation_result['sentiment']
        features = evaluation_result['features']

        feedback_response = FeedbackResponse(id, sentiment, features)

        features = json.dumps(features)
        try:
            cur = self.db.connection.cursor()
            cur.execute(
                "INSERT INTO feature (id, sentiment, features) VALUES (%s, %s, %s)",
                (feedback_response.id, feedback_response.sentiment, features)
            )
            self.db.connection.commit()
            cur.close()

            return True
        
        except MySQLdb.Error as e:
            print("Erro ao salvar FeedbackResponse:", e)
            return False
        
    def get_all_feedback_response(self):
        try:
            cur = self.db.connection.cursor()
            cur.execute("SELECT id, sentiment, features FROM feature")
            rows = cur.fetchall()
            cur.close()

            features = [FeedbackResponse(row[0], row[1], row[2]) for row in rows]
            return features
        
        except MySQLdb.Error as e:
            print("Erro ao buscar FeedbackResponses:", e)
            return []