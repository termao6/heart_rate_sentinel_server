import requests
import json
# from server import tachycardic

def test_index():
    res = requests.get('http://127.0.0.1:5000/')
    print(res.text)
    assert res.text == 'Testing'


def test_new_patient():
    res = requests.post('http://127.0.0.1:5000/api/new_patient',
                  data = {'patient_id': '1',
                          'attending_email': 'tm232@duke.edu',
                          'user_age': '50'})
    json_res = json.loads(res.text)
    assert json_res == {"patient_id": "1",
                    "attending_email": "tm232@duke.edu",
                    "user_age": 50}


def test_new_heart_rate():
    res = requests.post('http://127.0.0.1:5000/api/heart_rate',
                        data = {"patient_id": "1",
                                "heart_rate": "100"})
    json_res = json.loads(res.text)
    assert json_res["heart_rate"] == 100


def test_new_hr_invalid_patient():
    res = requests.post('http://127.0.0.1:5000/api/heart_rate',
                        data = {"patient_id": "2",
                                "heart_rate": "100"})
    assert res.status_code == 404


def test_get_status():
    res = requests.get('http://127.0.0.1:5000/api/status/1')
    json_res = json.loads(res.text)
    assert json_res["tachycardic"] == False


def test_get_invalid_status():
    res = requests.get('http://127.0.0.1:5000/api/heart_rate/10')
    assert res.status_code == 404


def test_get_heart_rates():
    requests.post('http://127.0.0.1:5000/api/heart_rate',
                    data = {"patient_id": "1",
                            "heart_rate": "110"})
    res = requests.get('http://127.0.0.1:5000/api/heart_rate/1')
    json_res = json.loads(res.text)
    assert json_res[0]['heart_rate'] == 100
    assert json_res[1]['heart_rate'] == 110


def test_get_average_hr():
    res = requests.get('http://127.0.0.1:5000/api/heart_rate/average/1')
    json_res = json.loads(res.text)
    assert json_res == {"average_heart_rate": 105,
                        "patient_id": "1"}


def test_get_interval():
    res = requests.post('http://127.0.0.1:5000/api/heart_rate/interval_average',
                        data = {"patient_id": 1,
                                "heart_rate_average_since":
                                    "2018-03-09 11:00:36.372339"})
    json_res = json.loads(res.text)
    assert json_res == {"average_heart_rate": 105,
                        "patient_id": "1"}


# def test_tachycardic():
    # Something funky going on with import statement
    # from server import tachycardic
    # print("a")
    # b = tachycardic(20, 100)
    # print("b")
    # print(b)
    # assert b
    # assert tachychardic(50, 150) is True
    # assert tachychardic(15, 119) is False
    # assert tachychardic(0, 170) is True
