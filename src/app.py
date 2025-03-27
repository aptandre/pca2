import json
import os
import MySQLdb
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL

from src.controller.feedback_controller import FeedbackController
from src.service.db_setup_service import DatabaseSetupService

app = Flask(__name__)

load_dotenv()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

feedback_controller = FeedbackController(mysql, ['andre.alves@ccc.ufcg.edu.br'])
db_setup_service = DatabaseSetupService(mysql)

@app.before_first_request
def setup_database():
    db_setup_service.create_database()
    db_setup_service.create_tables()


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