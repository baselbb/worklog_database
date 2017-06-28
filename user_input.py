""" Import required datetime module for UserInput class and methods"""

import datetime
import checkers
""" Class to create and parse user input and write to a database table.

The class methods returns 6 values which are passed in menu.py to
file_edit.py to write the tasks in the database

"""


def ask_first():
    """
    Method to ask for employee for first name
    """
    # get employee first name
    emp_first = input("Please enter employee FULL NAME > ")

    return emp_first


def ask_date():
    """
    Method to ask for task date and returen in datetime format.
    """
    # Get task date, parse into datetime format
    while True:
        user_date = input("Enter task Date in MM/DD/YYY format > ")
        if checkers.return_date_parsed(user_date):
            output = checkers.return_date_parsed(user_date)
            break
    return output


def ask_name():
    """
    Method to ask user for task name.
    """
    #get task name
    task_name = input("Please enter task name >")

    return task_name


def ask_time():
    """
    Method to ask for task spent in minutes and check integer validity.
    """
    # get time spent on task in minutes
    while True:
        user_time = input("Please enter the time spent on task in minutes >")
        if checkers.return_int(user_time):
            output = checkers.return_int(user_time)
            break
    return output

# get additional notes by the user
def ask_note():
    """Function to ask user for task notes"""
    task_note = input("Enter any additional task notes here >")

    return task_note


