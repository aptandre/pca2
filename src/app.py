import json
from typing import Counter
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL

from src.controller.feedback_controller import FeedbackController

app = Flask(__name__)

load_dotenv()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'alumind_user'
app.config['MYSQL_PASSWORD'] = '123drink'
app.config['MYSQL_DB'] = 'alumind'

mysql = MySQL(app)
feedback_controller = FeedbackController(mysql, ['andre.alves@ccc.ufcg.edu.br'])

@app.route("/")
def home_page():
    feedbacks = feedback_controller.get_all_feedbacks()
    features = feedback_controller.get_all_features()

    percents = feedback_controller.get_feedbacks_percentage()
    feature_ranking = feedback_controller.get_feedbacks_ranking()

    for f in features:
        if isinstance(f.features, str):
            try:
                f.features = json.loads(f.features)
            except json.JSONDecodeError:
                f.features = []
                
    return render_template(
        "relatorio.html",
        porcentagens=percents,
        ranking=feature_ranking,
        feedbacks=feedbacks,
        features=features
    )

@app.route("/feedbacks", methods=['POST'])
def get_feedback_evaluation():
    data = request.get_json()

    parsed_data = feedback_controller.get_evaluation(data)

    return jsonify(parsed_data)