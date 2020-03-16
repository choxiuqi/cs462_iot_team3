import json
import requests
import os
import time
import subprocess
import csv

def tocsv(msg):
    input_file = msg + '.json'
    output_file = msg + '.csv'
    data = json.loads(input_file)
    with open(output_file, 'w') as f2:
        csvwriter = csv.writer(f2)
        count = 0
        for i in data:
            if count == 0:
                header = data.keys()
                csvwriter.writerow(header)
                count += 1
            csvwriter.writerow(data.values())
    return (output_file)



def getoccupancy(url):
    occupancy = requests.get(url).json()[0]
    occ_dict = json.dumps(occupancy)
    dictionary = json.loads(occ_dict)


    # with open('occupancy.json', 'w') as f1:
    #     json.dump(occupancy, f1)

    # with open('occupancy.csv', 'w') as f1:
    #     for key in dictionary.keys():
    #         f1.write("%s, %s\n"%(key, dictionary[key]))

        # f1.write("id", "meeting_room_id", "timestamp", "value", '\n')
        # for i in occupancy:
        #     for k,v in i.items():
        #         f1.write(v)
        # json.dump(occupancy, f1)
    print(dictionary)
    return occupancy

def getsensorhealth(url):
    sensors = requests.get(url).json()[0]['sensor_health']
    # with open('sensors.json', 'w') as f2:
    #     json.dump(uss_in, f2)
    with open('sensors.csv', 'w') as f2:
        for key in sensors.keys():
            f1.write("%s, %s\n"%(key, sensors[key]))
    return ('sensors.csv')

def getevents(url):
    events = requests.get(url).json()
    # with open('events.json', 'w') as f3:
    #     json.dump(events, f3)
    with open('events.csv', 'w') as f3:
        for i in events:
            for key in i.keys():
                f3.write("%s, %s\n"%(key, i[key]))
        # for i in events:
        #     f3.write(i)
    return ('events.csv')

def s3(file):
    cmd = 'aws s3 cp {} s3://cs462g3'.format(file)
    os.system(cmd)
    return

def main():
    baseURL = 'http://3.80.134.50:5000'
    meetingRoom = baseURL + '/occupancy'
    print("meeting room called")
    getoccupancy(meetingRoom)
    # s3(getoccupancy(meetingRoom))
    # print("uploaded on s3")
    # sensorHealth = baseURL + '/sensor-health'
    # print("sensor health called")
    # s3(getsensorhealth(sensorHealth))
    # print("uploaded on s3")
    # events = baseURL + '/event'
    # print("events called")
    # s3(getevents(events))
    # print("uploaded on s3")

while True:
    main()
    time.sleep(300)