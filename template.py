from flask import Flask
import os
import glob
import socket
import requests, json
from random import random
from flask import jsonify, request, redirect, url_for, make_response, render_template
from flask_cors import CORS
import subprocess

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
@app.route("/hello/<name>")
def hello_name(name):
    return "Hello %s!" % name.capitalize()

# Integer
@app.route("/item/<int:itemID>")
def show_item(itemID):
    return "Item number %d:" % itemID

# Float
@app.route("/version/<float:versionNo>")
def show_version(versionNo):
    return "Version number %f:" % versionNo

##################
# Named parameters
##################

@app.route("/hero")
def show_hero():
    name = request.args.get("name", default = "Nobody", type = str)
    return "%s will save you!" % name.capitalize()

    # /hero?name=batman
    # --> Batman will save you!

    # /hero
    # --> Nobody will save you!

##############
# HTTP methods
##############

# POST & GET
# ...also introducing redirect and url_for
@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        return redirect(url_for("hello_name", name = name))
    else:
        return render_template("login.html")

##############################
# Receiving and returning JSON
##############################

@app.route("/json", methods = ["POST"])
def json_example():

    # Check if the request body contains JSON
    if request.is_json:

        # Parse JSON into a Python dictionary
        req = request.get_json()

        # Static response body
        response_body = {
            "message": "JSON received!"
        }

        # Create JSON response
        res = make_response(jsonify(response_body), 200)

        # Return JSON response
        return res

    else:
        # The request body is not JSON
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)

#################
# Delille example
#################

# Citations per verse per type of author
@app.route("/delille/piechart", methods = ["POST"])
def delille_piechart():

    # Check if the request body contains JSON
    if request.is_json:

        # Parse JSON into a Python dictionary
        req = request.get_json()

        # Getting iterable of actual results
        bindings = req["results"]["bindings"]

        # Total numbers of citations per authors of interest
        sum_menOfLetters = 0
        sum_vulgarizers  = 0
        sum_artists      = 0
        sum_others       = 0

        # Check number of citations per author for each verse
        # and add it to the total number per author
        for i in bindings:
            sum_menOfLetters += int(i["menOfLetters"]["value"])
            sum_vulgarizers  += int(i["vulgarizers"]["value"])
            sum_artists      += int(i["artists"]["value"])
            sum_others       += int(i["otherRoles"]["value"])

        # Create response body
        response_body = {
            "data": [
                {
                    "label": "Men of letters",
                    "value": sum_menOfLetters
                },
                {
                    "label": "Vulgarizers",
                    "value": sum_vulgarizers
                },
                {
                    "label": "Artists",
                    "value": sum_artists
                },
                {
                    "label": "Others",
                    "value": sum_others
                }
            ]
        }

        # Create JSON response
        res = make_response(jsonify(response_body), 200)

        # Return JSON response
        return res

    else:
        # The request body is not JSON
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)


@app.route("/transform", methods = ["POST", "GET"])
def transform():
    if request.method == "POST":

        # Get data and save as file
        data = request.form["data"]
        df = open("temp_files/yourData.json", "w+")
        df.write(data)
        df.close()

        # Get code and save as file
        code = request.form["code"]
        cf = open("temp_files/yourCode.py", "w+")
        cf.write(code)
        cf.close()

        # Enter temp_files directory and execute code file
        os.chdir("temp_files")
        process = subprocess.run(["python3", "yourCode.py"], check = True, stdout = subprocess.PIPE, universal_newlines = True)
        # Save output
        output = process.stdout

        # Delete saved files
        files = glob.glob("*")
        for f in files:
            os.remove(f)

        # Leave temp_files directory
        os.chdir("..")

        return output
    else:
        return render_template("transform.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
