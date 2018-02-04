#from flask import Flask
from src import app
from flask import jsonify,render_template,request,redirect
from flask.ext.bootstrap import Bootstrap
import requests
import json
#app=Flask(__name__)
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
	options=json.loads(resp.content)
	option=list()
	for x in options:
		option+=x["result"]
	options=option
	option=list()
	for x in options:
		option+=x	
	
		# This is the url to which the query is made
	url = "https://data.annulment76.hasura-app.io/v1/query"

	# This is the json payload for the query
	requestPayload = {
	    "type": "bulk",
	    "args": [
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select  \"Chloride\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select  \"Sulphates\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select  \"Alkalinity\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select  \"Manganese\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select  \"Calcium\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select  \"Magnesium\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select  \"Iron\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select  \"Coliform\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select  \"TDS\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select  \"Turbidity\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select  \"Fluoride\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select  \"pH\" from record;"
	            }
	        },
	        {
	            "type": "run_sql",
	            "args": {
	                "sql": "select  \"Hardness\" from record;"
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
	resp1 = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
	parameters=json.loads(resp1.content)
	para=list()
	for x in parameters:
		safe=0
		unsafe=0
		for j in x["result"][1:]:
			data=list(str(j[0]).split('@'))
			if(len(data)>=2):
				data=data[1]
				if(data=="safe" or data=="permissible"):
					safe+=1
				else:
					unsafe+=1
			else:
				continue
		para.append([(x['result'][0][0]),safe,unsafe])
	para_keys=[x[0] for x in para]
	para_safe=[x[1] for x in para]
	para_unsafe=[x[2] for x in para]
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
	url = "https://data.annulment76.hasura-app.io/v1/query"

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
	    "Authorization": "Bearer 60bcda7f858ca2dd9d5cf503cdb7aeeafcc997f6c469c66a"
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
	url = "https://data.annulment76.hasura-app.io/v1/query"

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
	    "Authorization": "Bearer 53c56d1e6c312c79c8a45a56aab27bf15be2c96d346bd5f4"
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
	url = "https://data.annulment76.hasura-app.io/v1/query"

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
	    "Authorization": "Bearer c13eee07dc87b8b77b11974f01e1b74c899d3afd3da7f279"
	}

	# Make the query and store response in resp
	resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

	# resp.content contains the json response.
	resp=json.loads(resp.content)
	if(len(resp)>=1):
		return true
	else:
		return "false"
"""
if __name__ == "__main__":
	app.run(debug=True)
"""