""" Import required modules for RecordChange class and methods
Import UserInput class to manage validation of user input when
editing task details such as datetimes.
"""
import datetime
import user_input
from file_edit import Task
import checkers
import menu


# Gets user choice to either edit or delete a task
def choice():
    """Function to edit or delete chosen task"""
    while True:
        try:
            user_choice = int(input("Would like to:\n"+
                                    "1: Edit\n"+
                                    "2: Delete\n"+
                                    "3: Go back to Main Menu > "))
            if user_choice in [1, 2, 3]:
                break
            else:
                print("Not a valid NUMBER choice.  Choose again")
        except ValueError:
            print("Not a valid INTEGER choice")

    return user_choice


# Function to to check if a user task name is available for edit
def search_valid_name(name_input):
    """Function to check user string for task name to edit
    Arguments required: User input for task name
    """
    query = Task.select().where(Task.task.contains(name_input))
    if len(list(query)) > 0:
        print("Matching Result\n" +
              "-" * 30)
        for task in query:
            print("id: {} \nTask Name: {}".format(task.id, task.task))
    else:
        menu.clear_screen()
        print("Oops! No matching results for Task Name: {}".format(name_input) +
              "\nBelow is a list of available Task Names to help you choose:\n"+
              "-" * 30)
        for task in Task.select():
            print("Task id: {} Task Name: {}".format(task.id, task.task))
        edit_app()

    return query


# Function to get task ids for user to choose from
def matching_id(query):
    """Function that lists ids of matching tasks"""
    valid_ids = []
    for task in query:
        valid_ids.append(task.id)

    return valid_ids


# Function for user to select ID of task and check if ID number is valid
def select_id(id_list):
    """Function to select task id to edit or delete
    Arguments Required: task id list with matching entries
    """
    while True:
        try:
            user_id = int(input("Enter Task ID to confirm Edit or Delete Process >  "))
            if user_id not in id_list:
                print("Please choose an INTEGER from LIST above!")
            else:
                break
        except ValueError:
            print("Not a valid integer")
    return user_id


def print_task(selected_id):
    """"Function to print selected task details """
    print("Below is the Entry selected to edit or delete\n" +
          '-'*30)
    selected_query = Task.select().where(Task.id == selected_id)
    for task in selected_query:
        print("Name: " + task.first_name,
              "\nDate : " + datetime.datetime.strftime(task.date, '%m/%d/%Y'),
              "\nTask Name: " + task.task,
              "\nTime Spent: " + str(task.time_spent),
              "\nTask Note:" + task.note)
    print('-'*30)


# Get user selected header to edit and check if it is a valid field name
def select_task_header():
    """Function to select what field to edit"""
    while True:
        try:
            header_edit = int(input("What would you like to edit:"
                                    "\n1.Date\n2.Task Name\n3.Time Spent\n4.Task Note\n > """))
            if header_edit in [1, 2, 3, 4]:
                break
            else:
                print("Not a valid ITEM to edit.  Try Again")
        except ValueError:
            print("Please choose an integer")

    return header_edit


def edit_task(task_id, header_id):
    """Function to edit task

    Arguments Required: task id and field name to edit
    Field Headers indexes:
    1.Date
    2.Task Name
    3.Time Spent
    4.Task Note

    """
    # select Task query to edit from given user_id
    edit_details = Task.select().where(Task.id == task_id).get()

    # Ask user for the replacement value by calling methods in class UserInput and append output to output list
    print("Please enter the new value")
    if header_id == 1:
        new_value = user_input.ask_date()
        edit_details.date = new_value
    elif header_id == 2:
        new_value = user_input.ask_name()
        edit_details.task = new_value
    elif header_id == 3:
        new_value = user_input.ask_time()
        edit_details.time_spent = new_value
    elif header_id == 4:
        new_value = user_input.ask_note()
        edit_details.note = new_value

    # save new edit details to database
    edit_details.save()
    print("Success! New task details saved")


# DELETE a task, user selected task for deletion is omitted from final list
def delete_task(task_id):
    """Function that calls delete task method

    Arguments Required: selected task id
    """
    checkers.delete_task(task_id)
    
    
def edit_app():
    """Main function that rund edit and delete methods"""

    # get user input for a task name
    user_string = input("Enter a Task NAME to edit or delete > ")

    # check that string is valid and search for matching tasks
    valid_string = search_valid_name(user_string)

    # get matching list of task ids
    matching_list = matching_id(valid_string)

    # Ask user to confirm the task using task database id
    id_to_edit = select_id(matching_list)

    edit_menu_selection = choice()

    if edit_menu_selection == 1:
        edit_field = select_task_header()
        edit_task(id_to_edit, edit_field)
    elif edit_menu_selection == 2:
        delete_task(id_to_edit)
