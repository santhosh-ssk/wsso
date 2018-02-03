from src import app
from flask import jsonify,render_template
from flask.ext.bootstrap import Bootstrap
import requests
import json

print resp.content
bootstrap=Bootstrap(app)
@app.route("/")
def home():
    return render_template("index.html")

# Uncomment to add a new URL at /new

# @app.route("/json")
# def json_message():
#     return jsonify(message="Hello World")
