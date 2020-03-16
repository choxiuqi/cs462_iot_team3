from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.debug = True #to set in staging development
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sxwvjgwhgvzwcu://smt203team2:9c7e10ad14854f8266bb4830c93f9c412d621b945ad04bd82f73c28b44247423@ec2-18-235-20-228.compute-1.amazonaws.com:5432/d3tvcbdn77mrah'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://team3user:password@localhost:5432/cs462team3db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Sensor, MeetingRoom, USSRecord, LatestUSSRecord, Occupancy, SensorHealth, PIRRecord, Upcoming

@app.route('/hello/', methods=['GET']) 
def hello():
    # print('hello')
    return 'hello'

@app.route('/meeting-room', methods=['GET']) 
def get_meetingRoom(): 
    # if 'id' in request.args: 
    #     id = int(request.args.get('id'))
        
    #     print (request.json())
    # else: 
    #     students = Student.query.all() 
    #     return jsonify([s.serialize() for s in students])

    meeting_room = MeetingRoom.query.all()
    return jsonify([m.serialize() for m in meeting_room])

@app.route('/sensors', methods=['GET']) 
def get_sensors(): 
    sensors = Sensor.query.all()
    return jsonify([s.serialize() for s in sensors])

# api for dashboard
@app.route('/sensor-health', methods=['GET'])
def sensorHealth():
    health = Sensor.query.all()
    # a1 = jsonify([h.health() for h in health])
    # s1 = json.dumps(a1)
    # json_data = json.loads(j1)
    final_dict = {}
    for temp_dict in health:
        d1 = temp_dict.serialize()
        final_dict["sensor_health"] = d1["sensor_health"]
        # for k,v in d1.items():
        #     if k == "desc" or k == "meeting_room_id":
        #         final_dict["sensor_health"] = {k:v}
        #     elif k == "sensor_health":
        #         final_dict["sensor_health"] = v
        #     elif k != "desc" or k != "meeting_room_id":
        #         final_dict[k] = v
    return jsonify(final_dict)

@app.route('/occupancy', methods=['GET']) 
def get_occupancy(): 
    occupancy = Occupancy.query.all()
    return jsonify([o.serialize() for o in occupancy])

@app.route('/event', methods=['GET'])
def get_event():
    event = Upcoming.query.all()
    return jsonify([e.serialize() for e in event])

#amelia added
@app.route('/latest_uss_record', methods=['GET']) 
def get_latest_uss_record(): 
    latest_records = LatestUSSRecord.query.all()
    return jsonify([l.serialize() for l in latest_records])
#to get the current reading occupancy in database 

