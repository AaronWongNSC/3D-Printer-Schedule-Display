from datetime import datetime
import os.path

import get_time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_credentials():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return creds

def get_events(local_start_dt, local_stop_dt):
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    start_time = get_time.g_time(local_start_dt)
    stop_time = get_time.g_time(local_stop_dt)
    
    try:
        # Call the Calendar API
        events_result = (
            service.events()
            .list(
                calendarId="48a69f78a92ac5650ee3ce054b572f1002bbd84d450f5750c080a5480618c2a8@group.calendar.google.com",
                timeMin=start_time,
                timeMax=stop_time,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        vyper = events_result.get("items", [])
        
        events_result = (
            service.events()
            .list(
                calendarId="cfbcfbd49fa596653a2d368cfdc6331a9a288082bf7d5a403cf05a399ffc4a3a@group.calendar.google.com",
                timeMin=start_time,
                timeMax=stop_time,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        ender = events_result.get("items", [])
        
        # Add printer information
        for event in vyper:
            event['printer'] = 'vyper'
        for event in ender:
            event['printer'] = 'ender'
        
        # Create prints list
        prints = [ convert_event(event) for event in vyper + ender]
        
        return prints

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def convert_event(event):
    starttime = get_time.convert_local_dt(
        datetime.strptime(event['start']['dateTime'][:19], get_time.GOOGLE_TIME_FORMAT))
    endtime = get_time.convert_local_dt(
        datetime.strptime(event['end']['dateTime'][:19], get_time.GOOGLE_TIME_FORMAT))
    
    if 'summary' not in event:
        event['summary'] = 'BLANK'
    return {
        'printer': event['printer'],
        'title': event['summary'],
        'start': starttime,
        'end': endtime,
        }