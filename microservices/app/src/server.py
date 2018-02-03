from src import app
from flask import jsonify,render_template
from flask.ext.bootstrap import Bootstrap
import requests
import json
bootstrap=Bootstrap(app)
@app.route("/")
def home():
	# This is the url to which the query is made
	url = "https://data.annulment76.hasura-app.io/v1/query"

	# This is the json payload for the query
	requestPayload = {
	    "type": "bulk",
	    "args": [
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select DISTINCT \"District\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select DISTINCT \"Block\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select DISTINCT \"Panchayat\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select DISTINCT \"Village\" from record;"
	            }
	        }
	    ]
	}

	# Setting headers
	headers = {
	    "Content-Type": "application/json",
	    "Authorization": "Bearer 60bcda7f858ca2dd9d5cf503cdb7aeeafcc997f6c469c66a"
	}

	# Make the query and store response in resp
	resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

	# resp.content contains the json response.
	print resp.content
    return render_template("index.html")

# Uncomment to add a new URL at /new

# @app.route("/json")
# def json_message():
#     return jsonify(message="Hello World")
