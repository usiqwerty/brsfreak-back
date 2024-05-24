import json

from flask import Flask, request
from flask_cors import CORS, cross_origin

import storage

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/get-user-data')
@cross_origin(origins='*')
def get_user_data():
    user_id = request.args["user_id"]
    password = request.args["pass"]
    return storage.get_user_data(user_id, password)


@app.route('/set-user-data', methods=["POST"])
@cross_origin(origins='*')
def set_user_data():
    userdata = json.loads(request.data.decode())
    user_id = userdata['user_id']
    data = userdata['data']
    password = userdata["pass"]
    success = storage.set_user_data(user_id, data, password)

    if success:
        return "Good"
    else:
        return "Wrong password", 401


if __name__ == '__main__':
    app.run(host="0.0.0.0")
