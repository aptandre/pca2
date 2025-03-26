from feedback import Feedback
import MySQLdb

class FeedbackService:
    def __init__(self, db):
        self.db = db

    def save_feedback(self, feedback_id, feedback):
        fback = Feedback(feedback_id, feedback)

        try:
            cur = self.db.connection.cursor()
            cur.execute(
                "INSERT INTO feedback (id, feedback) VALUES (%s, %s)",
                (fback.id, fback.feedback)
            )
            self.db.connection.commit()
            cur.close()

            return True

        except MySQLdb.Error as e:
            print("Erro ao salvar feedback:", e)
            return False
    
    def get_all_feedbacks(self):
        try:
            cur = self.db.connection.cursor()
            cur.execute("SELECT id, feedback FROM feedback")
            rows = cur.fetchall()
            cur.close()

            feedbacks = [Feedback(row[0], row[1]) for row in rows]
            return feedbacks
        
        except MySQLdb.Error as e:
            print("Erro ao buscar feedbacks:", e)
            return []