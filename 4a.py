##to be changed later to reference to 5a's py file and its function
from file_5a import function_5a
##to be changed later to reference to 3a's py file and its function
from file_3 import function_3

def check_occupancy(function_3):
    '''
    trigger: when new reading is recorded in db
    function will take in the trigger and see if there is a change in occupnacy
    if there is a change, save the number
    if occupancy is 0, will call function 5a before updating the database
    else update database

    TBC
    if function_3 returns -1 --> 1 person leaves
    if function_3 returns 1--> 1 person enters
    '''
    ##query from database 
    #previous_reading = Record.query.filter(Record.value).first()

    ## to be change to reference to 3's py file function later
    current_reading = previous_reading + function_3
    if current_reading ==0:
        #call function_5a to be changed later
        function_5a ()
        #update MeetingRoom db. column current_occupancy
        update = MeetingRoom.query.filter_by(id).first()
        update.current_occupancy = current_reading
        db.session.commit()
        return current_reading
    else:
        #update MeetingRoom db. column current_occupancy
        update = MeetingRoom.query.filter_by(id).first()
        update.current_occupancy = current_reading
        db.session.commit()
        return current_reading




    
