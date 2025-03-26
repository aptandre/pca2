from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

from feedback_controller import FeedbackController

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'alumind_user'
app.config['MYSQL_PASSWORD'] = '123drink'
app.config['MYSQL_DB'] = 'alumind'

mysql = MySQL(app)
feedback_controller = FeedbackController(mysql)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/feedbacks", methods=['POST'])
def get_feedback_evaluation():
    data = request.get_json()

    parsed_data = feedback_controller.get_evaluation(data)
    return jsonify(parsed_data)