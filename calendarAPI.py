from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime, pytz

# import json
# import requests
# from flask import jsonify

# calendarID = 'allyson.lim.2017@smu.edu.sg'
# base_url = 'https://www.googleapis.com/calendar/v3/'

# google_auth = 'https://www.googleapis.com/auth/calendar'
# credentials = jsonify({"client_id":"484791267877-fjk5bjh6m28fq432o997i9a0ti3kho7l.apps.googleusercontent.com","project_id":"cs462-1582599877119","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"mGdK_6Iy0Fq-CbLe4463tIlY","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]})

# getCalendar_url = base_url + 'calendars/{}'.format(calendarID)

# def get_calendar():
    
#     r = requests.get(url=getCalendar_url)
#     print(r.json())
#     return

# get_calendar()


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def creds():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

    # Call the Calendar API
    #datetime changed to SG time
def getCalendarEvents(service):
    eidDict = {}
    now = datetime.datetime.now(pytz.timezone('Asia/Singapore')).isoformat()
    #print(now)
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        creator = event['creator'].get('email')
        type_of_event = event['kind']
        eid = event['id']
        
        if 'location' in event:
            location = event['location']
        else:
            location = None
        
        details = {'creator':creator, 'location':location, 'start':start, 'end':end}
        eidDict[eid] = details
        #print(start, event)
        print(start,end,creator, type_of_event,eid, location)
    
    # print(events)

    num_of_events = len(events)
    print("Number of events: ", num_of_events)

    # print(eidDict)

    return eidDict

def deleteCalendarEvents(service, eid):
    now = datetime.datetime.now(pytz.timezone('Asia/Singapore')).isoformat()

    # events = events_result.get('items', [])

    if len(eid) == 0:
        print('No upcoming events found.')
    else:
        print('Deleting 1 Event')
        events_result = service.events().delete(calendarId='primary', eventId=list(eid.keys())[0], sendNotifications=True).execute()
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     end = event['end'].get('dateTime', event['end'].get('date'))
    #     creator = event['creator'].get('email')
    #     type_of_event = event['kind']

        # print(start,end,creator, type_of_event)
    return

def getEventColor(service, eventId):
    '''
    get the current color of the event on google calendar
    default event doesn't have a colorId but is inside the list of colorId [7]
    returns dictionary where key: event id, value: color ID
    '''
    now = datetime.datetime.now(pytz.timezone('Asia/Singapore')).isoformat()
    #get most current or upcoming event 
    event_result = service.events().list(calendarId='primary', timeMin=now,
                                      maxResults=1, singleEvents=True,
                                      orderBy='startTime').execute()

    latest_event = event_result.get('items', [])
    # print(latest_event)
    # start = latest_event[0]['start']['dateTime']
    # end = latest_event[0]['end']['dateTime']
    event_id = latest_event[0]['id']
    dict_id_color = {}

    if ('colorId' not in latest_event[0])==True:
        dict_id_color[event_id]=7
    else:
        dict_id_color[event_id] = latest_event[0]['colorId']
    # print(dict_id_color)
    return dict_id_color

#not totally completed yet
def updateEventColor(service, eventId, meetingrm):
    '''
    changes the color of the event based on several factors:
        red -> booked, occupied
        green-> booked, unoccupied
        no events created for unbooked & occupied and unbooked & unoccupied
    '''
    #available colors on google calendars
    colors = service.colors().get().execute()
    events_color = colors["event"]
    events_color_dict = {}

    default_color = 7
    book_occupied = 11 #red
    book_unoccupied = 2 #green

    for number in events_color:
        color_type = events_color[number]['background']
        events_color_dict[number]= color_type
    #print(events_color_dict)
    
    # for k,v in events_color_dict.items():
    #     if meetingrm > 1:





def main():
    # getCalendarEvents(creds())
    # deleteCalendarEvents(creds(),getCalendarEvents(creds()))
    # getEventColor(creds(), getCalendarEvents(creds()))


if __name__ == '__main__':
    main()