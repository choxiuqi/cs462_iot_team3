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

def main():
    # while True:
    getChatID()
	
main()
