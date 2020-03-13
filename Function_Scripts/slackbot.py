import json
import requests

chat_id = 148720480 # fill in your chat id here
oauth_token = 'xoxp-995394136980-983062033826-997694066677-b0e3c80a3779dfa9bacf56e683058364' # OAuth Access Token
bot_token = 'xoxb-995394136980-986657601185-GSgFfbhosFXevUrCyUllw5W0' # Bot User OAuth Access Token
baseURL = 'https://slack.com/api/'

sendMessage_url = baseURL + 'chat.postMessage'
getIdentity_url = baseURL + 'users.identity'
getConv_url = baseURL + 'users.conversations'
getUsers_url = baseURL + 'users.list'

# ##################################################################################################################################

# ------get user identity (https://api.slack.com/methods/users.identity)------
def getIdentity(token):
    params = {'token':token}
    r = requests.get(getIdentity_url, params=params)
    print(r.json())
    return 

# ------get conversations identity (https://api.slack.com/methods/users.conversations)------
def getConversation(token):
    params = {'token':token, 'limit':100}
    r = requests.get(getConv_url, params=params)
    print(r.json())
    return 

# ------get users (https://api.slack.com/methods/users.list)------
def getUsers(token, cursor):
    params = {'token':token, 'limit':2, 'cursor':cursor}
    r = requests.get(getUsers_url, params=params)
    # print(r.json())
    # for i in r.json()['members']:
    #     if i['id'] is not 'USLACKBOT':
    #         user = {'id': i['id'], 'name': i['name'], 'unixtime': i['updated']}
    i = r.json()['members'][-1]
    user = {'id': i['id'], 'name': i['name'], 'unixtime': i['updated']}
    cursor = r.json()['response_metadata']['next_cursor']
    print(user)
    return user, cursor

# ------post message (https://api.slack.com/methods/chat.postMessage)------
def postMessage(token,channel,msg):
    params = {'token':token, 'channel':channel, 'text':msg}
    r = requests.post(sendMessage_url, params=params)
    return 

# ------main function------

def main():
    # while True:
    # postMessage(bot_token, 'random', 'hello')
    # getIdentity(oauth_token)
    # getConversation(bot_token)
    new_cursor = 0
    cursor = 0
    while new_cursor is not '':
        getUsers(bot_token, cursor)
        cursor = new_cursor
        new_cursor = getUsers(bot_token, cursor) 

	
main()