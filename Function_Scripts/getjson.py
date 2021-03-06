import json
import requests
import os
import time
import subprocess
import csv
import datetime

def getoccupancy(url):
    occupancy = requests.get(url).json()
    # print(type(occupancy))
    json_dump = json.dumps(occupancy)
    json_parsed = json.loads(json_dump)
    # print(type(json_parsed))
    json_data = open('occupancy.csv', 'w')
    csvwriter = csv.writer(json_data)

    # header = json_parsed[0].keys()
    # csvwriter.writerow(header)
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
        # header = json_parsed[0].keys()
        # csvwriter.writerow(header)
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

    # header = json_parsed[0].keys()
    # csvwriter.writerow(header)
    for i in range(0,len(json_parsed)):
        csvwriter.writerow(json_parsed[i].values())

    json_data.close()

    return ('events.csv')

def s3(csvfile, folder):
    cmd = 'aws s3 cp {} s3://cs462-team3/{}/ --acl public-read'.format(csvfile, folder)
    # subprocess.call(cmd, shell=True)
    os.system(cmd)
    return

def main():
    # baseURL = 'http://3.86.89.118:5000'
    baseURL = 'http://172.31.95.27:5000'
    meetingRoom = baseURL + '/occupancy-debug'
    getoccupancy(meetingRoom)
    sensorHealth = baseURL + '/sensor-health-debug'
    getsensorhealth(sensorHealth)
    events = baseURL + '/event-debug' 
    getevents(events)
    
    # now = datetime.datetime.now()
    # if (now.hour >= 8 or now.hour <= 19) and now.weekday() <= 4:
    s3(getoccupancy(meetingRoom), 'occupancy')
    s3(getsensorhealth(sensorHealth), 'sensors')
    s3(getevents(events), 'events')

while True:
    main()
    time.sleep(900)