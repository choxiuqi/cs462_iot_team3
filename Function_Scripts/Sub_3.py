import paho.mqtt.client as mqttClient
import time
from config import *
import json
import csv
import psycopg2
from datetime import datetime
from pytz import timezone
import pytz
import requests
from UpdateOccupancy_4b import UpdateOccupancy, resetCounter #to change to actual function name

conn = psycopg2.connect(host="127.0.0.1", dbname="cs462team3db", user="team3user", password="password")
# Cursor is created by the Connection object and using the Cursor object we will be able to execute our commands.
cur = conn.cursor()
conn.autocommit = True

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")

def commit_sensor_data(data):
    '''
    This function will push in ONLY USS sensor data into latest_record AND record tables
    When this function is called, it means that a person walking through the door is detected, and we want to find out if there is a change in occupancy.
    USS sensor data is collated every 30s from the first USS sensor data received FROM THE RPI

    '''
    # first delete old data from latest_record
    print("deleting from latest_uss_record")
    cur.execute("DELETE FROM latest_uss_record;")
    conn.commit()
    print("deleted from latest_uss_record")
    print("USS msg recevied: {}".format(data))

    for msg in data:
        # print("USS msg recevied: {}".format(msg))
        timestamp_unix = msg['result'][0]['timestamp']
        timestamp = datetime.utcfromtimestamp(timestamp_unix)
        MAC_address = msg['result'][0]['mac_add']
        value = float(msg['result'][0]['value'])
        # sensorType = 'USS'
        print("looked through USS variables")

        try:
            print("executing_record")
            cur.execute("INSERT INTO uss_record VALUES (DEFAULT, %s, %s, %s);",(value, timestamp, MAC_address))
            conn.commit()
            print("committed_record")
            print("executing_latest_record")
            cur.execute("INSERT INTO latest_uss_record VALUES (DEFAULT, %s, %s, %s);",(value, timestamp, MAC_address))
            conn.commit()
            print("committed_latest_record")               
            
        except Exception as e:
            return(str(e))

    UpdateOccupancy()

    return


def commit_pir_data(data, id):
    '''
    This function will push in only PIR sensor data in PIR_record(tentative, NEW!!)
    '''
    print("PIR msg recevied: {}".format(data))
    for msg in data:
        timestamp_unix = msg['result'][0]['timestamp']
        timestamp = datetime.utcfromtimestamp(timestamp_unix)
        MAC_address = id
        value = float(msg['result'][0]['value'])
        # sensorType = 'USS'
        print("looked through PIR variables")

        # not sure about the flow now..... but anw below shows inserting into db, and the very basic calling amelia's function
        try:
            print("executing_record")
            cur.execute("INSERT INTO PIR_record VALUES (DEFAULT, %s, %s, %s);",(timestamp, MAC_address, value))
            conn.commit()
            print("committed_record")               
            
        except Exception as e:
            return(str(e))

    resetCounter()

def commit_uss_health_data(data):
    '''
    This function will push in only sensor health data in sensor_health(tentative, NEW!!)
    ''' 
    print("USS_health msg recevied: {}".format(data))  
    for msg in data:
        timestamp_unix = msg['results'][0]['timestamp']
        timestamp = datetime.utcfromtimestamp(timestamp_unix)
        MAC_address = msg['results'][0]['mac_add']
        value = float(msg['results'][0]['value'])
        # sensorType = 'USS'
        print("looked through USS_health variables")

        # not sure about the flow now..... but anw below shows inserting into db, and the very basic calling amelia's function
        try:
            print("executing_record")
            cur.execute("INSERT INTO sensor_health VALUES (DEFAULT, %s, %s, %s);",(timestamp, MAC_address, value))
            conn.commit()
            print("committed_record")               
            
        except Exception as e:
            return(str(e))
    return 

def commit_rpi_health_data(data, id):
    '''
    This function will push in only sensor health data in sensor_health(tentative, NEW!!)
    '''
    print("raspberry pi health data received: {}".format(data))
    
    timestamp_unix = data[1]['timestamp']
    timestamp = datetime.utcfromtimestamp(timestamp_unix)
    MAC_address = id
    value = float(data[0]['value'])
    temperature = float(data[2]['temperature'])
    print("looked through raspberry pi variables")

    # not sure about the flow now..... but anw below shows inserting into db, and the very basic calling amelia's function
    try:
        print("executing_record")
        cur.execute("INSERT INTO sensor_health VALUES (DEFAULT, %s, %s, %s, %s);",(timestamp, MAC_address, value, temperature))
        conn.commit()
        print("committed_record")               
        
    except Exception as e:
        return(str(e))


    return



def on_message(client, userdata, message):
    print("subscriber message received")
    data = message.payload.decode("utf-8").replace("'", '"')
    # print(data)
    # for i2 in data:
    print("yes")
    i2 = json.loads(data)
    print("JSON sub data: {}".format(i2))
    

    # if sensor normal data --> call function commit_sensor_data()
    if i2["type"] == "ultrasonic":
        print("ultrasonic data received")
        commit_sensor_data(i2["result"])

    # if only pir data --> call function commit_pir_data()
        # need to add in part where data received is only PIR motion sensor data, nobody coming in or out
        # --> if data is that there is no motion, call the function resetCounter()

    if i2["type"] == "pir": # not sure what's the real var name
        print("PIR data received")
        commit_pir_data(i2["sensor_health"], i2["mac_add"])

    # if uss_health data --> call function commit_health_data()
    if i2["type"] == "ultrasonic_health":
        commit_uss_health_data(i2['sensor_health'])

    if i2["type"] == "raspberry pi":
        commit_rpi_health_data(i2['sensor_health'], i2["mac_add"])
    

    return

Connected = False   #global variable for the state of the connection
 
# need to update broker details
# broker_address= "52.77.224.134"  #Broker address
# broker_address="127.0.0.1"
broker_address = "broker.mqttdashboard.com"
port = 1883                          #Broker port
# port = 16179
user = ""                    #Connection username
password = ""            #Connection password
 
client = mqttClient.Client("yo")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
client.subscribe("cs462-team3")
print("subscribed")
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print("exiting")    
    client.disconnect()
    client.loop_stop()