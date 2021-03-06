import psycopg2
from datetime import datetime
# from pytz import timezone
# import pytz

import requests

#reference to 5a's py file and its function
# from CalendarAPI_5a import *



conn = psycopg2.connect(host="127.0.0.1", dbname="cs462team3db", user="team3user", password="password")
# Cursor is created by the Connection object and using the Cursor object we will be able to execute our commands.
cur = conn.cursor()
conn.autocommit = True

def resetCounter():
    print("reset Counter called")
    cur.execute('SELECT "value", "timestamp" FROM pir_record_debug ORDER BY id DESC LIMIT 5;')
    last_five_readings = cur.fetchall()
    print(last_five_readings)
    print("resetCounter - selected last 5 pir record")
    
    occupied_or_not = 0

    #finding the total movements
    for reading in last_five_readings:
        value = reading[0]
        occupied_or_not += value

    #when there is a movement
    if occupied_or_not >0:
        print("there is a movement, reset done")
        return 
    #when there is no movement (occipied_or_not==1)
    else:
        #post ocupancy 1 new row to make occupancy 0,
        time = last_five_readings[0][1]
        print("line 42- time is: ",time)        
        meeting_room_id = 'G'
        new_occupancy = 0
        remarks = "resetted"
        cur.execute("INSERT INTO occupancy_debug VALUES (DEFAULT, %s, %s, %s, %s);",(time, meeting_room_id, new_occupancy, remarks))
        print("inserted and reset done")
    return 

# resetCounter()

# def checkMotion(new_occupancy):
#     print("checkMotion called")
#     '''
#     function will be called when:
#     1. the occupancy is <=0 to check if there is no one inside
#     2. every 5 mins since calendar event start to see if there are people
#     '''
#     try:
#         cur.execute('SELECT * FROM pir_record ORDER BY "id" DESC;')
#         latest_pir_reading = cur.fetchone()
#         print('latest_pir_reading: ', latest_pir_reading)
#         print('latest_pir_reading[3]: ',latest_pir_reading[3])
#     except Exception as e:
#         return(str(e))

#     print("selected from pir_record - check motion")

#     if latest_pir_reading[3]==0:     
#         return True #nobody in the room
#     else:
#         return False     #people in the room

# checkMotion()

def UpdateOccupancy():
    ##1. want to find out which are the new datas in the records db.
    ##  compare the ids that are in record db and the ids of those in occupancy db

    #get all the ids from latest_record db
    print("Update Occupancy called")
    cur.execute('SELECT * FROM latest_uss_record;')
    details_list = cur.fetchall()
    #OUTPUT [(3, 74, datetime.datetime(2020, 3, 5, 16, 19, 7), 0), (4, 70, datetime.datetime(2020, 3, 5, 16, 19, 10), 0)]
    print("selected all from latest_uss_record")
    
    '''
    --DETERMINE IF PEOPLE ARE WALKING IN/OUT/NOISE--
    
    Possible scenarios
    1. there may be multiple readings(eg: 1,2,3,4) when a person passes through 1 of the sensor 
    2. there may be only a single reading (eg: 1) when a person passes through 1 of the sesnsor
    3. a person is just a noise, goes through 1 sensor but not the other
    4. readings still coming in when the data is 0
    
    '''
    #possible to find two consecutive readings with mac address out and then in(person walking in) and with mac adress in then out(person walking out)
    #out_mac is the one outside, in_mac will be in the one inside
    out_mac = "e6f5f2bb5b0e"
    in_mac = "fb48fc3a6ee3"

    counter = 0
    pairs_in_out = []
    previous_record = {}

    print("find 2 consecutive reading pairs")

    while (counter<len(details_list)):
        id_current = details_list[counter][0]
        value_current = details_list[counter][1]
        time_current = details_list[counter][2]
        sensor_id_current = details_list[counter][3]
        print("counter: ",counter)

        if counter == 0:
            previous_record = {'id':id_current, 'value': value_current, 'timestamp':time_current, 'sensor_id':sensor_id_current}
            print("line 118 prev record: ",previous_record)
            counter += 1

        else:
            time_difference = (time_current - previous_record['timestamp']).total_seconds()
            if ((previous_record['sensor_id']) != sensor_id_current) and (previous_record['value']!=89) and (value_current!=89) and (time_difference<=2):
                pairs_in_out.append([(previous_record['sensor_id']), sensor_id_current])
                previous_record = {'id':details_list[counter+1][0], 'value': details_list[counter+1][1], 'timestamp':details_list[counter+1][2], 'sensor_id':details_list[counter+1][3]}
                print("line 125 prev record: ",previous_record)
                counter += 2
            else:
                previous_record = {'id':id_current, 'value': value_current, 'timestamp':time_current, 'sensor_id':sensor_id_current}
                print("line 129 prev record: ",previous_record)
                counter += 1

    print("finding ppl in/out")    
    #find number of people who enter and exit
    human_traffic = 0
    if len(pairs_in_out)!=0:
        for pairs in pairs_in_out:
            first = pairs[0]
            second = pairs[1]
            print("first: ",first)
            print("second: ",second)
            if (first == out_mac) and (second == in_mac):
                human_traffic +=1
            elif (first == in_mac) and (second == out_mac):
                human_traffic -=1
    else:
        human_traffic = 0
    #print(human_traffic)

    print("selecting value from occupancy")

    cur.execute('SELECT value FROM occupancy;') 
    occupancy_list = cur.fetchall()[-1]
    # print("occupancy_list: {}".format(occupancy_list))
    print("selected value from occupancy - line 156")
    last_occupancy = occupancy_list[0]
    # print("occup list: {}".format(occupancy_list))
    # print("last occup: {}".format(last_occupancy))
    
    new_occupancy = int(last_occupancy) + int(human_traffic)

    print("selecting timestamp from latest_uss_record")
    cur.execute('SELECT timestamp FROM latest_uss_record ORDER BY id DESC;')
    time = cur.fetchone()[0]
    print("selected timestamp frm l_u_r: {}".format(time))
    # time = last_record_list[2]
    meeting_room_id = 'G'
  
    if new_occupancy < 0:
        print("new occupancy detected negative change")
        new_occupancy = 0
        remarks = 'calculated -ve occupancy'
        cur.execute("INSERT INTO occupancy_debug VALUES (DEFAULT, %s, %s, %s, %s);",(time, meeting_room_id, new_occupancy, remarks))
        print('inserted 0 instead of negative value')

        # if checkMotion(new_occupancy)== True:  #there's no one
        #     print("line 192 - there is no one")
        #     # getCalendarEvents() #reference to CalendarAPI (to be changed)
        #     # cur.execute("INSERT INTO occupancy VALUES (DEFAULT, %s, %s, %s);",(time, meeting_room_id, new_occupancy))
        # elif checkMotion(new_occupancy)== False:
        #     new_occupancy += 1
        #     print('line 197 - new occupancy is: ',new_occupancy)
        #     # cur.execute("INSERT INTO occupancy VALUES (DEFAULT, %s, %s, %s);",(time, meeting_room_id, new_occupancy))

    elif new_occupancy >=0:
        cur.execute("INSERT INTO occupancy_debug VALUES (DEFAULT, %s, %s, %s);",(time, meeting_room_id, new_occupancy))
        print("line 202- new occupancy is more than more and the new occupancy is: ", new_occupancy)

    print("line inserted into occ")
    print("new occupancy is: {}".format(new_occupancy))
    print("num pairs", len(pairs_in_out))
    return


UpdateOccupancy()