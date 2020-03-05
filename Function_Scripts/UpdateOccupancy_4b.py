import psycopg2

from datetime import datetime
from pytz import timezone
import pytz

import requests

#date time, __future__ is a lib
from __future__ import division
import datetime

##reference to 5a's py file and its function
from CalendarAPI_5a import *

#reference to Sub_3.py and its funciton
from Sub_3 import *

##import database
from models import db
from models import *


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


def check_change():
    ##1. want to find out which are the new datas in the records db.
    ##  compare the ids that are in record db and the ids of those in occupancy db

    #get all ids in records db (integer value)
    cur.execute('SELECT ("id") FROM record')
    ids_records = cur.fetchall() #fetches multuple rows and store the result in a list variable
    # ids_records = db.session.query(Record.id).all() 


    #get all ids in Occupancy db
    cur.execute('SELECT ("id") FROM occupancy')
    ids_occupancy = cur.fetchall()
    print(ids_occupancy)
    # ids_occupancy = db.session.query(Occupancy.id).all() #will return tuple
    # ids_occupancy = [Occupancy.id for each in ids_occupancy] #returns list
    #because the ids in occupancy will be combined for the nett value, only the largest id value in neet value will be added to db
    #eg ids_occupancy = [1,12,16]







    # latest_occu_id = ids_occupancy[-1] #ie 16

    # #find the new records in the records db
    # #ids_records eg: [1,2,3,4,5,6,7,8........,16,17,18,19]
    # new_entries = []
    # for each_record in ids_records: #to be changed later
    #     if each_record>latest_occu_id:#ie record's id which is greater than 16
    #         new_entries.append(each_record)

    # #get detailed records of all new entreies with reference to the new_entries
    # #ie: id of entry, value (actual sensor reading in cm ), timestamp, sensor_id
    
    # cur.execute('SELECT * FROM record ')
    # all_new_details = Record.query.filter(Record.id.in_(new_entries)).all()
    # # in the case that recor has a json field: all_new_details = Record.query.filter(Record.data['key].in_(new_entries)).all()

    # details_list = []
    # #save the entries into a dictionary
    # # ie: [{id:_,value:_,timestamp:_,sensor_id:_}, 
    # #       id:_,value:_,timestamp:_,sensor_id:_}, 
    # #       id:_,value:_,timestamp:_,sensor_id:_}.....]
    # for details in all_new_details:
    #     new = (f"<id={details.id}, value={details.value}, timestamp={details.timestamp}, sensor_id={details.sernsor_id}>")
    #     details_list.append(new) #output: [{..,..,..},{},{}]
    

    # '''
    # --DETERMINE IF PEOPLE ARE WALKING IN/OUT/NOISE--
    
    # Possible scenarios
    # 1. there may be multiple readings(eg: 1,2,3,4) when a person passes through 1 of the sensor 
    # 2. there may be only a single reading (eg: 1) when a person passes through 1 of the sesnsor
    # 3. a person is just a noise, goes through 1 sensor but not the other
    # 4. readings still coming in when the data is 0
    
    # '''
    # # empty_readings = [] #detailed readings of all the times no one passes through
    # # position_index = [] #index of these detailed readings in the details_list
    # num_details = len(details_list)
    # #get reading id where there is no one passing through 
    # # for i in range(0,num_details):
    # #     if details_list[i]['value']==89:
    # #         empty_readings.append(details_list[i])  #save the dict entry to new list
    # #         position_index.append(i)  #record the index of it

    # #possible to find two consecutive readings with mac address out and then in(person walking in) and with mac adress in then out(person walking out)
    # ###to get the current reading occupancy in database 
    # #get the possible 2 mac address
    # # will be saved into a list 

    # #mac_1 is the one outside, mac_2 will be in the one inside
    # sensor_id_list = [mac_1, mac_2]   #to be changed later to reference

    # counter = 0
    # pairs_in_out = []
    # previous_record = {}

    # while (counter<num_details):
    #     id_current = details_list[counter]['id']
    #     value_current = details_list[counter]['value']
    #     time_current = details_list[counter]['timestamp']
    #     sensor_id_current = details_list[counter]['sensor_id']
    #     if counter==0:
    #         #initialise a previous records dictionary to compare to the current one
    #         previous_record = {'id':id_current, 'value': value_current, 'timestamp':time_current, 'sensor_id':sensor_id_current}
    #         counter +=1
    #     elif counter>0:
    #         #########change time to pytz kind
    #         time_difference = time_current - previous_record['timestamp']
    #         #means that there is a change// means that there is someone passing through both sensors
    #         ((previous_record['sensor_id']) != sensor_id_current) and (previous_record['value']!=89) and (value_current!=89) and (time_difference<=120)
    #         pairs_in_out.append([(previous_record['sensor_id']), sensor_id_current])
    #         previous_record = {'id':id_current, 'value': value_current, 'timestamp':time_current, 'sensor_id':sensor_id_current}
    #         counter +=1

    
    # #find number who enter and exit
    # human_traffic = 0
    # if len(previous_record)!=0:
    #     for pairs in previous_record:
    #         first = pairs[0]
    #         second = pairs[1]
    #         if (first == sensor_id_list[0]) and (second == sensor_id_list[1]):
    #             human_traffic +=1
    #         elif (first ==sensor_id_list[1]) and (second==sensor_id_list[0]):
    #             human_traffic -=1

    # #previous_occupancy
    # previous_occupancy = db.session.query(Occupancy).order_by(Occupancy.value.desc()).first()
    # new_occupancy = previous_occupancy + human_traffic
    # if new_occupancy <= 0:
    #     new_id = new_entries[-1] #the last id in the list of all new ids
    #     time = details_list[-1]['timestamp']   #the last timestamp in the details_list,new_id and time will have reference to dsam detail
    #     meeting_room_id = 'G' #to be changed later
    #     getCalendarEvents() #reference to CalendarAPI
    #     new_occupancy_entry = Occupancy(new_id, time, meeting_room_id, new_occupancy)
    #     db.session.add(new_occupancy_entry)
    #     db.session.commit()
    # elif new_occupancy>=1:
    #     new_id = new_entries[-1] #the last id in the list of all new ids
    #     time = details_list[-1]['timestamp']   #the last timestamp in the details_list,new_id and time will have reference to dsam detail
    #     meeting_room_id = 'G' #to be changed later
    #     new_occupancy_entry = Occupancy(new_id, time, meeting_room_id, new_occupancy)
    #     db.session.add(new_occupancy_entry)
    #     db.session.commit()

            

            
                
        
















