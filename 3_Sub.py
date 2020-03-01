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
    # print("message received")
    # data = message.payload.decode("utf-8").replace("'", '"')
    # msg = json.loads(data)
    # print(msg)
    # for i in range(len(msg['result'])):
    #     timestamp_unix = msg['timestamp']
    #     timestamp = datetime.utcfromtimestamp(timestamp_unix)
    #     MAC_address = msg['id']
    #     sensorType = msg['result'][i]['type']
    #     reading = float(msg['result'][i]['reading'])
    #     if sensorType == 'light':
    #         if reading < 59:
    #             description = 'Low'
    #         elif reading <= 150:
    #             description = 'Optimal'
    #         else:
    #             description = 'High'
    #     elif sensorType == 'temp':
    #         if reading < 23:
    #             description = 'Low'
    #         elif reading <= 25:
    #             description = 'Optimal'
    #         else:
    #             description = 'High'
    #     elif sensorType == 'humidity':
    #         if reading < 40:
    #             description = 'Low'
    #         elif reading <= 60:
    #             description = 'Optimal'
    #         else:
    #             description = 'High'
    #     try:
    #         print("executing")
    #         cur.execute("INSERT INTO sensor_reading VALUES (DEFAULT, %s, %s, %s, %s, %s);",(timestamp, sensorType, MAC_address, reading, description))
    #         conn.commit()
    #         print("committed")
    #         cur.execute('INSERT INTO latest_sensor_reading VALUES (DEFAULT, %s, %s, %s, %s, %s) ON CONFLICT ("sensorType" ,"MAC_address") DO UPDATE SET timestamp = %s, reading = %s, description = %s;',(timestamp, sensorType, MAC_address, reading, description, timestamp, reading, description))
    #         conn.commit()
            
    #         # if (sensorType == 'light' or sensorType == 'temp') and (description == 'Low' or description == 'High'):
    #         if (sensorType == 'light') and (description == 'High'):
    #             try:
    #                 cur.execute('SELECT "readingID" FROM sensor_reading ORDER BY "readingID" DESC;')
    #                 readingID = cur.fetchone()[0]
    #                 cur.execute('SELECT "MAC_address", "sensorType", description FROM sensor_reading WHERE "readingID" = %s;',(readingID,))
    #                 retrieved = cur.fetchone()
    #                 sensorType = retrieved[1]
                    
    #                 cur.execute('SELECT "building", "level", "area" FROM sensor, location WHERE sensor."sensorLocationID" = location."sensorLocationID" and sensor."MAC_address" =%s;',(MAC_address,))
    #                 location = cur.fetchone()
                    
    #             except Exception as e:
    #                 print(str(e))

    #             create_ticket(readingID, description, sensorType,location)
                
            
        except Exception as e:
            return(str(e))

Connected = False   #global variable for the state of the connection
 
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