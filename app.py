from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
import json
from datetime import datetime

app = Flask(__name__)
app.debug = True #to set in staging development
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sxwvjgwhgvzwcu://smt203team2:9c7e10ad14854f8266bb4830c93f9c412d621b945ad04bd82f73c28b44247423@ec2-18-235-20-228.compute-1.amazonaws.com:5432/d3tvcbdn77mrah'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://team3user:password@localhost:5432/cs462team3db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Sensor, MeetingRoom, USSRecord, LatestUSSRecord, Occupancy, SensorHealth, PIRRecord, Upcoming, OccupancyDebug, PIRRecordDebug, ManualCounter

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
    final_list = []
    for temp_dict in health:
        final_dict = {}
        d1 = temp_dict.serialize()
        final_dict["id"] = d1["id"]
        final_dict["pir_records"] = d1["pir_records"]
        final_dict["sensor_health"] = d1["sensor_health"]
        for k,v in d1.items():
            if k == "sensor_health":
                for a in v:
                    a["desc"] = d1["desc"]
                    a["meeting_room_id"] = d1["meeting_room_id"]
            # if k == "pir_records":
            #     for i in v:
            #         if "temperature" not in k:
            #             i["temperature"] = "null"
            #         if "meeting_room_id" not in k:
            #             i["meeting_room_id"] = "G"
        final_list.append(final_dict)
    return jsonify(final_list)

@app.route('/sensor-health-debug', methods=['GET'])
def sensorHealthDebug():
    health = Sensor.query.all()

    final_list = []
    for temp_dict in health:
        final_dict = {}
        d1 = temp_dict.health()
        final_dict["id"] = d1["id"]
        final_dict["pir_records"] = d1["pir_records"]
        final_dict["sensor_health"] = d1["sensor_health"]
        for k,v in d1.items():
            if k == "sensor_health":
                for a in v:
                    a["desc"] = d1["desc"]
                    a["meeting_room_id"] = d1["meeting_room_id"]
            elif k == "pir_records":
                for a in v:
                    a["desc"] = d1["desc"]
                    a["meeting_room_id"] = d1["meeting_room_id"]
        final_list.append(final_dict)

    return jsonify(final_list)

@app.route('/occupancy', methods=['GET']) 
def get_occupancy(): 
    occupancy = Occupancy.query.all()
    return jsonify([o.serialize() for o in occupancy])

@app.route('/occupancy-debug', methods=['GET'])
def get_occupancy_debug():
    occupancy = Occupancy.query.all()
    
    finalList = []
    for tempDict in occupancy:
        finalDict = {}
        d1 = tempDict.serialize()
        finalDict['id'] = d1['id']
        finalDict['meeting_room_id'] = d1['meeting_room_id']
        for k,v in d1.items():
            if k == 'timestamp':
                # finalDict['timestamp'] = v.strftime('%d-%m-%Y %H:%M:%S')
                finalDict['date'] = v.strftime('%Y-%m-%d')
                finalDict['time'] = v.strftime('%H:%M:%S.%fZ')
        finalDict['value'] = d1['value']
        finalList.append(finalDict)

    return jsonify(finalList)

@app.route('/event', methods=['GET'])
def get_event():
    event = Upcoming.query.all()
    return jsonify([e.serialize() for e in event])

# @app.route('/occupancy-debug', methods=['POST'])
# def get_event_occupancy():
#     event = Upcoming.query.all()
#     return jsonify([e.serialize() for e in event])

#amelia added
@app.route('/latest_uss_record', methods=['GET']) 
def get_latest_uss_record(): 
    latest_records = LatestUSSRecord.query.all()
    return jsonify([l.serialize() for l in latest_records])
#to get the current reading occupancy in database 


# xq added
@app.route('/manual-counting', methods=['GET'])
def count():
    return render_template('clicker.html')


# sinsin added
@app.route("/count/<int:id>", methods=['POST'])
def create_count(id):
    data = request.get_json()
    count = ManualCounter(id,**data)

    try:
        db.session.add(count)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the count."}), 500

    return jsonify(count.json()), 201