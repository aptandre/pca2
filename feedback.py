class Feedback:
    def __init__(self, id: str, feedback: str):
        self.id = id
        self.feedback = feedback

    def __str__(self):
        return f"id:{self.id}\ntext:{self.feedback}"