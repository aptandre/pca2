from src.service.email_service import EmailService
from src.service.metrics_service import MetricsService
from src.service.feedback_response_service import FeedbackResponseService
from src.service.feedback_service import FeedbackService
from src.service.llm_service import LLMService
import schedule

class FeedbackController:
    def __init__(self, db, stakeholders_list):
        self.db = db
        self.feedback_service = FeedbackService(db)
        self.llm_service = LLMService(db)
        self.feedback_response_service = FeedbackResponseService(db)
        self.metrics_service = MetricsService(db, self.feedback_response_service)
        self.email_service = EmailService(db, stakeholders_list, self.metrics_service, self.llm_service)

    def get_evaluation(self, data):

        feedback_id = data['id']
        feedback_text = data['feedback']

        try:

            self.feedback_service.save_feedback(feedback_id, feedback_text)

            evaluation_result = self.llm_service.evaluate(feedback_id, feedback_text)

            self.feedback_response_service.save_feedback_response(evaluation_result)

            self.send_email_to_stakeholders()

        except Exception as e:
            return {
                'error': 'Erro ao enviar e-mail aos stakeholders.',
                'message': str(e)
            }

        return evaluation_result
    
    def get_all_feedbacks(self):
        return self.feedback_service.get_all_feedbacks()
    
    def get_all_features(self):
        return self.feedback_response_service.get_all_feedback_response()
    
    def get_feedbacks_percentage(self):
        return self.metrics_service.get_percentage_feedbacks()
    
    def get_feedbacks_ranking(self):
        return self.metrics_service.get_most_wanted_features()
    
    def send_email_to_stakeholders(self):
        schedule.every().friday.at("17:00").do(self.email_service.send_report)