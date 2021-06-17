import tkinter as tk
from tkinter import ttk
import GUI
from tkmacosx import Button as button
from manager import spam_people, create_event, change_metadata
from manager.change_metadata import change_drive_id, init, change_calender_id, change_shifts_calender_id, add_docker, \
    del_docker, add_non_activity


def main():
    init()
    window = tk.Tk()
    window.configure(background='black')
    window.title("manager app")
    window.geometry('605x505')
    window.resizable(width=False, height=False)

    invite_text = tk.StringVar()
    invite_entry = tk.Entry(window, textvariable=invite_text)
    invite_entry.config(highlightbackground="black", highlightthickness=2, relief=tk.FLAT, fg='Khaki1', bg="black",
                        justify='center', font=("Courier", 20))
    invite_entry.insert(tk.END, 'amount:')
    invite_entry.place(x=120, y=140, height=30, width=150)
    invite_p = tk.PhotoImage(file='invite.png')
    invite = tk.Button(window, command=lambda: create_event.create_n_events(int(invite_text.get())), image=invite_p,
                       highlightbackground="#3E4149", highlightthickness=0, relief=tk.FLAT, pady=0, padx=0)
    invite.place(x=10, y=110)

    drive_p = tk.PhotoImage(file='drive.png')
    spam = tk.Button(window, command=lambda: change_drive_id(drive_str.get()), image=drive_p,
                     highlightbackground="#3E4149", highlightthickness=0, relief=tk.FLAT, pady=0, padx=0)
    spam.place(x=10, y=210)
    drive_str = tk.StringVar()
    spam_entry = tk.Entry(window, textvariable=drive_str)
    spam_entry.config(highlightbackground="black", highlightthickness=2, relief=tk.FLAT, fg='DarkGoldenrod1',
                      bg="black", justify='center', font=("Courier", 20))
    spam_entry.insert(tk.END, 'drive id:')
    spam_entry.place(x=120, y=240, height=30, width=150)

    calender_p = tk.PhotoImage(file='shifts.png')
    calender = tk.Button(window, command=lambda: change_shifts_calender_id(shifts_text.get()), image=calender_p,
                         highlightbackground="#3E4149", highlightthickness=0, relief=tk.FLAT, pady=0, padx=0)
    calender.place(x=10, y=310)
    calender_text = tk.StringVar()
    calender_entry = tk.Entry(window, textvariable=calender_text)
    calender_entry.config(highlightbackground="black", highlightthickness=2, relief=tk.FLAT, fg='snow3', bg="black",
                          justify='center', font=("Courier", 20))
    calender_entry.insert(tk.END, 'shifts id:')
    calender_entry.place(x=120, y=340, height=30, width=150)

    shifts_p = tk.PhotoImage(file='calender.png')
    shifts = tk.Button(window, command=lambda: change_calender_id(calender_text.get()), image=shifts_p,
                       highlightbackground="#3E4149", highlightthickness=0, relief=tk.FLAT, pady=0, padx=0)
    shifts.place(x=15, y=410)
    shifts_text = tk.StringVar()
    shifts_entry = tk.Entry(window, textvariable=shifts_text)
    shifts_entry.config(highlightbackground="black", highlightthickness=2, relief=tk.FLAT, fg='SteelBlue2', bg="black",
                        justify='center', font=("Courier", 20))
    shifts_entry.insert(tk.END, 'calender id:')
    shifts_entry.place(x=120, y=440, height=30, width=150)

    # spam_p = tk.PhotoImage(file='exit.png')
    # drive = tk.Button(window, command=window.destroy, image = spam_p,  highlightbackground = "#3E4149", highlightthickness = 0,relief = tk.FLAT, pady=0, padx=0)
    # drive.place(x=500, y=10)

    doc_p = tk.PhotoImage(file='plus.png')
    docker = tk.Button(window, command=lambda: add_docker(docker_test.get()), image=doc_p,
                       highlightbackground="#3E4149", highlightthickness=0, relief=tk.FLAT, pady=0, padx=0)
    docker.place(x=500, y=110)
    docker_test = tk.StringVar()
    docker_entry = tk.Entry(window, textvariable=docker_test)
    docker_entry.config(highlightbackground="black", highlightthickness=2, relief=tk.FLAT, fg='DarkSlategray3',
                        bg="black", justify='center', font=("Courier", 20))
    docker_entry.insert(tk.END, 'email:')
    docker_entry.place(x=340, y=140, height=30, width=150)

    n_doc_p = tk.PhotoImage(file='del.png')
    non_docker = tk.Button(window, command=lambda: del_docker(non_docker_test.get()), image=n_doc_p,
                           highlightbackground="#3E4149", highlightthickness=0, relief=tk.FLAT, pady=0, padx=0)
    non_docker.place(x=503, y=210)
    non_docker_test = tk.StringVar()
    non_docker_entry = tk.Entry(window, textvariable=non_docker_test)
    non_docker_entry.config(highlightbackground="Black", highlightthickness=2, relief=tk.FLAT, fg='brown3', bg="black",
                            justify='center', font=("Courier", 20))
    non_docker_entry.insert(tk.END, 'email:')
    non_docker_entry.place(x=340, y=240, height=30, width=150)

    act_p = tk.PhotoImage(file='plus2.png')
    non_activity = tk.Button(window, command=lambda: add_non_activity(add_activity_text.get()), image=act_p,
                             highlightbackground="#3E4149", highlightthickness=0, relief=tk.FLAT, pady=0, padx=0)
    non_activity.place(x=500, y=310)
    add_activity_text = tk.StringVar()
    non_activity_entry = tk.Entry(window, textvariable=add_activity_text)
    non_activity_entry.config(highlightbackground="Black", highlightthickness=2, relief=tk.FLAT, fg='PaleVioletRed1',
                              bg="black", justify='center', font=("Courier", 20))
    non_activity_entry.insert(tk.END, '!activity:')
    non_activity_entry.place(x=340, y=340, height=30, width=150)

    n_act_p = tk.PhotoImage(file='del2.png')
    del_non_activity = tk.Button(window, command=lambda: change_metadata.del_non_activity(del_activity_text.get()),
                                 image=n_act_p, highlightbackground="#3E4149", highlightthickness=0, relief=tk.FLAT,
                                 pady=0, padx=0)
    del_non_activity.place(x=503, y=410)
    del_activity_text = tk.StringVar()
    non_activity_entry = tk.Entry(window, textvariable=del_activity_text)
    non_activity_entry.config(highlightbackground="Black", highlightthickness=2, relief=tk.FLAT, fg='SeaGreen3',
                              bg="black", justify='center', font=("Courier", 20))
    non_activity_entry.insert(tk.END, '!activity:')
    non_activity_entry.place(x=340, y=440, height=30, width=150)

    var = tk.StringVar()
    var.set("TalpiDoc")
    header = tk.Label(window, textvariable=var)
    header.config(highlightthickness=2, relief=tk.FLAT, fg='white', bg="black", font=("Courier", 80))
    header.place(x=120, y=30, height=60, width=380)

    window.mainloop()


if __name__ == '__main__':
    main()
