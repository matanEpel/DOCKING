import global_vars

def init():
    data = dict()
    with open("data_files/info.txt", "r") as info:
        for line in info.read().split("\n"):
            if len(line) != 0:
                if line.split(": ")[1][0] == '\\':
                    data[line.split(": ")[0]] = line.split(": ")[1][1:]
                else:
                    data[line.split(": ")[0]] = line.split(": ")[1]
    global_vars.SHIFTS_CALENDER = data["SHIFTS_CALENDER"]
    global_vars.DES_FILE = data["description"]
    global_vars.TALPIOT_DRIVE_ID = data["TALPIOT_DRIVE_ID"]
    global_vars.ORIGINAL_CALENDER = data["ORIGINAL_CALENDER"]
    global_vars.NOT_ACTIVITIES = data["not_activities"]
    global_vars.EMAIL_FILE_NAME = data["emails"]
    global_vars.DESCRIPTION_FILE = data["description_file"]
    global_vars.DOCUMENTATION_FILE = data["documentation_file"]
    global_vars.MAIL_MSG_FILE = data["EMAIL_DATA"]

def change_calender_id(new_id):
    init()
    new_data = "emails: " + global_vars.EMAIL_FILE_NAME + "\n"
    new_data += "not_activities: " + global_vars.NOT_ACTIVITIES + "\n"
    new_data += "description: " + global_vars.DESCRIPTION_FILE + "\n"
    new_data += "documentation_file: " + global_vars.DOCUMENTATION_FILE + "\n"
    new_data += "description_file: " + global_vars.DESCRIPTION_FILE + "\n"
    new_data += "SHIFTS_CALENDER: " + global_vars.SHIFTS_CALENDER + "\n"
    new_data += "TALPIOT_DRIVE_ID: " + global_vars.TALPIOT_DRIVE_ID + "\n"
    new_data += "ORIGINAL_CALENDER: " + new_id + "\n"
    new_data += "EMAIL_DATA: " + global_vars.EMAIL_FILE_NAME + "\n"
    with open("data_files/info.txt", "w") as info:
        info.write(new_data)


def change_shifts_calender_id(new_id):
    init()
    new_data = "emails: " + global_vars.EMAIL_FILE_NAME + "\n"
    new_data += "not_activities: " + global_vars.NOT_ACTIVITIES + "\n"
    new_data += "description: " + global_vars.DESCRIPTION_FILE + "\n"
    new_data += "documentation_file: " + global_vars.DOCUMENTATION_FILE + "\n"
    new_data += "description_file: " + global_vars.DESCRIPTION_FILE + "\n"
    new_data += "SHIFTS_CALENDER: " + new_id + "\n"
    new_data += "TALPIOT_DRIVE_ID: " + global_vars.TALPIOT_DRIVE_ID + "\n"
    new_data += "ORIGINAL_CALENDER: " + global_vars.ORIGINAL_CALENDER + "\n"
    new_data += "EMAIL_DATA: " + global_vars.EMAIL_FILE_NAME + "\n"
    with open("data_files/info.txt", "w") as info:
        info.write(new_data)


def change_drive_id(new_drive):
    init()
    new_data = "emails: " + global_vars.EMAIL_FILE_NAME + "\n"
    new_data += "not_activities: " + global_vars.NOT_ACTIVITIES + "\n"
    new_data += "description: " + global_vars.DESCRIPTION_FILE + "\n"
    new_data += "documentation_file: " + global_vars.DOCUMENTATION_FILE + "\n"
    new_data += "description_file: " + global_vars.DESCRIPTION_FILE + "\n"
    new_data += "SHIFTS_CALENDER: " + global_vars.SHIFTS_CALENDER + "\n"
    new_data += "TALPIOT_DRIVE_ID: " + new_drive + "\n"
    new_data += "ORIGINAL_CALENDER: " + global_vars.ORIGINAL_CALENDER + "\n"
    new_data += "EMAIL_DATA: " + global_vars.EMAIL_FILE_NAME + "\n"
    with open("data_files/info.txt", "w") as info:
        info.write(new_data)


def add_docker(new_email):
    init()
    mails = ""
    with open(global_vars.EMAIL_FILE_NAME, "r") as emails:
        mails += new_email + "\n" + emails.read()
    with open(global_vars.EMAIL_FILE_NAME, "w") as emails:
        emails.write(mails)


def del_docker(new_email):
    init()
    mails = []
    with open(global_vars.EMAIL_FILE_NAME, "r") as emails:
        mails += emails.readlines()
        if new_email + "\n" in mails:
            mails.remove(new_email + "\n")
    with open(global_vars.EMAIL_FILE_NAME, "w") as emails:
        emails.write("".join(mails))


def add_non_activity(new_act):
    init()
    acti = ""
    with open(global_vars.NOT_ACTIVITIES, "r") as act:
        acti += new_act + "\n" + act.read()
    with open(global_vars.NOT_ACTIVITIES, "w") as act:
        act.write(acti)


def del_non_activity(new_email):
    init()
    mails = []
    with open(global_vars.NOT_ACTIVITIES, "r") as emails:
        mails += emails.readlines()
        if new_email + "\n" in mails:
            mails.remove(new_email + "\n")
    with open(global_vars.NOT_ACTIVITIES, "w") as emails:
        emails.write("".join(mails))
