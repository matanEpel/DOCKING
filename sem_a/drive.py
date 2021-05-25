from __future__ import print_function

import io
import pickle
import os.path
import time

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import global_vars

# If modifying these scopes, delete the file token.pickle.
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']


def set_permission(service, file_id):
    permission = {'type': 'anyone',
                  'value': 'anyone',
                  'role': 'writer'}
    return service.permissions().create(fileId=file_id, body=permission).execute()


def create_folder(name, date):
    full_name = name + ": " + date

    """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
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

    folder_metadata = {
        'name': full_name,
        'parents': [global_vars.TALPIOT_DRIVE_ID],
        'mimeType': 'application/vnd.google-apps.folder'
    }

    folder = service.files().create(body=folder_metadata, fields='webViewLink, id').execute()
    folder_id = folder.get('id')
    service.permissions().create(body={"role": "writer", "type": "anyone"}, fileId=folder_id).execute()
    folder_link = folder.get('webViewLink')

    # file_metadata = {'parents': [folder_id], 'name': 'תיאור הפעילות'}
    # media = MediaFileUpload(global_vars.DESCRIPTION_FILE)
    # file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    file2_metadata = {'parents': [folder_id], 'name': 'סיכום הפעילות'}
    media2 = MediaFileUpload(global_vars.DOCUMENTATION_FILE)
    file2 = service.files().create(body=file2_metadata, media_body=media2, fields='id').execute()
    return folder_link, folder_id


def search_by_word(word: str, folders):
    """gets a word and list of names and ids and return ids of matching names"""
    ids = {}
    for name in folders.keys():
        if word in name or name in word:
            ids[name] = folders[name]
    return ids


def get_all_names():
    """getting the names and ids of every folder in the drive"""

    names_id_dict = {}
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
    count = 0
    while True:
        param = {}
        if page_token:
            param['pageToken'] = page_token
        children = service.children().list(
            folderId=global_vars.TALPIOT_DRIVE_ID, **param).execute()

        for child in children.get('items', []):
            file = service.files().get(fileId=child["id"]).execute()
            names_id_dict[file["title"]] = child["id"]
            count += 1
            if count % 7 == 0:
                print("\n" * 10 + "loading" + "." * (1 + count % 6))

        page_token = children.get('nextPageToken')
        if not page_token:
            break

    return names_id_dict


def get_all_files(folder_id):
    """downloading all the files of given folder to the current directory"""

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
            folderId=folder_id, **param).execute()

        for child in children.get('items', []):
            id_of_file = child["id"]
            request = service.files().get_media(fileId=id_of_file)
            file = service.files().get(fileId=child["id"]).execute()
            fh = io.FileIO(file['title'], 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))

        page_token = children.get('nextPageToken')
        if not page_token:
            break

    print("all the files in this folder are in the current working directory")
    time.sleep(3)
    print("\n" * 10)


def search():
    folders_dict = get_all_names()

    done = False

    print("\n" * 10)
    while not done:
        word = input("press x to exit or the word you want to search for searching: ")
        print("\n" * 10)
        if word == 'x':
            done = True
            continue

        names_and_ids = search_by_word(word, folders_dict)
        keys = [key for key in names_and_ids.keys()]

        if len(keys) > 0:
            inp = input("\n".join([str(i + 1) + ". " + keys[i]
                        for i in range(len(keys))]) +
                        "\nenter the number of the folder you want (x for no one):")
            if inp == 'x':
                print("\n" * 10)
                continue
            specific_folder = int(inp)
        else:
            print("no matching names!")
            time.sleep(2)
            print("\n" * 10)
            continue
        print("\n" * 10)

        folder_id = names_and_ids[keys[specific_folder - 1]]

        get_all_files(folder_id)
