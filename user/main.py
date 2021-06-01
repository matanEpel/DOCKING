from user_backend import *

folders_dict = get_data_from_file()
print(search("description", folders_dict))


def user_backend_server():
    """
    a server that handles the user's requests:
    1. getting a file from the user and u[loading it
    2. getting a string for search
    and returning all the names of files and links to the client
    """

    # in case of uploading file:
    # TODO: name, path = get_file_from_user()
    # TODO: add_doc(path, global_vars.TALPIOT_DRIVE_ID)
    # TODO: deleting the file in path

    # in case of asing for metadata file:
    # TODO: send metadata.json to client

    # in case of searching file:
    # TODO: string = get_search_string_from_user()
    files_dict = get_data_from_file()
    # TODO: send back the result of search(string, files_dict)


def main():
    init()
    # TODO: run in another process every one hour:
    update_meta_data_every_1_hour()

    # TODO: run in another process:
    user_backend_server()

if __name__ == '__main__':
    main()
