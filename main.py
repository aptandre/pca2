from flask import Flask, jsonify, request

from feedback_controller import FeedbackController

app = Flask(__name__)

feedback_controller = FeedbackController()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/feedbacks", methods=['POST'])
def get_feedback_evaluation():
    data = request.get_json()

    parsed_data = feedback_controller.get_evaluation(data)
    return jsonify(parsed_data)