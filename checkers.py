"""Import modules and file_edit module"""
import datetime
import menu
from file_edit import *

# datetime format of the database
fmt = '%m/%d/%Y'


# Function to print a dictionary items
def dict_printer(dict_item):
    """Print dictionary items"""
    for key, value in dict_item.items():
        print("{}: {}".format(key, value))


# function to print menu options
def option_printer(set_item):
    """Print menu options"""
    dict_printer(set_item)
    counter = 0
    while True:
        try:
            user_option = int(input("Please enter you chosen OPTION NUMBER here > "))
            if user_option > len(set_item):
                print("Chosen option is not available")
            else:
                break
        except ValueError:
            print("Not a valid choice number")

        counter += 1
        if counter > 5:
            raise ValueError('Invalid input')

    return user_option


# Function that returns string date as datetime format
def return_date_parsed(user_input):
    """Function to that returns a parsed date from user string"""
    try:
        parsed_date = datetime.datetime.strptime(user_input, fmt)
    except ValueError:
        print("Oops! Not a valid date format.")
    else:
        return parsed_date


# Function that returns datetime date as a string
def return_date_string(user_input):
    """Function that returns string date from datetime format string date"""
    try:
        string_date = datetime.datetime.strftime(user_input, fmt)
    except ValueError:
        print("Oops! Not a valid integer format.")
    else:
        return string_date


# Function to check user input is a valid integer
def return_int(user_input):
    """Function to check and return an integer from user input"""
    try:
        user_int = int(user_input)
    except ValueError:
        print("Oops! Not a valid integer format.")
    else:
        return user_int


# function to delete a task
def delete_task(id_provided):
    """Function to delete a task using the task database provided id"""
    delete_row = Task.get(Task.id == id_provided)
    delete_row.delete_instance()
    print("Success! Task Deleted")


#  paginate through search results
def pagination_menu(returned):
    """Search results pagination menu
    Arguments required: dictionary of database query search results
    """
    len_returned = len(returned)
    print('RESULTS OUTPUT\n',
          "{} matching entries\n".format(len_returned),
          "-" * 30,
          "\nTo page through entries use the following commands:",
          "\n[N]ext entry",
          "\n[P]revious entry",
          "\n[M]ain menu\n",
          '-' * 30)


# Pagination output of search result entries, displayed one by one
def pagination_logic(returned):
    """Function with logic to paginate through search results
    Arguments required: dictionary of database query search results
    """

    pagination_menu(returned)
    len_returned = len(returned)
    counter = 0

    while counter < len_returned:
        pagination = input("Enter letters [N], [P] or [M] > ").lower()
        if pagination == 'n':
            print("Result {} out of {}\n".format(counter + 1, len_returned),
                  "-" * 30)
            for key, values in returned[counter].items():
                print("{}: {}".format(key, values))
            print("-" * 30)
            counter += 1

        elif pagination == 'p':
            if counter == 0:
                print("You have reached beginning of list")
            else:
                print("Result {} out of {}\n".format(counter + 1, len_returned),
                      "-" * 30 + "\n" + "-" * 30)
                for key, values in returned[counter].items():
                    print("{}: {}".format(key, values))
                counter -= 1

        elif pagination == 'm':
            menu.run_app()
        else:
            print("Choice not valid. Enter letters [N], [P] or [M] ")
    

