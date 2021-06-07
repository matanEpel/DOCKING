# TODO: def get_list_of_docs(search_string)
#  gets a list of docs names and keys out of the drive by a given search input

# TODO: def get_doc(doc_key)
#  gets the dock by its key

from __future__ import print_function

import io
import json
import pickle
import os.path
import time

import global_vars

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import time

SCOPES = ['https://www.googleapis.com/auth/drive']


def init():
    data = dict()
    with open("data_files/info.txt", "r") as info:
        for line in info.read().split("\n"):
            if len(line) != 0:
                if line.split(": ")[1][0] == '\\':
                    data[line.split(": ")[0]] = line.split(": ")[1][1:]
                else:
                    data[line.split(": ")[0]] = line.split(": ")[1]
    global_vars.TALPIOT_DRIVE_ID = data["TALPIOT_DRIVE_ID"]


def add_doc(file_path, folder_id):
    """
    adds the doc to the drive and all the tags we need
    :param folder_id: id of the folder in Google Drive
    :param file_path: file path of the doc in the client's computer
    :return: file id
    """
    service = add_drive_data()
    file_metadata = {'parents': [folder_id], 'name': file_path}
    media = MediaFileUpload(file_path)
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


def search_by_word(word: str, folders):
    """gets a word and list of names and ids and return ids of matching names"""
    ids = {}
    for name in folders.keys():
        if word in name or name in word:
            ids[name] = folders[name]
    return ids


def week_date(date):
    with open("data_files/date_week_sem.txt", "r") as f:
        for line in f.read().split("\n"):
            new_line = line.split(":")
            date1, date2 = time.strptime(new_line[0].split(",")[0], "%Y-%m-%d"), time.strptime(
                new_line[0].split(",")[1], "%Y-%m-%d")
            week, sem = int(new_line[1].split(",")[0]), int(new_line[1].split(",")[1])
            if date1 <= time.strptime(date, "%Y-%m-%d") <= date2:
                return week, sem
    return 0, 0


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
            week, sem = week_date(file["createdDate"].split("T")[0])
            type_doc = file["title"].split(".")
            if len(type_doc) == 1:
                type_doc = "folder"
            else:
                type_doc = type_doc[-1]
            names_id_dict[file["title"]] = {"name": file["title"], "link": file["alternateLink"],
                                            "date": file["createdDate"], "type": type_doc,
                                            "week": week, "sem": sem}
            count += 1
            if count % 7 == 0:
                print("\n" * 10 + "loading" + "." * (1 + count % 6))

        page_token = children.get('nextPageToken')
        if not page_token:
            break

    return names_id_dict


def search(input_search, files_dict):
    return search_by_word(input_search, files_dict)


def update_meta_data_every_1_hour():
    while True:
        time.sleep(60*10)  # sleep for 110 minutes
        folders_dict = get_all_names()
        with open("metadata.json", "w") as metadata:
            json.dump(folders_dict, metadata)
        print("heyyy")  # TODO: change when done


def get_data_from_file():
    with open("metadata.json", "r") as metadata:
        return json.load(metadata)
