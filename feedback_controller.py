from feature_service import FeatureService
from feedback_service import FeedbackService
from llm_service import LLMService

class FeedbackController:
    def __init__(self, db):
        self.db = db
        self.feedback_service = FeedbackService(db)
        self.llm_service = LLMService(db)
        self.feature_service = FeatureService(db)

    def get_evaluation(self, data):

        feedback_id = data['id']
        feedback_text = data['feedback']

        self.feedback_service.save_feedback(feedback_id, feedback_text)

        for f in self.feedback_service.get_all_feedbacks():
            print(f)


        #evaluation_result = self.llm_service.evaluate(feedback_id, feedback_text)

        #self.feature_service.save_feature(evaluation_result)

        for f in self.feature_service.get_all_features():
            print(f)

        #print(evaluation_result)

        return {"ok": True}
    
    def get_all_feedbacks(self):
        return self.feedback_service.get_all_feedbacks()
    
    def get_all_features(self):
        return self.feature_service.get_all_features()