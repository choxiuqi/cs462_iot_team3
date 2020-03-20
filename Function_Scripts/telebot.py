import psycopg2
from datetime import datetime
from pytz import timezone
import time
import requests
import json

# -----------------db--------------------------
conn = psycopg2.connect(host="127.0.0.1", dbname="cs462team3db", user="team3user", password="password")
# Cursor is created by the Connection object and using the Cursor object we will be able to execute our commands.
cur = conn.cursor()
conn.autocommit = True

# ----------------telebot -----------------------
# chat_id = 344832007 # fill in your chat id here (XQ)
# chat_id = -472331637    #(grp)
api_token = '1101942872:AAE7Z80sUtx2KhWDmh-r7mATB0xM1EuV3a0' # fill in your api token here
url_base = 'https://api.telegram.org/bot{}/'.format(api_token)
url_getUpdates = '{}getupdates'.format(url_base)
url_sendMsg = '{}sendMessage'.format(url_base)

prev_msg_id = ''
# prev_reply = ''

# ##################################################################################################################################
def check_text():
    r = requests.get(url_getUpdates)
    d = r.json()

    global prev_msg_id
    # global prev_reply
    msg_text = ''
    
    current_msg = d['result'][-1]
    print(current_msg)
    
    current_msg_id = current_msg['message']['message_id']
    if current_msg_id != prev_msg_id:
        msg_text = current_msg['message']['text']
        if '/health_updates' in msg_text:
            print("\nhealth updates present")
            chat_id = current_msg['message']['chat']['id']
            get_health_update(chat_id)

        elif '/curr_occupancy' in msg_text:
            print("\curr occup present")
            chat_id = current_msg['message']['chat']['id']
            get_curr_occupancy(chat_id)

        elif '/reset_occupancy' in msg_text:
            print("reset occup present")
            chat_id = current_msg['message']['chat']['id']
            reset_occupancy(chat_id)

        else:
            print("\nnot present")
    else:
        print("msg id is the same")
    prev_msg_id = current_msg_id
    
    return


def get_health_update(chat_id):
    ''' for pi and uss, readings must be less than 3 min from now
        else: we will add error msg: _____ sensor hasn't gotten a reading in the last 60 min'''

    errors = []
    timestamps = []

    # get reading for out USS
    cur.execute('select "timestamp" from sensor_health where "sensor_id" = \'pi123\' order by id desc limit 1;')
    last_pi_rec = cur.fetchone()[0]
    # print("current time:", datetime.now())
    # print("pi timestamp:", last_pi_rec)
    rpi_time_diff = (datetime.now() - last_pi_rec).total_seconds() / 60         # time difference in minutes
    # print ("rpi time diff:", rpi_time_diff, '\n')

    if (rpi_time_diff > 60):
        errors.append("Raspberry pi")
    timestamps.append(("Raspberry pi",last_pi_rec))
    
    # get reading for in USS
    cur.execute('select "timestamp" from sensor_health where "sensor_id" = \'fb48fc3a6ee3\' order by id desc limit 1;')
    last_inUSS_rec = cur.fetchone()[0]

    # print("current time:", datetime.now())
    # print("in uss timestamp:", last_inUSS_rec)
    inUSS_time_diff = (datetime.now() - last_inUSS_rec).total_seconds() / 60         # time difference in minutes
    # print ("in uss time diff:", inUSS_time_diff, '\n')

    if (inUSS_time_diff > 60):
        errors.append("Inside USS")
    timestamps.append(("Inside USS", last_inUSS_rec))

    # get reading for pir USS
    cur.execute('select "timestamp" from sensor_health where "sensor_id" = \'e6f5f2bb5b0e\' order by id desc limit 1;')
    last_outUSS_rec = cur.fetchone()[0]

    # print("current time:", datetime.now())
    # print("out uss timestamp:", last_outUSS_rec)
    outUSS_time_diff = (datetime.now() - last_outUSS_rec).total_seconds() / 60         # time difference in minutes
    # print ("out uss time diff:", outUSS_time_diff, '\n')

    if (outUSS_time_diff > 60):
        errors.append("Outisde USS")
    timestamps.append(("Outside USS",last_outUSS_rec))

    print("errors:",errors)
    print("timestamps:",timestamps)


    send_msg =''

    if len(errors) > 0:
        for error in errors:
            s = error + ", "
            send_msg += s
        send_msg.strip(", ")

        send_msg += "did not receive health updates in the last 60min.\n\nLast hearbeats:\n"

    else:
        send_msg = "All sensors and pi are working fine! :)\n\nLast heartbeats:\n"

    for t in timestamps:
        utc = datetime.strptime(str(t[1]), '%Y-%m-%d %H:%M:%S')
        local_time= utc.astimezone(timezone('Asia/Singapore'))

        s = t[0] + " - " + str(local_time) + "\n"
        send_msg += s

    send_msg.strip("\n")
    print("\n final msg is:", send_msg)

    params = {'chat_id':chat_id, 'text':send_msg}
    r = requests.get(url=url_sendMsg, params = params)  


    '''
    if all working:
    All sensors are working fine! :)

    else:
    [ ], [ ], did not receive health updates in the last 60min.

    Last heartbeats:
    Raspberry Pi - [timestamp]
    In USS - [timestamp]
    Out USS - [timestamp]
    '''
    
    ''' for pir, a bit more difficult.... perhaps don't do first'''

    return

def get_curr_occupancy(chat_id):
    cur.execute('select "value", "timestamp" from occupancy order by id desc limit 1;')
    result = cur.fetchone()
    # (5, datetime.datetime(2020, 3, 20, 10, 22, 51))
    # print(result)

    value = result[0]
    # timestamp = result[1]
    utc = datetime.strptime(str(result[1]), '%Y-%m-%d %H:%M:%S')
    local_time= utc.astimezone(timezone('Asia/Singapore'))

    # s = t[0] + " - " + str(local_time) + "\n"
    send_msg = "Current occupancy is " + str(value) + " last recorded at " + str(local_time) + "."

    params = {'chat_id':chat_id, 'text':send_msg}
    r = requests.get(url=url_sendMsg, params = params)   

    return

def reset_occupancy(chat_id):
    timestamp = datetime.now()
    meeting_room_id = 'G'
    remarks = 'Reset'
    cur.execute('INSERT INTO occupancy VALUES (DEFAULT, %s, %s, %s, %s);',(str(timestamp), str(meeting_room_id), 0, str(remarks)))
    # cur.execute('INSERT INTO sensor_health ("id", "timestamp", "sensor_id", "value") VALUES (DEFAULT, %s, %s, %s);',(str(timestamp), str(MAC_address), float(value)))
    # timestamp, meeting_room_id, value, remarks=None

    send_msg = "Reset done!"
    params = {'chat_id':chat_id, 'text':send_msg}
    r = requests.get(url=url_sendMsg, params = params)

    get_curr_occupancy(chat_id)

    return



while True:
    check_text()
    time.sleep(5)
