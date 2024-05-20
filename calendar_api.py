import datetime
import os.path

from time_format import time_format

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

def get_events():
    def display_event(event):
        def convert_time(time):
            dt = datetime.datetime.strptime(time[:19], "%Y-%m-%dT%H:%M:%S")
            return dt.strftime(time_format)
        
        start = convert_time(event["start"]["dateTime"])
        end = convert_time(event["end"]["dateTime"])
        print('{:25}{:25}  {}'.format(start, end, event["summary"]))
    
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId="48a69f78a92ac5650ee3ce054b572f1002bbd84d450f5750c080a5480618c2a8@group.calendar.google.com",
            timeMin=now,
            maxResults=5,
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
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    ender = events_result.get("items", [])
    
    print('Next 5 prints on the Vyper:')
    print('{:25}{:25}  {}'.format('START', 'STOP', 'DESCRIPTION'))
    for event in vyper:
        display_event(event)
    
    print('\nNext 5 prints on the Ender:')
    print('{:25}{:25}  {}'.format('START', 'STOP', 'DESCRIPTION'))
    for event in ender:
        display_event(event)
