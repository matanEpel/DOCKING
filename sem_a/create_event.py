from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import events_and_dates
import service_rotation
import drive
import global_vars


def save_to_not_done_file(id, email, date, name):
    with open('data_files/hasnt_done_yet.txt', 'a') as not_done_file:
        not_done_file.write(id+":"+email+":"+date[:10]+":"+name+"\n")


def get_description():
    description = ""
    with open(global_vars.DES_FILE, 'r') as desc:
        description = desc.read()
    return description


def create_n_events(n):
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


    amount = n
    event_dict = events_and_dates.get_n_events(amount * 4)[:amount]

    for i in range(min(n, len(event_dict))):
        email = service_rotation.get_n_emails(1)
        link, id = drive.create_folder(event_dict[i]["name"], event_dict[i]["start"][:10])
        save_to_not_done_file(id, email[0], event_dict[i]["start"], event_dict[i]["name"])
        event = {
            'summary': "סיכום: " + event_dict[i]["name"],
            'description': "תעלו את המצגת שהועברה בפעילות (אם הועברה מצגת) ללינק המצורף, ותערכו את קובץ התיאור/סיכום (נמצא בקישור) לפי מה שצריך (סיכום אם אפשר לסכם תוך כדי ותיאור אם הפעילות אינטראקטיבית ואפשר לכתוב במחשב רק בסוף): " + link,
            'start': {
                'dateTime': event_dict[i]["start"],
                'timeZone': 'Israel',
            },
            'end': {
                'dateTime': event_dict[i]["end"],
                'timeZone': 'Israel',
            },
            'attendees': [
                {'email': email},
            ]
        }

        event = service.events().insert(calendarId=global_vars.SHIFTS_CALENDER, body=event, sendNotifications=True).execute()
        print("\n"*80)
        print("|||" * (i+1) + " " + str(100*((i+1)/n)) + "%", end="")


if __name__ == '__main__':
    create_n_events(1)
