from __future__ import print_function
import datetime
import pickle
import os.path
import sys
from oauth2client import client
from googleapiclient import sample_tools
import pytz
import time
import psycopg2

conn = psycopg2.connect(host="127.0.0.1", dbname="cs462team3db", user="team3user", password="password")
cur = conn.cursor()
conn.autocommit = True

def main(argv):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar')

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
    service = main(sys.argv)
    results = getCalendarEvents(service)
    length = len(results)
    counter = 0
    while counter<length:
        creator = results[counter]['creator']
        start = results[counter]['start']
        end = results[counter]['end']
        cur.execute("INSERT INTO upcoming VALUES(DEFAULT, %s, %s, %s);", (creator,start,end))
        counter += 1
    time.sleep(900)
    cur.execute("DELETE FROM upcoming;")