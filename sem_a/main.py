import create_event
import drive
import spam_people
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


def main():
    init()
    choice = input("what do you want to do?\npress s for spam!!\n"
                   "press gs for search!!\n"
                   "press anything else to create events\n"
                   "your choise: ")
    if choice == "s":
        spam_people.spam_everyone()
    elif choice == 'gs':
        drive.search()
    else:
        print("\n"*10)
        events_num = int(input("how much events? "))
        print("\n" * 10)
        create_event.create_n_events(events_num)


if __name__ == '__main__':
    main()