# def check_occupancy(on_message):
#     '''
#     trigger: when new reading is recorded in db
#     function will take in the trigger and see if there is a change in occupnacy
#     if there is a change, save the number
#     if occupancy is 0, will call function 5a before adding new occupancy data into the ocupancy database
#     else add the new occupancy data into database

#     TBC
#     if function_3 returns -1 --> 1 person leaves
#     if function_3 returns 1--> 1 person enters

#     determine if there's a change in occupancy, and if yes, what's the new
#     occupany. and push it back into the db

#     '''
#     #get all the records
#     all_records = record.query(id,value,timestamp,sensor_id).filter_by(id).all()

#     #get latest 2 readings from recordy db
#     if len(all_records)>=2: #ensures that comparison will not be done is 0/1 records only
#         latest_record = all_records[-1]
#         sec_latest_record = all_records[-2]

#     #need to add in an additional part where we check which sensor will be triggered




#     #if occupancy is 0, call Calendar API and update Occupancy database
#     if latest_record[1]==0:
#         new_time_stamp= latest_record[2]
#         getCalendarEvents(creds())
#         new_entry = Occupancy('',new_time_stamp,'',0)
#         db.session.add(new_entry)
#         db.session.commit()

#     #check if readings changed in records db
#     elif latest_record[1] != sec_latest_record[1]:
#         new_time_stamp= latest_record[2]
#         #positive occu_change means someone entered
#         #negative occu_change means someone left
#         occu_change = (sec_latest_record[1]-latest_record[1])
#         #add occupancy db
#         new_entry = Occupancy('',new_time_stamp,'',0)
#         db.session.add(new_entry)
#         db.session.commit()
