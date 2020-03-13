from flask import Flask
import os
import socket
import requests, json
from random import random
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return jsonify(
        response='Hello World from host \"%s\".\n' % socket.gethostname()
    )

@app.route('/query-example')
def getTriples():
    r = requests.get("https://www.e-codices.ch/metadata/iiif/ubb-A-III-0021/manifest.json")
    print(r.text)
    return r.text

@app.route('/another-example')
def randomNumber():
    return jsonify(
        username='test@test.com',
        email='test@test.com',
        id=random()
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
