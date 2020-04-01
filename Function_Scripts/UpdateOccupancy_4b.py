import psycopg2
from datetime import datetime
import requests
conn = psycopg2.connect(host="127.0.0.1", dbname="cs462team3db", user="team3user", password="password")
# Cursor is created by the Connection object and using the Cursor object we will be able to execute our commands.
cur = conn.cursor()
conn.autocommit = True

def resetCounter():
    print("Reset Counter called")
    #take the last 5 readings from pir_record table
    ## if value 0= no movement (in 1 1min frame) 1=movement(in that 1 1min frame)
    cur.execute('SELECT "value", "timestamp" FROM pir_record WHERE "sensor_id" = %s ORDER BY id DESC LIMIT 5;', ('X001'))
    last_five_readings_1 = cur.fetchall()
    cur.execute('SELECT "value", "timestamp" FROM pir_record WHERE "sensor_id" = %s ORDER BY id DESC LIMIT 5;', ('X002'))
    last_five_readings_2 = cur.fetchall()    
    occupied_or_not = 0

    #finding the total movements
    for reading in last_five_readings_1:
        value = reading[0]
        occupied_or_not += value

    for reading in last_five_readings_2:
        value = reading[0]
        occupied_or_not += value

    #when there is a movement
    if occupied_or_not >0:
        print("nobody in room")
        return 
    #when there is no movement (occipied_or_not==1)
    else:
        #post ocupancy 1 new row to make occupancy 0,
        time = max(last_five_readings_1[0][1], last_five_readings_2[0][1])
        print("final time in last 5 readings:",time)     
        meeting_room_id = 'G'
        new_occupancy = 0
        remarks = "resetted"
        cur.execute("INSERT INTO occupancy VALUES (DEFAULT, %s, %s, %s, %s);",(time, meeting_room_id, new_occupancy, remarks))
        print("got people, updated occupancy")
        return 

def checkMotion(new_occupancy):
    print("checkMotion called")
    '''
    function will be called when:
    1. the occupancy is <=0 to check if there is no one inside
    2. every 5 mins since calendar event start to see if there are people
    '''
    try:
        cur.execute('SELECT * FROM pir_record WHERE "sensor_id" = %sORDER BY "id" DESC;',('X001'))
        latest_pir_reading_1 = cur.fetchone()
    except Exception as e:
        return(str(e))

    try:
        cur.execute('SELECT * FROM pir_record WHERE "sensor_id" = %sORDER BY "id" DESC;',('X002'))
        latest_pir_reading_2 = cur.fetchone()
    except Exception as e:
        return(str(e))

    print("selected from pir_record - check motion")

    if latest_pir_reading_1[3]==0 and latest_pir_reading_2[3]==0:     
        return True #nobody in the room
    else:
        return False     #people in the room

def UpdateOccupancy():
    ##1. want to find out which are the new datas in the records db.
    ##  compare the ids that are in record db and the ids of those in occupancy db

    print("update occupancy called")

    cur.execute('SELECT * FROM latest_uss_record;')
    details_list = cur.fetchall()
    print("selected latest uss records")
    
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

    print("looking through counter now")

    while (counter<len(details_list)):
        id_current = details_list[counter][0]
        value_current = details_list[counter][1]
        time_current = details_list[counter][2]
        sensor_id_current = details_list[counter][3]

        if counter == 0:
            previous_record = {'id':id_current, 'value': value_current, 'timestamp':time_current, 'sensor_id':sensor_id_current}
            counter += 1

        else:
            time_difference = (time_current - previous_record['timestamp']).total_seconds()
            if ((previous_record['sensor_id']) != sensor_id_current) and (previous_record['value']!=89) and (value_current!=89) and (time_difference<=2):
                pairs_in_out.append([(previous_record['sensor_id']), sensor_id_current])
                previous_record = {'id':details_list[counter+1][0], 'value': details_list[counter+1][1], 'timestamp':details_list[counter+1][2], 'sensor_id':details_list[counter+1][3]}
                counter += 2
            else:
                previous_record = {'id':id_current, 'value': value_current, 'timestamp':time_current, 'sensor_id':sensor_id_current}
                counter += 1

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
    print("human traffic", human_traffic)

    cur.execute('SELECT value FROM occupancy;') 
    occupancy_list = cur.fetchall()[-1]
    last_occupancy = occupancy_list[0]

    new_occupancy = int(last_occupancy) + int(human_traffic)

    cur.execute('SELECT timestamp FROM latest_uss_record ORDER BY id DESC;')
    time = cur.fetchone()[0]
    meeting_room_id = 'G'

    if new_occupancy < 0:
        new_occupancy = 0
        remarks = 'calculated -ve occupancy'
        cur.execute("INSERT INTO occupancy VALUES (DEFAULT, %s, %s, %s, %s);",(time, meeting_room_id, new_occupancy, remarks))

    elif new_occupancy >=0:
        cur.execute("INSERT INTO occupancy VALUES (DEFAULT, %s, %s, %s);",(time, meeting_room_id, new_occupancy))

    return