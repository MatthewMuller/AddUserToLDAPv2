import tkinter as tk
from tkinter import messagebox
import sys


'''
This function is used to build the GUI used to enter information
about the user being added to the LDAP.
'''


def gui(window):

    window.title("Add a user to the LDAP")

    ############################
    #      LEFT COLUMN         #
    ############################

    # First Name
    first_name = tk.Label(window, text="First Name")
    first_name.grid(column=0, row=0, padx=(20, 0), pady=(20, 0))
    first_name_entry = tk.Entry(window)
    first_name_entry.grid(column=0, row=1, padx=(20, 0), pady=(20, 0))

    # Last Name
    last_name = tk.Label(window, text="Last Name")
    last_name.grid(column=0, row=2, padx=(20, 0), pady=(20, 0))
    last_name_entry = tk.Entry(window)
    last_name_entry.grid(column=0, row=3, padx=(20, 0), pady=(20, 0))

    # User Name
    user_name = tk.Label(window, text="User Name")
    user_name.grid(column=0, row=4, padx=(20, 0), pady=(20, 0))
    user_name_entry = tk.Entry(window)
    user_name_entry.grid(column=0, row=5, padx=(20, 0), pady=(20, 0))

    ############################
    #      RIGHT COLUMN        #
    ############################

    # Enter Password
    enter_password = tk.Label(window, text="Enter Password")
    enter_password.grid(column=3, row=0, padx=(0, 20), pady=(20, 0))
    enter_password_entry = tk.Entry(window, show="*")
    enter_password_entry.grid(column=3, row=1, padx=(0, 20), pady=(20, 0))

    # Verify Password
    verify_password = tk.Label(window, text="Verify Password")
    verify_password.grid(column=3, row=2, padx=(0, 20), pady=(20, 0))
    verify_password_entry = tk.Entry(window, show="*")
    verify_password_entry.grid(column=3, row=3, padx=(0, 20), pady=(20, 0))

    # Admin Password
    admin_password = tk.Label(window, text="LDAP Admin Password")
    admin_password.grid(column=3, row=4, padx=(0, 20), pady=(20, 0))
    admin_password_entry = tk.Entry(window, show="*")
    admin_password_entry.grid(column=3, row=5, padx=(0, 20), pady=(20, 0))

    ############################
    #     ADD USER BUTTON      #
    ############################

    # Add user button - We need the lambda function because we are passing in parameters
    btn = tk.Button(window, text="Add User", command=lambda: add_user_button_pressed(first_name_entry,
                                                                                     last_name_entry,
                                                                                     user_name_entry,
                                                                                     enter_password_entry,
                                                                                     verify_password_entry,
                                                                                     admin_password_entry))
    btn.grid(column=2, row=6, padx=(20, 20), pady=(20, 20))

    return window


'''
This function is called when a user hits the "Add User" button
in the GUI. It will verify the passwords match. If so, it will
add the user. Otherwise, it will prompt the user of the issue
and return them to the gui.
'''


def add_user_button_pressed(fn, ln, un, pw, vp, ap):

    # If the passwords don't match, let the user know and go back to main gui
    if pw.get() != vp.get():
        messagebox.showinfo("Passwords Don't Match!", "The passwords entered by the user do not match!")
        return

    # If the password contains a space, let the user know and go back to main gui
    if " " in pw.get():
        messagebox.showinfo("Passwords Contains a Space!", "The password is not allowed to contain a space!")
        return

    # If any of the fields are empty, let the user know and go back to main gui
    if fn.index("end") == 0 or ln.index("end") == 0 or un.index("end") == 0 \
            or pw.index("end") == 0 or vp.index("end") == 0 or ap.index("end") == 0:
        messagebox.showinfo("Empty Fields!", "Not all entry fields have been populated.")
        return

    # Check to see if the last name is in the user name. If not, warn the
    # user the username could possibly be incorrect
    if str(ln.get().lower()) not in str(un.get().lower()):
        messagebox.showinfo("Warning!", "The username does not contain the last name! The entry might not be correct.")

    # Verify with the user they truly want to add new user to LDAP
    add_user_last_chance_verification_popup(fn, ln, un, pw, ap)


def add_user_last_chance_verification_popup(fn, ln, un, pw, ap):
    popup_window = tk.Tk()
    popup_window.wm_title("Verify")
    popup_label = tk.Label(popup_window, text="Are you sure you want to add this user to the LDAP?")
    popup_label.grid(column=0, row=0, columnspan=2, padx=(20, 20), pady=(20, 20))
    popup_button = tk.Button(popup_window, text="Add To LDAP",
                             command=lambda: pipe_input_to_script(fn, ln, un, pw, ap))
    popup_button.grid(column=0, row=1, padx=(20, 20), pady=(20, 20))
    popup_button = tk.Button(popup_window, text="Go Back", command=popup_window.destroy)
    popup_button.grid(column=1, row=1, padx=(20, 20), pady=(20, 20))


def pipe_input_to_script(fn, ln, un, pw, ap):
    # TODO write a function that pipes the user input to the bash script
    # This needs to be tested inside of a bash script
    # Output will collect these in an array and terminate at sentinel value -1
    sys.stderr.write(fn.get() + " ")
    sys.stderr.write(ln.get() + " ")
    sys.stderr.write(un.get() + " ")
    sys.stderr.write(pw.get() + " ")
    sys.stderr.write(ap.get())

    exit()


def test_pipe_input_to_script():

    window = tk.Tk()
    window = gui(window)

    fne = tk.Entry(window)
    lne = tk.Entry(window)
    une = tk.Entry(window)
    pwe = tk.Entry(window)
    ape = tk.Entry(window)

    fn = "test" 
    ln = "dummy"
    un = "dummyt"
    pw = "0000"
    ap = ""

    fne.insert(0, fn)
    lne.insert(0, ln)
    une.insert(0, un)
    pwe.insert(0, pw)
    ape.insert(0, ap)

    pipe_input_to_script(fne, lne, une, pwe, ape)


'''
Main driver that builds and launches the gui
'''
if __name__ == "__main__":

    inputWindow = tk.Tk()
    inputWindow = gui(inputWindow)
    inputWindow.mainloop()