##reference to 5a's py file and its function
from CalendarAPI_5a import *

##import database
from models import db
from models import *



#record- raw sensor data, ingsin coding, sensor reading, macaddress from sensor to 
# know which sensor it is

##my part. use data from record to write function to update occupancy table
#occupancy- current occupancy in the meeting room 

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
def check_occupancy():
    ##1. want to find out which are the new datas in the records db.
    ##  compare the ids that are in record db and the ids of those in occupancy db

    #get all ids in records db (integer value)
    ids_records = db.session.query(Record.id).all() #will return tuple
    ids_records = [re.id for each in ids_records] #returns list
    #alterantive:
    #use with_entities to get spcific columns 
    #ids_records = Record.query.with_entities(Record.col1) or ids_records = Record.query.with_entities(Record.id).all()


    #get all ids in Occupnacy db
    ids_occupancy = db.session.query(Occupancy.id).all() #will return tuple
    ids_occupancy = [occ.id for each in ids_occupancy] #returns list
    # Alternative
    # ids_occupancy = Occupancy.query.with_entities(Occupancy.col1)
    #because the ids in occupancy will be combined for the nett value, only the largest id value in neet value will be added to db
    #eg ids_occupancy = [1,12,16]
    latest_occu_id = ids_occupancy[-1] #ie 16

    #find the new records in the records db
    #ids_records eg: [1,2,3,4,5,6,7,8........,16,17,18,19]
    new_entries = []
    for each_record in ids_records:
        if each_record>latest_occu_id:#ie record's id which is greater than 16
            new_entries.append(each_record)

    #get detailed records of all new entreies with reference to the new_entries
    #ie: id of entry, value (actual sensor reading in cm ), timestamp, sensor_id
    all_new_details = Record.query.filter(Record.id.in_(new_entries)).all()
    # in the case that recor has a json field: all_new_details = Record.query.filter(Record.data['key].in_(new_entries)).all()

    details_list = []
    #save the entries into a dictionary
    # ie: [{id:_,value:_,timestamp:_,sensor_id:_}, 
    #       id:_,value:_,timestamp:_,sensor_id:_}, 
    #       id:_,value:_,timestamp:_,sensor_id:_}.....]
    for details in all_new_details:
        new = (f"<id={details.id}, value={details.value}, timestamp={details.timestamp}, sensor_id={details.sernsor_id}>")
        details_list.append(new) #output: [{..,..,..},{},{}]
    

    '''
    --DETERMINE IF PEOPLE ARE WALKING IN/OUT/NOISE--
    
    Possible scenarios
    1. there may be multiple readings(eg: 1,2,3,4) when a person passes through 1 of the sensor 
    2. there may be only a single reading (eg: 1) when a person passes through 1 of the sesnsor
    3. a person is just a noise, goes through 1 sensor but not the other
    4. readings still coming in when the data is 0
    
    '''
    empty_readings = [] #detailed readings of all the times no one passes through
    position_index = [] #index of these detailed readings in the details_list
    num_details = len(details_list)
    #get reading id where there is no one passing through 
    for i in range(0,num_details):
        if details_list[i]['value']==89:
            empty_readings.append(details_list[i])  #save the dict entry to new list
            position_index.append(i)  #record the index of it

    #create empty list of list depending on number of position_indexs
    num_empty = len(position_index) #find the number of times there are no one entering 
    lists_empty = [[] for _ in range(num_empty)]

    #group the readings before each empty_reading and append to lists_empty
    location_in_postion_list = 0
    for detail in details_list:
        id_of_empty = details_list[position_index[location_in_postion_list]]
        if detail['id']<
















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
