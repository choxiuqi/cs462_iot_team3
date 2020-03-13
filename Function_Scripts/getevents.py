from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pytz
import time
import psycopg2

conn = psycopg2.connect(host="127.0.0.1", dbname="cs462team3db", user="team3user", password="password")
cur = conn.cursor()
conn.autocommit = True

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authService():
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
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def getCalendarEvents(service):
    # Call the Calendar API
    now_utc = pytz.utc.localize(datetime.datetime.utcnow())
    now_sg = now_utc.astimezone(pytz.timezone('Asia/Singapore'))
    now = now_sg.isoformat()
    print('Getting the upcoming 2 events')
    events_result = service.events().list(calendarId='ntucenterprise.sg_32313338393839313338@resource.calendar.google.com', timeMin=now,
                                        maxResults=2, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    eidDict = {}
    counter = 0

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        creator = event['creator'].get('email')
        eid = event['id']
        details = {'eid':eid, 'creator':creator, 'start':start, 'end':end}
        eidDict[counter] = details
        counter += 1
        
    no_of_events = len(events)
    print("Number of events: ", no_of_events)
    #print(eidDict)

    return eidDict

while True:
    results = getCalendarEvents(authService())
    length = len(results)
    counter = 0
    while counter<length:
        creator = results[counter]['creator']
        start = results[counter]['start']
        end = results[counter]['end']
        cur.execute("INSERT INTO upcoming VALUES (%s, %s, %s);",(creator, start, end))
    time.sleep(900)
    cur.execute("DELETE FROM upcoming;")
