''' This script will run continuosly and check for motion for the last 3 min
    if there is no motion for the last 3 min, we will reset the occupancy reading to 0
    this will replace the resetCounter() function in UpdateOccupancy_4b.py'''

import psycopg2
from datetime import datetime
import time
import requests
import json

# -----------------db--------------------------
conn = psycopg2.connect(host="127.0.0.1", dbname="cs462team3db", user="team3user", password="password")
# Cursor is created by the Connection object and using the Cursor object we will be able to execute our commands.
cur = conn.cursor()
conn.autocommit = True

# ----------------telebot -----------------------
chat_id = 344832007 # fill in your chat id here
api_token = '1101942872:AAE7Z80sUtx2KhWDmh-r7mATB0xM1EuV3a0' # fill in your api token here
url_base = 'https://api.telegram.org/bot{}/'.format(api_token)
url_getUpdates = '{}getupdates'.format(url_base)
url_sendMsg = '{}sendMessage'.format(url_base)


def check_reset():
    # print('function called...')
    cur.execute('SELECT "value", "timestamp" FROM pir_record ORDER BY id DESC LIMIT 3;')
    last_three_readings = cur.fetchall()    
    occupied_or_not = 0

    #finding the total movements
    for reading in last_three_readings:
        value = reading[0]
        occupied_or_not += value
    
    # print('final reading is: ', occupied_or_not,)

    #when there is a movement
    if occupied_or_not >0:
        # print("reset function done\n\n")
        return 

    #when there is no movement (occipied_or_not==1)
    else:
        # get current occupancy
        cur.execute('SELECT "value" FROM occupancy ORDER BY id DESC LIMIT 1;')
        last_occupancy = cur.fetchone()[0]
        # print("last_occupancy is:",last_occupancy)

        if last_occupancy > 0:
        # if current occupancy > 0
            timestamp = str(datetime.now())[0:19]        
            meeting_room_id = 'G'
            new_occupancy = 0
            remarks = "resetted"
            cur.execute("INSERT INTO occupancy VALUES (DEFAULT, %s, %s, %s, %s);",(timestamp, meeting_room_id, new_occupancy, remarks))
            # print('inserted reset into occupancy table \n\n')
            # return

        return
        # else:
        # if current occupancy = 0, do nothing
            # print("current occupancy is already 0")
            # return 

def check_sensor_health():
    ''' for pi and uss, readings must be less than 3 min from now
        else: we will add error msg: _____ sensor hasn't gotten a reading in the last 60 min'''

    errors = []

    # get reading for out USS
    cur.execute('select "timestamp" from sensor_health where "sensor_id" = \'pi123\' order by id desc limit 1;')
    last_pi_rec = cur.fetchone()[0]
    # print("current time:", datetime.now())
    # print("pi timestamp:", last_pi_rec)
    rpi_time_diff = (datetime.now() - last_pi_rec).total_seconds() / 60         # time difference in minutes
    # print ("rpi time diff:", rpi_time_diff, '\n')

    if (rpi_time_diff > 60):
        errors.append(("Raspberry pi",last_pi_rec)
    
    # get reading for in USS
    cur.execute('select "timestamp" from sensor_health where "sensor_id" = \'fb48fc3a6ee3\' order by id desc limit 1;')
    last_inUSS_rec = cur.fetchone()[0]

    # print("current time:", datetime.now())
    # print("in uss timestamp:", last_inUSS_rec)
    inUSS_time_diff = (datetime.now() - last_inUSS_rec).total_seconds() / 60         # time difference in minutes
    # print ("in uss time diff:", inUSS_time_diff, '\n')

    if (inUSS_time_diff < 60):
        errors.append(("Inside USS",last_inUSS_rec)

    # get reading for pir USS
    cur.execute('select "timestamp" from sensor_health where "sensor_id" = \'e6f5f2bb5b0e\' order by id desc limit 1;')
    last_outUSS_rec = cur.fetchone()[0]

    # print("current time:", datetime.now())
    # print("out uss timestamp:", last_outUSS_rec)
    outUSS_time_diff = (datetime.now() - last_outUSS_rec).total_seconds() / 60         # time difference in minutes
    # print ("out uss time diff:", outUSS_time_diff, '\n')

    if (outUSS_time_diff < 60):
        errors.append(("Outisde USS",last_outUSS_rec)

    # print(errors)
    error_msg = ""

    if len(errors) > 0:
        for error in errors:
            error_msg += error[0] + ", "
        error_msg.strip(", ")
        error_msg += "did not receive a reading in the last 60 min\n\n"   

        for error in errors:
            s = error[0] + " - last heartbeat received at: " + error[1] + "\n"
            error_msg += s

        error_msg.strip("\n")

        params = {'chat_id':chat_id, 'text':error_msg}
        r = requests.get(url=url_sendMsg, params = params)  
    
    ''' for pir, a bit more difficult.... perhaps don't do first'''


try:
    while True:
        for i in range(60):
            time.sleep(60)
            check_reset()

            if i == 59:
                check_sensor_health()


        ''' for debug: '''
        # check_reset()
        # check_sensor_health()
        # time.sleep(60)

except Exception as e:
    print(str(e))