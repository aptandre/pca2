from flask import Flask, request

from feedback_controller import FeedbackController

app = Flask(__name__)

feedback_controller = FeedbackController()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/feedbacks", methods=['POST'])
def get_feedback_evaluation():
    data = request.get_data()

    return feedback_controller.get_evaluation(data)