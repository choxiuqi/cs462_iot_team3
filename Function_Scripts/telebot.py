import json
import requests

chat_id = 148720480 # fill in your chat id here
api_token = '1080322521:AAEniAOZwvcueU0AKsLxEAPju3gAT9S-DvI' # fill in your api token here
base_url = 'https://api.telegram.org/bot{}/'.format(api_token)

getUpdates_url = base_url + 'getUpdates'
sendMsg_url = base_url + 'sendMessage'

# ##################################################################################################################################

# telebot's use is to inform us when there are any errors or alerts that we should take not of
# e.g. when sensor didn't give us health reading, or when rpi no heartbeat, or (when too many errors?)

# ------get chatId------
def getChatID():
    params = {'offset':0}
    r = requests.get(getUpdates_url, params=params)
    chatID = r.json()['result'][-1]['message']['chat']['id']
    # print(chatID)
    return chatID

def alert(chatID, msg):
    params = {'chat_id':chatID, 'text':msg}
    r = requests.post(sendMsg_url, params=params)

# ------main function------

def check_sensor_health():
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
            s = error[0] + " - last heartbeat received at: " + error[1] + "\n"
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