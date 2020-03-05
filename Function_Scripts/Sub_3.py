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
from UpdateOccupancy_4b import check_occupancy #to change to actual function name

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

def on_message(client, userdata, message):
    print("message received")
    data = message.payload.decode("utf-8").replace("'", '"')
    for i2 in data:
        msg = json.loads(i2)
        print(msg)
        for i in range(len(msg['result'])):
            timestamp_unix = msg['timestamp']
            timestamp = datetime.utcfromtimestamp(timestamp_unix)
            MAC_address = msg['id']
            sensorType = msg['result'][i]['type']
            value = float(msg['result'][i]['reading'])

            try:
                print("executing")
                cur.execute("INSERT INTO record VALUES (DEFAULT, %s, %s, %s);",(value, timestamp, MAC_address))
                conn.commit()
                print("committed")

                # call (function from) 4b.py file
                UpdateOccupancy() #to change to actual function name
                    
                
            except Exception as e:
                return(str(e))

    return

Connected = False   #global variable for the state of the connection
 
# need to update broker details
# broker_address= "52.77.224.134"  #Broker address
# broker_address="127.0.0.1"
broker_address = "tailor.cloudmqtt.com"
# port = 1883                          #Broker port
port = 16179
user = "smt203team2"                    #Connection username
password = "smt203team2"            #Connection password
 
client = mqttClient.Client("yo")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
client.subscribe("test")
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