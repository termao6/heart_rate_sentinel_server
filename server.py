from flask import Flask, request, jsonify, abort
import datetime

app = Flask(__name__)

patients = {}
heart_rates = {}


@app.route('/')
def index():
    return 'Testing'


@app.route('/api/new_patient', methods=['POST'])
def new_patient():
    """
    POST new patient to patients dictionary
    form:
        patient_id,
        attending_email,
        user_age
    {patient_id: {form info}
    :return: json verifying posted info
    """
    # Validate age
    patient = {
        "patient_id": request.form['patient_id'],
        "attending_email": request.form['attending_email'],
        "user_age": int(request.form['user_age'])
    }
    patients[patient["patient_id"]] = patient
    return jsonify(patient)


@app.route('/api/heart_rate', methods=['POST'])
def new_heart_rate():
    """
    POST add heart_rate & timestamp to array
    form:
        patient_id,
        heart_rate
    heart_rates = {patient_id : array[heart_rate, timestamp]}
    :return: json of {heart_rate, timestamp}
    """
    pat_id = request.form['patient_id']
    check_patient_exists(pat_id) # check that such patient exists
    # if record exists, patient must also exist
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

    # IF TACHYCARDIC, SEND EMAIL TO ATTENDING PHYS
    return jsonify(heart_rate)


@app.route('/api/status/<patient_id>')
def get_status(patient_id):
    """
    GET check last heart_rate entered and check if tachycardic
    :param patient_id: id of patient to be checked
    :return: json {tachycardic: bool, timestamp: time of last entry}
    """
    check_records_exist(patient_id)
    # check that such patient and such heart rate readings exist
    pat_heart_rates = heart_rates[patient_id]
    last_heart_rate = pat_heart_rates[len(pat_heart_rates) - 1]
    hr = last_heart_rate["heart_rate"]
    age = patients[patient_id]["user_age"]
    ret = {
        "tachycardic": tachychardic(age, hr),
        "timestamp": last_heart_rate["timestamp"]
    }
    return jsonify(ret)


@app.route('/api/heart_rate/<patient_id>')
def get_heart_rates(patient_id):
    """
    GET all the previous heart rate measurements for that patient
    :param patient_id: id of patient to check
    :return: json array of {heart_rate, timestamp}
    """
    check_records_exist(patient_id)
    return jsonify(heart_rates[patient_id])


@app.route('/api/heart_rate/average/<patient_id>')
def get_average_hr(patient_id):
    """
    GET the patients's average heart rate over all measurements
    stored for this user

    :param patient_id:
    :return: average heart rate over all measurements
    """
    check_records_exist(patient_id)
    sum = 0
    for hr in heart_rates[patient_id]:
        sum = sum + hr["heart_rate"]
    avg = sum/len(heart_rates[patient_id])
    return jsonify({"patient_id": patient_id,
                    "average_heart_rate": avg})


@app.route('/api/heart_rate/interval_average', methods=['POST'])
def get_interval():
    """
    POST patient_id and datetime from which average caculation begins
    does not store posted info
    :return: json {patient_id, average_hr}
    """
    # form = request.get_json()
    # print(form)
    patient_id = request.form["patient_id"]
    since_time = datetime.datetime.strptime(
        request.form["heart_rate_average_since"],
        '%Y-%m-%d %H:%M:%S.%f')

    check_records_exist(patient_id)

    sum = 0
    ctr = 0
    for hr in heart_rates[patient_id]:
        if hr["timestamp"] > since_time:
            sum = sum + hr["heart_rate"]
            ctr = ctr + 1
    avg = sum/ctr
    return jsonify({"patient_id": patient_id,
                    "average_heart_rate": avg})


# HELPER METHODS
def tachychardic(age, hr):
    """

    :param age: age of patient
    :param hr: latest heart rate to compare against threshold
    :return: True if tachycardic, false if not
    """
    if age < 1 and hr > 169:
        return True
    elif age <= 2 and hr > 151:
        return True
    elif age <= 4 and hr > 137:
        return True
    elif age <= 7 and hr > 133:
        return True
    elif age <= 11 and hr > 130:
        return True
    elif age <= 15 and hr > 119:
        return True
    elif age > 15 and hr > 100:
        return True

    return False


def check_patient_exists(pat_id):
    """
    checks if pat_id exists as key in patients
    raises 404 exception if not
    :param pat_id:
    """
    if pat_id not in patients:
        abort(404, "Patient with id {} not found"
              .format(pat_id))


def check_records_exist(pat_id):
    """
    checks if pat_id exists as key in heart_rate
    raises 404 exception if not
    :param pat_id:
    """
    # if record exists, patient must also exist
    if pat_id not in patients:
        abort(404, "Patient with id {} does not yet have"
                   " a heart rate recording".format(pat_id))


# ERRORHANDLERS
@app.errorhandler(404)
def handle_not_found(error):
    return jsonify(error=404, text=str(error)), 404


app.run('127.0.0.1')
