from django.http import response

from user_backend import *
from threading import Thread
from server_api import *


def user_backend_server():
    """
    a server that handles the user's requests:
    1. getting a file from the user and u[loading it
    2. getting a string for search
    and returning all the names of files and links to the client
    """
    server.test(HandlerClass=HTTPRequestHandler)


def main():
    init()

    Thread(target=update_meta_data_every_1_hour).start()
    Thread(target=user_backend_server).start()


if __name__ == '__main__':
    main()
