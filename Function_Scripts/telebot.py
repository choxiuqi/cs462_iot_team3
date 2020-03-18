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
    healthy = []

    # get reading for out USS
    cur.execute('select "timestamp" from sensor_health where "sensor_id" = \'pi123\' order by id desc limit 1;')
    last_pi_rec = cur.fetchone()[0]
    # print("current time:", datetime.now())
    # print("pi timestamp:", last_pi_rec)
    rpi_time_diff = (datetime.now() - last_pi_rec).total_seconds() / 60         # time difference in minutes
    # print ("rpi time diff:", rpi_time_diff, '\n')

    if (rpi_time_diff < 60):
        errors.append(("Raspberry pi", last_pi_rec))
    else:
        healthy.append("Raspberry pi")
    
    # get reading for in USS
    cur.execute('select "timestamp" from sensor_health where "sensor_id" = \'fb48fc3a6ee3\' order by id desc limit 1;')
    last_inUSS_rec = cur.fetchone()[0]

    # print("current time:", datetime.now())
    # print("in uss timestamp:", last_inUSS_rec)
    inUSS_time_diff = (datetime.now() - last_inUSS_rec).total_seconds() / 60         # time difference in minutes
    # print ("in uss time diff:", inUSS_time_diff, '\n')

    if (inUSS_time_diff < 60):
        errors.append(("Inside USS", last_inUSS_rec))
    else:
        healthy.append("Inside USS")

    # get reading for pir USS
    cur.execute('select "timestamp" from sensor_health where "sensor_id" = \'e6f5f2bb5b0e\' order by id desc limit 1;')
    last_outUSS_rec = cur.fetchone()[0]

    # print("current time:", datetime.now())
    # print("out uss timestamp:", last_outUSS_rec)
    outUSS_time_diff = (datetime.now() - last_outUSS_rec).total_seconds() / 60         # time difference in minutes
    # print ("out uss time diff:", outUSS_time_diff, '\n')

    if (outUSS_time_diff > 60):
        errors.append(("Outisde USS",last_outUSS_rec))
    else:
        healthy.append("Outisde USS")

    print("errors:",errors)
    print("health:",healthy)


    send_msg = "Working: \n"

    if len(healthy) > 0:
        for health in healthy:
            send_msg += health + ", "
        send_msg.strip(", ")
        send_msg += "\n\nNot working: \n"
        # error_msg += "did not receive a reading in the last 60 min"  
    else:
        send_msg += "None\n\nNot working: \n"

    if len(errors) > 0:
        for error in errors:
            utc = datetime.strptime(str(error[1]), '%Y-%m-%d %H:%M:%S')
            local_time= utc.astimezone(timezone('Asia/Singapore'))
            s = error[0] + " - last heartbeat received at: " + str(error[1]) + "\n"
            send_msg += s
        send_msg.strip("\n")
        # error_msg += "did not receive a reading in the last 60 min"  
    else:
        send_msg += "None"


    print("\n final msg is:", send_msg)

    params = {'chat_id':chat_id, 'text':send_msg}
    r = requests.get(url=url_sendMsg, params = params)  


    '''
    Working:
    rpi, 
    
    Not working:
    outside uss - last heartbeat received at:
    inside uss - last heartbeat received at:
    '''
    
    ''' for pir, a bit more difficult.... perhaps don't do first'''

    return