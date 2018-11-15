from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

patients = []
heart_rates = []


@app.route('/')
def index():
    return 'Testing'


@app.route('/api/new_patient', methods=['POST'])
def new_patient():
    patient = {
        "patient_id": request.form['patient_id'],
        "attending_email": request.form['attending_email'],
        "user_age": request.form['user_age']
    }
    patients.append(patient)
    return jsonify(patient)


@app.route('/api/heart_rate', methods=['POST'])
def new_heart_rate():
    heart_rate = {
        "patient_id": request.form['patient_id'],
        "heart_rate": request.form['heart_rate'],
        "timestamp": datetime.datetime.now()
    }
    heart_rates.append(heart_rate)
    return jsonify(heart_rate)


app.run('127.0.0.1')
