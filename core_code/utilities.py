import os
import sqlite3


def admin_login():
    while True:
        password = input("Input the password of admin:")
        if str(password) == "12345":
            print(f'\nWelcome to the system, Admin.')
            return
        else:
            print("Wrong password! Check your input please.")


def volunteer_login():
    with sqlite3.connect('info_files/emergency_system.db') as conn:
        c = conn.cursor()
        while True:
            name = input("Input your username:")
            password = input("Input the password of volunteer:")

            result = c.execute(f"select volunteerID from volunteer where username = '{name}' and password = '{password}'").fetchall()
            if len(result) > 0:
                print(f'\nWelcome to the system, {name}.')
                return result[0][0]
            else:
                print("Wrong username or password! Check your input please.")


