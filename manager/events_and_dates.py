from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import global_vars

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar']


def get_all_non_activities():
    not_act = []
    with open(global_vars.NOT_ACTIVITIES, 'r') as not_activities:
        not_act = not_activities.read()
    not_act = [word for word in not_act.split("\n") if len(word) > 0]
    return not_act


def not_contains(name, not_act):
    for word in not_act:
        if word in name:
            return False
    return True


def get_todays_events(year, month, day):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('data_files/token.pickle'):
        with open('data_files/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'data_files/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('data_files/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    date = year+"-"+month+"-"+day
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=global_vars.ORIGINAL_CALENDER, timeMin=date + 'T00:00:00',
                                          timeMax=date+'23:59:59', singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    events_data = []
    if not events:
        print('No upcoming events found.')
    not_act = get_all_non_activities()
    for event in events:
        name = event['summary']
        start = event['start'].get('dateTime', event['start'].get('time'))
        end = event['end'].get('dateTime', event['end'].get('time'))
        if start is not None and end is not None and name is not None and not_contains(name, not_act) :
            events_data.append({"name": name, "start": start, "end": end})
    return events_data


def get_n_events(n):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('data_files/token.pickle'):
        with open('data_files/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'data_files/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('data_files/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=global_vars.ORIGINAL_CALENDER, timeMin=now,
                                          maxResults=n, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    events_data = []
    if not events:
        print('No upcoming events found.')
    not_act = get_all_non_activities()
    for event in events:
        name = event['summary']
        start = event['start'].get('dateTime', event['start'].get('time'))
        end = event['end'].get('dateTime', event['end'].get('time'))
        if start is not None and end is not None and name is not None and not_contains(name, not_act) :
            events_data.append({"name": name, "start": start, "end": end})
    return events_data


if __name__ == '__main__':
    print(get_n_events(4))
