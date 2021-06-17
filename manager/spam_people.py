from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import create_event
import events_and_dates
import global_vars
from datetime import date

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar']


def spam_1_people(mail, date, name):
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
                'data_files/credentials.json', events_and_dates.SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('data_files/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    email = ["matan.epel12@gmail.com"]  # service_rotation.get_n_emails(1)
    event = {
        'summary': "שכחת לסכם את: " + name,
        'description': "היי, אז שכחת לסכם את האירוע: " + name + "\n" + "מזכיר שצריך למלא את קובץ התיאור/סיכום, תלוי מה רלוונטי, ולהעלות את המצגת אם הייתה. יכול להיות ששכחת פשוט לשנות את השם של הקבצים, אז פשוט תשנה את השם ואני אפסיק לחפור לך.",
        'start': {
            'date': date,
            'timeZone': 'Israel',
        },
        'end': {
            'date': date,
            'timeZone': 'Israel',
        },
        'attendees': [
            {'email': [mail]},
        ]
    }

    event = service.events().insert(calendarId=global_vars.SHIFTS_CALENDER, body=event,
                                    sendNotifications=True).execute()


def not_edited(dir_id):
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # The file token.pickle stores the
    # user's access and refresh tokens. It is
    # created automatically when the authorization
    # flow completes for the first time.

    # Check if file token.pickle exists
    if os.path.exists('data_files/drive_token.pickle'):
        # Read the token from the file and
        # store it in the variable creds
        with open('data_files/drive_token.pickle', 'rb') as token:
            creds = pickle.load(token)

            # If no valid credentials are available,
    # request the user to log in.
    if not creds or not creds.valid:

        # If token is expired, it will be refreshed,
        # else, we will request a new one.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'data_files/drive-credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle
        # file for future usage
        with open('data_files/drive_token.pickle', 'wb') as token:
            pickle.dump(creds, token)

            # Connect to the API service
    service = build('drive', 'v2', credentials=creds)

    page_token = None
    while True:
        param = {}
        if page_token:
            param['pageToken'] = page_token
        children = service.children().list(
            folderId=dir_id, **param).execute()

        for child in children.get('items', []):
            file = service.files().get(fileId=child["id"]).execute()
            if file['title'] != "תיאור הפעילות" and file['title'] != "סיכום הפעילות":
                return False

        page_token = children.get('nextPageToken')
        if not page_token:
            break
    return True


def spam_everyone():
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    all_people = []
    with open('data_files/hasnt_done_yet.txt', 'r') as data:
        d = data.read()
        for line in d.split("\n"):
            if len(line) > 0:
                all_people.append({"id": line.split(":")[0], "email": line.split(":")[1], "date": line.split(":")[2], "name": line.split(":")[3]})
    with open('data_files/hasnt_done_yet.txt', 'w') as data:
        pass
    for p in all_people:
        if not_edited(p["id"]):
            print(p["email"])
            spam_1_people(p["email"], d1, p["name"])
            create_event.save_to_not_done_file(p["id"], p["email"], p["date"], p["name"])


