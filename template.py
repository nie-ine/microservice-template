from flask import Flask
import os
import socket
import requests, json
from random import random
from flask import jsonify, request, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

##############
# Basic routes
##############

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

################
# Variable parts
################

# String
@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' % name.capitalize()

# Integer
@app.route('/item/<int:itemID>')
def show_item(itemID):
   return 'Item number %d:' % itemID

# Float
@app.route('/version/<float:versionNo>')
def show_version(versionNo):
   return 'Version number %f:' % versionNo

##################
# Named parameters
##################

@app.route('/hero')
def show_hero():
    name = request.args.get('name', default = 'Nobody', type = str)
    return '%s will save you!' % name.capitalize()

    # /hero?name=batman
    # --> Batman will save you!

    # /hero
    # --> Nobody will save you!

##############
# HTTP methods
##############

# POST & GET
# ...also introducing redirect and url_for
@app.route('/login', methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      name = request.form['name']
      return redirect(url_for('hello_name', name = name))
   else:
      name = request.args.get('name')
      return redirect(url_for('hello_name', name = name))

      # POST: run template.py and open template.html in browser
      # GET: /login?name=superman


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
