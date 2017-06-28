""" Import required built in python modules.
to search for entries in database"""
import checkers
import datetime
from file_edit import Task
import menu

fmt = '%m/%d/%Y'


# Take a query and create a list of task items
def query_to_dict(query_result):
    """Prepares query final results in a dictionary for print output"""
    pagination = []
    for item in query_result:
        pagination.append({'First Name': item.first_name,
                           'Task Date': datetime.datetime.strftime(item.date, fmt),
                           'Task Name': item.task,
                           'Time Spent(mins)': item.time_spent,
                           'Task Note': item.note})

    return pagination


def emp_query(passed_query):
    """Function to choose final employee name to display entries for

    The function takes a valid name query and prints matching employee names
    Asks the user to select employee index number to see entries
    Returns final name for other function to make a final query for one employee name

    :param passed_query:
    :return: final employee for search
    """

    matching_names = []
    for person in passed_query:
        matching_names.append(person.first_name)

    print("We found the following names matching your search. ")
    for item in matching_names:
        print("{}. {}".format(matching_names.index(item)+1, item))

    while True:
        try:
            user_num = int(input("Please choose NUMBER of employee you are searching for > "))-1
        except ValueError:
            print("Oops!! This is not an integer")
        else:
            if (user_num + 1) > len(matching_names):
                print("Oops!!! Please choose a valid integer")
            else:
                final_name = [matching_names[user_num]]
                break

    unique_final = Task.select().where(Task.first_name == (final_name[0]))

    return unique_final


def search_employee():
    """Main function to search for entries for a specific employee

    :return: final_values dictionary holding entries for specific employee
    """
    all_query = (Task.select().group_by(Task.first_name))
    print("The following is a list of all employees available:\n"+"-"*50)
    for item in all_query:
        print(item.first_name)

    user_string = input("Please enter EMPLOYEE NAME > ")
    query = (Task.select()
             .where(Task.first_name.startswith(user_string))
             .group_by(Task.first_name))

    if len(list(query)) == 0:
        menu.clear_screen()
        print("Oops! No matching results for entered search string")
        search_employee()

    else:
        final_query = emp_query(query)
        final_values = query_to_dict(final_query)
        return final_values


def search_string():
    """Function for search for entries using a search string

    Asks user for search string
    Matches user string in task name and task notes
    :returns final_values dict holding final matching entry details

    """
    user_string = input("Please enter the search term you are looking for > ")
    query = (Task.select()
             .where((Task.task.contains(user_string)) |
                    (Task.note.contains(user_string))))
    final_values = query_to_dict(query)

    if len(final_values) == 0:
        print("Oops! No matching results for entered search string")

    return final_values


def search_time():
    """
    Method to search for task entries from database by Time spent on task
    in minutes
    """

    time_list = []
    # Print min-max range to help user choose with entries with minutes
    time_query = Task.select().group_by(Task.time_spent)
    for item in time_query:
        time_list.append(item.time_spent)
    print("""The min-max Time Spent on tasks is between {} - {} minutes"""
          .format(min(time_list), max(time_list)))

    # Check user input is valid int and available in search query
    while True:
        try:
            user_minutes = int(input("Please enter time spent on tasks in MINUTES > "))
        except ValueError:
            print("Not a valid minutes search selection.  Try again.")
        else:
            # Check if user minutes is in minute choices with available entries
            if user_minutes not in time_list:
                print("Oops! Minutes selected has no matching entries.")
            else:
                break

    # Append tasks for selected minutes including details
    time_query = Task.select().where(Task.time_spent == user_minutes)
    final_values = query_to_dict(time_query)
    return final_values


def date_printer():
    """Function to print all dates that have entrie"""

    date_query = Task.select().group_by(Task.date)
    print("""The following dates have entries:""")
    for item in date_query:
        print(datetime.datetime.strftime(item.date, fmt))


def date_checker():
    """Function to check user provided date for entry search is valid"""
    while True:
        date_string = input("""Enter date search for entries in MM/DD/YYYY format > """)
        if checkers.return_date_parsed(date_string):
            date_parsed = checkers.return_date_parsed(date_string)

            if not Task.select().where(Task.date == date_parsed):
                print("Oops! This date has no entries. Please select from the list above.")
            else:
                break

    return date_parsed


def search_date():
    """Function to search entries by date"""

    date_printer()
    user_parsed = date_checker()
    date_query = Task.select().where(Task.date == user_parsed)
    final_values = query_to_dict(date_query)

    return final_values


def search_range():
    """Method to search entries available based on date range"""

    date_printer()

    print("ENTER START DATE")
    start_parsed = date_checker()

    print("ENTER END DATE")
    end_parsed = date_checker()

    while True:
        if end_parsed < start_parsed:
            print("Oops! End date should be after your start date")
            search_range()
        else:
            break

    date_query = Task.select().where(Task.date.between(start_parsed, end_parsed))
    final_values = query_to_dict(date_query)
    return final_values
