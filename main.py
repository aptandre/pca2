import json
from typing import Counter
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL

from feedback_controller import FeedbackController

app = Flask(__name__)

load_dotenv()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'alumind_user'
app.config['MYSQL_PASSWORD'] = '123drink'
app.config['MYSQL_DB'] = 'alumind'

mysql = MySQL(app)
feedback_controller = FeedbackController(mysql)

@app.route("/")
def hello_world():
    features = feedback_controller.get_all_features()

    sentiment_count = Counter([f.sentiment.upper() for f in features])

    total = sum(sentiment_count.values())
    percents = {
        'POSITIVO': round(sentiment_count.get('POSITIVO', 0) / total * 100, 1),
        'NEGATIVO': round(sentiment_count.get('NEGATIVO', 0) / total * 100, 1),
        'INCONCLUSIVO': round(sentiment_count.get('INCONCLUSIVO', 0) / total * 100, 1)
    }


    all_feature_codes = []

    for f in features:
        feature_list = f.features
        if isinstance(feature_list, str):
            try:
                feature_list = json.loads(feature_list)
            except json.JSONDecodeError:
                continue

        for item in feature_list:
            if isinstance(item, dict) and 'code' in item:
                all_feature_codes.append(item['code'])

    feature_ranking = Counter(all_feature_codes).most_common(10)

    print(features)

    return render_template(
        "relatorio.html",
        porcentagens=percents,
        ranking=feature_ranking,
        features=features
    )

@app.route("/feedbacks", methods=['POST'])
def get_feedback_evaluation():
    data = request.get_json()

    parsed_data = feedback_controller.get_evaluation(data)
    return jsonify(parsed_data)