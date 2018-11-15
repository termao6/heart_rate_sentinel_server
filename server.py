from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

patients = {}
heart_rates = {}


@app.route('/')
def index():
    return 'Testing'


@app.route('/api/new_patient', methods=['POST'])
def new_patient():
    patient = {
        "patient_id": request.form['patient_id'],
        "attending_email": request.form['attending_email'],
        "user_age": int(request.form['user_age'])
    }
    patients[patient["patient_id"]] = patient
    return jsonify(patient)


@app.route('/api/heart_rate', methods=['POST'])
def new_heart_rate():
    # check that such patient exists
    pat_id = request.form['patient_id']
    heart_rate = {
        "heart_rate": int(request.form['heart_rate']),
        "timestamp": datetime.datetime.now()
    }
    if pat_id in heart_rates:
        hr_arr = heart_rates[pat_id]
        hr_arr.append(heart_rate)
        heart_rates[pat_id] = hr_arr
    else:
        heart_rates[pat_id] = [heart_rate]
    return jsonify(heart_rate)


@app.route('/api/status/<patient_id>')
def get_status(patient_id):
    # check that such patient and such heart rate readings exist
    pat_heart_rates = heart_rates[patient_id]
    last_heart_rate = pat_heart_rates[len(pat_heart_rates) - 1]
    hr = last_heart_rate["heart_rate"]
    age = patients[patient_id]["user_age"]
    ret = {
        "tachycardic": check_tachychardic(age, hr),
        "timestamp": last_heart_rate["timestamp"]
    }
    return jsonify(ret)


@app.route('/api/heart_rate/<patient_id>')
def get_heart_rates(patient_id):
    return jsonify(heart_rates[patient_id])


@app.route('/api/heart_rate/average/<patient_id>')
def get_average_hr(patient_id):
    # check that such patient and such heart rate readings exist
    sum = 0
    for hr in heart_rates[patient_id]:
        sum = sum + hr["heart_rate"]
    avg = sum/len(heart_rates[patient_id])
    return jsonify({"patient_id": patient_id, "average_heart_rate": avg})


@app.route('/api/heart_rate/interval_average', methods=['POST'])
def get_interval():
    # form = request.get_json()
    # print(form)
    patient_id = request.form["patient_id"]
    since_time = datetime.datetime.strptime(request.form["heart_rate_average_since"], '%Y-%m-%d %H:%M:%S.%f')
    print(patient_id)
    print(since_time)
    # check that such patient and such heart rate readings exist
    sum = 0
    for hr in heart_rates[patient_id]:
        if hr["timestamp"] > since_time:
            sum = sum + hr["heart_rate"]
    avg = sum/len(heart_rates[patient_id])
    return jsonify({"patient_id": patient_id, "average_heart_rate": avg})



# HELPER METHODS
def check_tachychardic(age, hr):
    return True


app.run('127.0.0.1')
