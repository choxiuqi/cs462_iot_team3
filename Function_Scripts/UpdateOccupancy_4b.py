##reference to 5a's py file and its function
from CalendarAPI_5a import *
##reference to 3a's py file and its function
from Sub_3 import on_message
##import database
from models import db
from models import *
##import time
from datetime import datetime
from pytz import timezone

def check_occupancy(on_message):
    '''
    trigger: when new reading is recorded in db
    function will take in the trigger and see if there is a change in occupnacy
    if there is a change, save the number
    if occupancy is 0, will call function 5a before adding new occupancy data into the ocupancy database
    else add the new occupancy data into database

    TBC
    if function_3 returns -1 --> 1 person leaves
    if function_3 returns 1--> 1 person enters

    determine if there's a change in occupancy, and if yes, what's the new
    occupany. and push it back into the db

    '''
    #get all the records
    all_records = record.query(id,value,timestamp,sensor_id).filter_by(id).all()

    #get latest 2 readings from recordy db
    if len(all_records)>=2: #ensures that comparison will not be done is 0/1 records only
        latest_record = all_records[-1]
        sec_latest_record = all_records[-2]

    #need to add in an additional part where we check which sensor will be triggered




    #if occupancy is 0, call Calendar API and update Occupancy database
    if latest_record[1]==0:
        new_time_stamp= latest_record[2]
        getCalendarEvents(creds())
        new_entry = Occupancy('',new_time_stamp,'',0)
        db.session.add(new_entry)
        db.session.commit()

    #check if readings changed in records db
    elif latest_record[1] != sec_latest_record[1]:
        new_time_stamp= latest_record[2]
        #positive occu_change means someone entered
        #negative occu_change means someone left
        occu_change = (sec_latest_record[1]-latest_record[1])
        #add occupancy db
        new_entry = Occupancy('',new_time_stamp,'',0)
        db.session.add(new_entry)
        db.session.commit()
