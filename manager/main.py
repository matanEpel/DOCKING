import create_event
import drive
import spam_people
import global_vars
import change_metadata
import GUI

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
    while True:
        print("\n"*10)
        choice = input("what do you want to do?\n"
                       "1. spamming people who haven't documented.\n"
                       "2. search a file in the drive.\n"
                       "3. create events.\n"
                       "4. change calender id.\n"
                       "5. change drive id.\n"
                       "6. add somone to doc.\n"
                       "7. delete someone to doc.\n"
                       "8. add non activity.\n"
                       "9. del non activity\n"
                       "10. change shifts calender id\n"
                       "anything else to quit\n"
                       "your choise: ")
        if choice == "1":
            spam_people.spam_everyone()
        elif choice == '2':
            drive.search()
        elif choice == "3":
            print("\n"*10)
            events_num = int(input("how much events? "))
            print("\n" * 10)
            create_event.create_n_events(events_num)
        elif choice == '4':
            change_metadata.change_calender_id()
        elif choice == '5':
            change_metadata.change_drive_id()
        elif choice == '6':
            change_metadata.add_docker()
        elif choice == '7':
            change_metadata.del_docker()
        elif choice == '8':
            change_metadata.add_non_activity()
        elif choice == '9':
            change_metadata.del_non_activity()
        elif choice == "10":
            change_metadata.change_shifts_calender_id()
        else:
            return


if __name__ == '__main__':
    GUI.main()
