''' This script will run continuosly and check for motion for the last 3 min
    if there is no motion for the last 3 min, we will reset the occupancy reading to 0
    this will replace the resetCounter() function in UpdateOccupancy_4b.py'''

import psycopg2
from datetime import datetime
import time
import requests
conn = psycopg2.connect(host="127.0.0.1", dbname="cs462team3db", user="team3user", password="password")
# Cursor is created by the Connection object and using the Cursor object we will be able to execute our commands.
cur = conn.cursor()
conn.autocommit = True

def check_reset():
    print('function called...')
    cur.execute('SELECT "value", "timestamp" FROM pir_record_debug ORDER BY id DESC LIMIT 3;')
    last_three_readings = cur.fetchall()    
    occupied_or_not = 0

    #finding the total movements
    for reading in last_three_readings:
        value = reading[0]
        occupied_or_not += value
    
    print('final reading is: ', occupied_or_not,)

    #when there is a movement
    if occupied_or_not >0:
        print("reset done\n\n")
        return 
    #when there is no movement (occipied_or_not==1)
    else:
        #post ocupancy 1 new row to make occupancy 0,
        # time = last_three_readings[0][1]
        timestamp = time.now()        
        meeting_room_id = 'G'
        new_occupancy = 0
        remarks = "resetted"
        cur.execute("INSERT INTO occupancy_debug VALUES (DEFAULT, %s, %s, %s, %s);",(timestamp, meeting_room_id, new_occupancy, remarks))
        print('inserted reset into occupancy table \n\n')
        return 


try:
    while True:
        time.sleep(60)
        check_reset()

except Exception as e:
    print(str(e))