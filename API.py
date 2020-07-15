from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import random
app = Flask(__name__)
api = Api(app)
cors = CORS(app)

events = [
    {
        "id": 0,
        "starter": "SCtre",
        "dungeon": "Undead Lair",
        "info": "we are running the undead lair"
    },
    
    {
        "id": 1,
        "starter": "b",
        "dungeon": "test b",
        "info": "A test event for the web app and api 2"
    }
]

def set_event(starter, dungeon, info):
    events[0]["starter"] = starter
    events[0]["dungeon"] = dungeon
    events[0]["info"] = info

class Event(Resource):
    def get(self, id=999):
        if id == 999:
            return random.choice(events), 200
        for event in events:
            if(event["id"] == id):
                return event, 200, {'Access-Control-Allow-Origin': '*'}
        return "Event not found", 404

api.add_resource(Event, "/events", "/events/", "/events/<int:id>")
if __name__ == '__main__':
    app.run(debug=True)
