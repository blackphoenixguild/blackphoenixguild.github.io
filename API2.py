from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import random
app = Flask(__name__)
CORS(app)

events = [
    {
        "id": 0,
        "starter": "a",
        "dungeon": "test a",
        "info": "A test event for the web app and api"
    },
    
    {
        "id": 1,
        "starter": "b",
        "dungeon": "test b",
        "info": "A test event for the web app and api 2"
    }
]

@app.route("/")
def get_event(id_=0):
    for event in events:
        if event["id"] == int(id_):
            return event
