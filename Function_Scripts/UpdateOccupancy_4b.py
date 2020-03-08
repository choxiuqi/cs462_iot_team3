import psycopg2

from datetime import datetime
from pytz import timezone
import pytz

import requests

##reference to 5a's py file and its function
from CalendarAPI_5a import *


'''
assuming there are 3 people walking,
will have 6 new records, and push into records db
 
my function:
1. we now know that we have 6 new data. call the 6 new data. 
- i will be the only adding entries into the occupancy
- possible way to call the newest 6 data is to see which id is not in the occupancy db already

2. determine if people walking in/out/noise
- assumption that people will pass between the 2 seconds within 2 seconds frame

3. then add into the occupancy data base
- hold variables to see isit 2 people walking in and 1 out?
- then i get the nett number of people and then this nett data will
be entered into the occupancy db

'''

conn = psycopg2.connect(host="127.0.0.1", dbname="cs462team3db", user="team3user", password="password")
# Cursor is created by the Connection object and using the Cursor object we will be able to execute our commands.
cur = conn.cursor()
conn.autocommit = True


def UpdateOccupancy():
    ##1. want to find out which are the new datas in the records db.
    ##  compare the ids that are in record db and the ids of those in occupancy db

    #get all ids in Occupancy db
    cur.execute('SELECT ("id") FROM occupancy')
    ids_occupancy = cur.fetchall()
    all_ids_occupancy = [i[0] for i in ids_occupancy]


    latest_occu_id = all_ids_occupancy[-1] #ie 16

    #get detailed records of all new entreies with reference to the new_entries
    #ie: id of entry, value (actual sensor reading in cm ), timestamp, sensor_id
    cur.execute('SELECT * FROM record WHERE "id">%s;',(latest_occu_id,))
    details_list = cur.fetchall()
    # ouput of details_list = [(3, 74, datetime.datetime(2020, 3, 5, 16, 19, 7), 0), (4, 70, datetime.datetime(2020, 3, 5, 16, 19, 10), 0)]
    # list of tuples

    
    '''
    --DETERMINE IF PEOPLE ARE WALKING IN/OUT/NOISE--
    
    Possible scenarios
    1. there may be multiple readings(eg: 1,2,3,4) when a person passes through 1 of the sensor 
    2. there may be only a single reading (eg: 1) when a person passes through 1 of the sesnsor
    3. a person is just a noise, goes through 1 sensor but not the other
    4. readings still coming in when the data is 0
    
    '''
    num_details = len(details_list)


    #possible to find two consecutive readings with mac address out and then in(person walking in) and with mac adress in then out(person walking out)
    #out_mac is the one outside, in_mac will be in the one inside
    out_mac = "e6f5f2bb5b0e"
    in_mac = "fb48fc3a6ee3"

    counter = 0
    pairs_in_out = []
    previous_record = {}

    while (counter<num_details):
        id_current = details_list[counter][0]
        value_current = details_list[counter][1]
        time_current = details_list[counter][2]
        sensor_id_current = details_list[counter][3]
        if counter==0:
            #initialise a previous records dictionary to compare to the current one
            previous_record = {'id':id_current, 'value': value_current, 'timestamp':time_current, 'sensor_id':sensor_id_current}
            # output of print(previous_record): {'id': 3, 'value': 74, 'timestamp': datetime.datetime(2020, 3, 5, 16, 19, 7), 'sensor_id': 0}
            counter +=1
        elif counter>0:
            time_difference = (time_current - previous_record['timestamp']).total_seconds()
            #means that there is a change// means that there is someone passing through both sensors
            if ((previous_record['sensor_id']) != sensor_id_current) and (previous_record['value']!=89) and (value_current!=89) and (time_difference<=2):
                pairs_in_out.append([(previous_record['sensor_id']), sensor_id_current])
            previous_record = {'id':id_current, 'value': value_current, 'timestamp':time_current, 'sensor_id':sensor_id_current}
            counter +=1

    
    #find number of people who enter and exit
    human_traffic = 0
    if len(pairs_in_out)!=0:
        for pairs in pairs_in_out:
            first = pairs[0]
            second = pairs[1]
            if (first == out_mac) and (second == in_mac):
                human_traffic +=1
            elif (first == in_mac) and (second == out_mac):
                human_traffic -=1
    else:
        human_traffic = 0
    #print(human_traffic)




    #previous occupancy
    ####################edit code to include if there's nothing in database #######################
    
    # cur.execute('SELECT ("value") FROM occupancy;')
    # exist_one = cur.fetchone()
    # occupancy_list = cur.fetchall()[-1]
    # if exist_one == None:
    #     last_occupancy = 0
    # else:
    #     last_occupancy = occupancy_list[0]

    cur.execute('SELECT ("value") FROM occupancy;')
    occupancy_list = cur.fetchall()[-1]
    if occupancy_list == []:
        last_occupancy = 0
        #add an empty row into db
        new_id = 0
        time = 0
        meeting_room_id  = 'G'
        cur.execute("INSERT INTO occupancy VALUES (%s, %s, %s, %s);",(new_id, time, meeting_room_id, last_occupancy))
    else:
        last_occupancy = occupancy_list[0]

    # print("occup list: {}".format(occupancy_list))
    # print("last occup: {}".format(last_occupancy))
    

    new_occupancy = int(last_occupancy) + int(human_traffic)


    cur.execute('SELECT ("id", "timestamp") FROM record;')
    last_record_list = cur.fetchall()[-1][0][1:-1]
    # print("last_record_list: {}".format(last_record_list))
    last_record_list_new = last_record_list.split(",")

    new_id = last_record_list_new[0]
    time = last_record_list_new[1].strip('"')
    # print("new id: {}".format(new_id))
    # print("time: {}".format(time))
    
    meeting_room_id = 'G'

    if new_occupancy <= 0:
        getCalendarEvents() #reference to CalendarAPI
        cur.execute("INSERT INTO occupancy VALUES (%s, %s, %s, %s);",(new_id, time, meeting_room_id, new_occupancy))
    elif new_occupancy>=1:
        cur.execute("INSERT INTO occupancy VALUES (%s, %s, %s, %s);",(new_id, time, meeting_room_id, new_occupancy))
