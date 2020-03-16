import json
import requests
import os
import time
import subprocess

def getoccupancy(url):
    occupancy = requests.get(url).json()
    with open('occupancy.json', 'w') as f1:
        json.dump(occupancy, f1)
    return ('occupancy.json')

def getsensorhealth(url):
    uss_in = requests.get(url).json()[0]['sensors']['sensor_health']
    with open('sensors.json', 'w') as f2:
        json.dump(uss_in, f2)
    return ('sensors.json')

def getevents(url):
    events = requests.get(url).json()
    with open('events.json', 'w') as f3:
        json.dump(events, f2)
    return ('events.json')

def s3(file):
    cmd = 'aws s3 cp {} s3://cs462g3'.format(file)
    subprocess.check_output(cmd, shell=True)
    return

def main():
    baseURL = 'http://52.87.236.66:5000'
    meetingRoom = baseURL + '/occupancy'
    print("meeting room called")
    s3(getoccupancy(meetingRoom))
    print("uploaded on s3")
    # sensorHealth = baseURL + '/sensor-health'
    events = baseURL + '/event'
    print("events called")
    # s3(getsensorhealth(sensorHealth))
    s3(getevents(events))
    print("uploaded on s3")

while True:
    main()
    time.sleep(300)