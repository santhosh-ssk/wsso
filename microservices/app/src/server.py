from flask import Flask
#from src import app

from flask import jsonify,render_template,request,redirect
from flask_bootstrap import Bootstrap
import requests
import json
app=Flask(__name__)
bootstrap=Bootstrap(app)
@app.route("/")

def home():
	

	# This is the url to which the query is made
	url = "https://data.biblical52.hasura-app.io/v1/query"

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
    	"Authorization": "Bearer e2dc21035e06649e102be8d7d95601db5ce69da9115767fa",
	    "X-Hasura-Role": "admin"
	}

	# Make the query and store response in resp
	resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
	options=json.loads(resp.content)
	option=list()
	for x in options:
		option+=x["result"]
	options=option
	option=list()
	for x in options:
		option+=x	
	

	# This is the url to which the query is made
	url = "https://data.biblical52.hasura-app.io/v1/query"

	# This is the json payload for the query
	requestPayload = {
	    "type": "select",
	    "args": {
	        "table": "report",
	        "columns": [
	            "*"
	        ]
	    }
	}

	# Setting headers
	headers = {
	    "Content-Type": "application/json",
	    "Authorization": "Bearer e2dc21035e06649e102be8d7d95601db5ce69da9115767fa",
	    "X-Hasura-Role": "admin"
	}

	# Make the query and store response in resp
	resp1 = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
	parameters=json.loads(resp1.content)
	para_keys=list(parameters[0].keys())
	print(para_keys)
	para_keys.remove('status')
	para_keys.remove('sno')
	for i in range(0,len(parameters)):
		if(parameters[i]["status"]=="safe"):
			para_safe=[parameters[i][key] for key in para_keys]
		else:
			para_unsafe=[parameters[i][key] for key in para_keys]
	print(para_keys)
	return render_template("index.html",option=option,para_keys=para_keys,para_safe=para_safe,para_unsafe=para_unsafe)

	#print(option)
	# resp.content contains the json response.
	

# Uncomment to add a new URL at /new

# @app.route("/json")
# def json_message():
#     return jsonify(message="Hello World")
@app.route("/api/v1/request/<name>",methods=['POST',"GET"])
def request_data(name):
	# This is the url to which the query is made
	url = "https://data.biblical52.hasura-app.io/v1/query"

	# This is the json payload for the query
	requestPayload = {
	    "type": "bulk",
	    "args": [
	        {
	            "type": "select",
	            "args": {
	                "table": "record",
	                "columns": [
	                    "*"
	                ],
	                "where": {
	                    "District": {
	                        "$eq": name	                    }
	                }
	            }
	        },
	        {
	            "type": "select",
	            "args": {
	                "table": "record",
	                "columns": [
	                    "*"
	                ],
	                "where": {
	                    "Block": {
	                        "$eq": name
	                    }
	                }
	            }
	        },
	        {
	            "type": "select",
	            "args": {
	                "table": "record",
	                "columns": [
	                    "*"
	                ],
	                "where": {
	                    "Panchayat": {
	                        "$eq": name	                    }
	                }
	            }
	        },
	        {
	            "type": "select",
	            "args": {
	                "table": "record",
	                "columns": [
	                    "*"
	                ],
	                "where": {
	                    "Village": {
	                        "$eq": name	                    }
	                }
	            }
	        }
	    ]
	}

	# Setting headers
	headers = {
 	   "Content-Type": "application/json",
    	"Authorization": "Bearer e2dc21035e06649e102be8d7d95601db5ce69da9115767fa",
    	"X-Hasura-Role": "admin"
	}

	# Make the query and store response in resp
	resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

# resp.content contains the json response.
	options=json.loads(resp.content)
	return jsonify(options)
@app.route("/api/v1/request/login",methods=['POST',"GET"])
def login():
	json_data = request.get_json(force=True)
	user= json_data['username']
	psw= json_data['password']
	url = "https://data.biblical52.hasura-app.io/v1/query"

	# This is the json payload for the query
	requestPayload = {
	    "type": "select",
	    "args": {
	        "table": "userdata",
	        "columns": [
	            "email","level","name"
	        ],
	        "where": {
	            "$and": [
	                {
	                    "email": {
	                        "$eq": user
	                    }
	                },
	                {
	                    "password": {
	                        "$eq":psw
	                    }
	                },
	                {
	                    "auth": {
	                        "$eq": "True"
	                    }
	                }
	            ]
	        }
	    }
	}

	# Setting headers
	headers = {
    	"Content-Type": "application/json",
    	"Authorization": "Bearer e2dc21035e06649e102be8d7d95601db5ce69da9115767fa",
    	"X-Hasura-Role": "admin"
	}

	# Make the query and store response in resp
	resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
	resp=json.loads(resp.content)
	# resp.content contains the json response.
	if(len(resp)>=1):
		return true
	else:
		return "false"

@app.route("/api/v1/request/",methods=['POST',"GET"])
def register():
	json_data = request.get_json(force=True)
	user= json_data['username']
	psw= json_data['password']
	level=json_data['level']
	name=json_data['name']

	# This is the url to which the query is made
	url = "https://data.biblical52.hasura-app.io/v1/query"

	# This is the json payload for the query
	requestPayload = {
	    "type": "insert",
	    "args": {
	        "table": "userdata",
	        "objects": [
	            {
	                "email": user,
	                "password": psw,
	                "auth": "true",
	                "name": name,
	                "level": level
	            }
	        ]
	    }
	}

	# Setting headers
	headers = {
    	"Content-Type": "application/json",
    	"Authorization": "Bearer e2dc21035e06649e102be8d7d95601db5ce69da9115767fa",
    	"X-Hasura-Role": "admin"
	}

	# Make the query and store response in resp
	resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

	# resp.content contains the json response.
	resp=json.loads(resp.content)

	# This is the json payload for the query
	requestPayload = {
	    "type": "select",
	    "args": {
	        "table": "record",
	        "columns": [
	            "*"
	        ],
	        "where": {
	            level: {
	                "$eq": name
	            }
	        }
	    }
	}

	# Setting headers
	headers = {
    	"Content-Type": "application/json",
    	"Authorization": "Bearer e2dc21035e06649e102be8d7d95601db5ce69da9115767fa",
    	"X-Hasura-Role": "admin"
	}

	# Make the query and store response in resp
	resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

	# resp.content contains the json response.
	resp=json.loads(resp.content)
	if(len(resp)>=1):
		return true
	else:
		return "false" 

if __name__ == "__main__":
	app.run(debug=True)

"""
	requestPayload = {
	    "to": user,
	    "from": "santhoshkumar.ssk54@gmail.com",
	    "fromName": "WSSO",
	    "sub": "Report on "+name+" "+level,
	    "text": "This is the email content in plain text",
	    "html": "<p>This is the <b>email content</b> in html format</p>"
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

"""
	