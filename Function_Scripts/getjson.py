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



# def getoccupancy(url):
#     occupancy = requests.get(url).json()
#     for i in occupancy:
#         occ_dict = json.dumps(i)
#         dictionary = json.loads(occ_dict)
#         with open('occupancy.csv', 'a') as f1:
#             for key in dictionary.keys():
#                 f1.write("%s, %s\n"%(key, dictionary[key]))
#     return ('occupancy.csv') 

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

    # for a in occupancy:
    #     json_parsed = json.loads(str(a))
    #     getoccupancy_data = open('occupancy.csv', 'w')
    #     csvwriter = csv.writer(getoccupancy_data)
    #     count = 0
    #     for i in json_parsed:
    #         if count == 0:
    #             header = i.keys()
    #             csvwriter.writerow(header)
    #             count += 1
    #         csvwriter.writerow(i.values())
    #     getoccupancy_data.close()


def getsensorhealth(url):
    data = requests.get(url).json()
    for i in range(0, len(data)):
        sensor = data[i]['sensor_health']
        json.dump = json.dumps(sensor)
        json_parsed = json.loads(json.dump)
        json_data = open('sensor.csv', 'w')
        csvwriter = csv.writer(json_data)
        if len(sensor) > 0:
            header = json_parsed[0].keys()
            csvwriter.writerow(header)
            for i in range(0,len(json_parsed)):
                csvwriter.writerow(json_parsed[i].values())
            # print(i, json_parsed[i].values())
        json_data.close()
        # for i in sensor:
        #     sensor_dict = json.dumps(i)
        #     sensors = json.loads(sensor_dict)
        # # with open('sensors.json', 'w') as f2:
        # #     json.dump(uss_in, f2)
        #     with open('sensors.csv', 'a') as f2:
        #         for key in sensors.keys():
        #             f2.write("%s, %s\n"%(key, sensors[key]))
    return ('sensors.csv')

def getevents(url):
    event = requests.get(url).json()
    # with open('events.json', 'w') as f3:
    #     json.dump(events, f3)
    json.dump = json.dumps(event)
    json_parsed = json.loads(json.dump)
    json_data = open('event.csv', 'w')
    csvwriter = csv.writer(json_data)

    header = json_parsed[0].keys()
    csvwriter.writerow(header)
    for i in range(0,len(json_parsed)):
        csvwriter.writerow(json_parsed[i].values())
        # print(i, json_parsed[i].values())
    json_data.close()


    # for i in event:
    #     event_dict = json.dumps(i)
    #     events = json.loads(event_dict)
    #     with open('events.csv', 'w') as f3:
    #         for key in events.keys():
    #             if key != "id":
    #                 f3.write("%s, %s\n"%(key, events[key]))
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
    s3(getoccupancy(meetingRoom))
    print("uploaded on s3")
    sensorHealth = baseURL + '/sensor-health'
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