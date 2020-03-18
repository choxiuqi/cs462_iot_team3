import json
import requests
import os
import time
import subprocess
import csv

def getoccupancy(url):
    occupancy = requests.get(url).json()
    # print(type(occupancy))
    json_dump = json.dumps(occupancy)
    json_parsed = json.loads(json_dump)
    # print(type(json_parsed))
    json_data = open('occupancy.csv', 'w')
    csvwriter = csv.writer(json_data)

    header = json_parsed[0].keys()
    csvwriter.writerow(header)
    for i in range(0,len(json_parsed)):
        csvwriter.writerow(json_parsed[i].values())
        # print(i, json_parsed[i].values())
    json_data.close()
    return ('occupancy.csv')


def getsensorhealth(url):
    data = requests.get(url).json()
    json_data = open('sensors.csv', 'w')

    sensor = data[0]['sensor_health']
    json_dump = json.dumps(sensor)
    json_parsed = json.loads(json_dump)
    json_data = open('sensors.csv', 'w')
    csvwriter = csv.writer(json_data)
    if len(sensor) > 0:
        header = json_parsed[0].keys()
        csvwriter.writerow(header)
        for i in range(0,len(json_parsed)):
            csvwriter.writerow(json_parsed[i].values())

    for i in range(1, len(data)):
        if data[i]["id"] != "X001":
            sensor = data[i]['sensor_health']
            json_dump = json.dumps(sensor)
            json_parsed = json.loads(json_dump)
            csvwriter = csv.writer(json_data)
            if len(sensor) > 0:
                for i in range(0,len(json_parsed)):
                    csvwriter.writerow(json_parsed[i].values())
        elif data[i]["id"] == "X001":
            sensor = data[i]['pir_records']
            json_dump = json.dumps(sensor)
            json_parsed = json.loads(json_dump)
            csvwriter = csv.writer(json_data)
            if len(sensor) > 0:
                for i in range(0,len(json_parsed)):
                    csvwriter.writerow(json_parsed[i].values())

    json_data.close()

    return ('sensors.csv')

def getevents(url):
    event = requests.get(url).json()

    json.dump = json.dumps(event)
    json_parsed = json.loads(json.dump)
    json_data = open('events.csv', 'w')
    csvwriter = csv.writer(json_data)

    header = json_parsed[0].keys()
    csvwriter.writerow(header)
    for i in range(0,len(json_parsed)):
        csvwriter.writerow(json_parsed[i].values())

    json_data.close()

    return ('events.csv')

def s3(file):
    cmd = 'aws s3 cp {} s3://cs462g3'.format(file)
    os.system(cmd)
    return

def main():
    baseURL = 'http://3.86.89.118:5000'
    meetingRoom = baseURL + '/occupancy'
    print("meeting room called")
    getoccupancy(meetingRoom)
    s3(getoccupancy(meetingRoom))
    print("uploaded on s3")
    sensorHealth = baseURL + '/sensor-health-debug'
    print("sensor health called")
    s3(getsensorhealth(sensorHealth))
    print("uploaded on s3")
    events = baseURL + '/event'
    print("events called")
    s3(getevents(events))
    print("uploaded on s3")

while True:
    main()
    time.sleep(300)