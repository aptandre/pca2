from feature_service import FeatureService
from feedback_service import FeedbackService
from llm_service import LLMService

class FeedbackController:
    def __init__(self):
        self.feedback_service = FeedbackService()
        self.llm_service = LLMService()
        self.feature_service = FeatureService()

    def get_evaluation(self, data):
        print(data)
        print(type(data))
        print("\n\n\n")
        feedback_id = data['id']
        feedback_text = data['feedback']

        self.feedback_service.save_feedback(feedback_id, feedback_text)

        evaluation_result = self.llm_service.evaluate(feedback_id, feedback_text)

        self.feature_service.save_feature(evaluation_result)

        print(evaluation_result)

        return {"ok": True}