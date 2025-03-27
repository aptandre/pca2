from src.service.email_service import EmailService
from src.service.metrics_service import MetricsService
from src.service.feature_service import FeatureService
from src.service.feedback_service import FeedbackService
from src.service.llm_service import LLMService
import schedule

class FeedbackController:
    def __init__(self, db, stakeholders_list):
        self.db = db
        self.feedback_service = FeedbackService(db)
        self.llm_service = LLMService(db)
        self.feature_service = FeatureService(db)
        self.metrics_service = MetricsService(db, self.feature_service)
        self.email_service = EmailService(db, stakeholders_list, self.metrics_service, self.llm_service)

    def get_evaluation(self, data):

        feedback_id = data['id']
        feedback_text = data['feedback']

        try:
            self.feedback_service.save_feedback(feedback_id, feedback_text)
        except Exception as e:
            return {
                'error': 'Erro ao salvar feedback',
                'message': str(e)
            }

        try:
            evaluation_result = self.llm_service.evaluate(feedback_id, feedback_text)
        except Exception as e:
            return {
                'error': 'Ocorreu um erro ao tentar avaliar o feedback.',
                'message': str(e)
            }
        
        try:
            self.feature_service.save_feature(evaluation_result)
        except Exception as e:
            return {
                'error': 'Erro ao salvar a feature desejada.',
                'message': str(e)
            }

        try:
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
        return self.feature_service.get_all_features()
    
    def get_feedbacks_percentage(self):
        return self.metrics_service.get_percentage_feedbacks()
    
    def get_feedbacks_ranking(self):
        return self.metrics_service.get_most_wanted_features()
    
    def send_email_to_stakeholders(self):
        schedule.every().friday.at("17:00").do(self.email_service.send_report())