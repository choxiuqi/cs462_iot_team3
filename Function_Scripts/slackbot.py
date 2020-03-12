import json
import requests

chat_id = 148720480 # fill in your chat id here
oauth_token = 'xoxp-995394136980-983062033826-985371856035-911c96855d6a6795c0ff1059c6f85a0f' # OAuth Access Token
bot_token = 'xoxb-995394136980-986657601185-mICVRNdVOmb4l4vhvkcrabmF' # Bot User OAuth Access Token
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

def getUsers(token, cursor):
    params = {'token':token, 'limit':2, 'cursor':cursor}
    r = requests.get(getUsers_url, params=params)
    print(r.json())
    return r.json()['response_metadata']['next_cursor']

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
    cursor = 0
    while cursor is not '':
        getUsers(bot_token, cursor)
        new_cursor = getUsers(bot_token, cursor) 
        cursor = new_cursor
        new_cursor = ''

	
main()