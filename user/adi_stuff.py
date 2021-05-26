from __future__ import print_function

import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']


def add_doc(file_path, folder_id):
    """
    adds the doc to the drive and all the tags we need
    :param folder_id: id of the folder in Google Drive
    :param file_path: file path of the doc in the client's computer
    :return: file id
    """
    service = add_drive_data()
    file_metadata = {'parents': [folder_id], 'name': file_path}
    media = MediaFileUpload('files/photo.jpg', mimetype='image/jpeg')
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    file_id = file.get('id')

    return file_id


def add_drive_data():
    """
    creates a connection to the data base (drive) based on the drive token
    :return: service
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('data_files/drive_token.pickle'):
        with open('data_files/drive_token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'data_files/drive-credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('data_files/drive_token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

