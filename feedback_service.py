from feedback import Feedback


class FeedbackService:
    def __init__(self):
        pass

    def save_feedback(self, feedback_id, feedback):
        fback = Feedback(feedback_id, feedback)
        print("FEEDBACK PERSISTIDO!")
        print(fback)
    
