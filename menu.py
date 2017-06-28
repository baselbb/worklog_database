""" Import required built in python modules
 and task functions """

import os

import user_input
import file_edit
import search_record
import checkers
import edit


# clear screen function when user quits or wants to return task program
def clear_screen():
    """
    Clear screen function when user runs main program script
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def main_choice():
    """Prints main menu user options"""
    print("Welcome to Task Manager.  From the menu below choose and option number")
    main_options = {1: 'Add a new task',
                    2: 'Search for a task',
                    3: 'Edit or Delete a task by Task Name',
                    4: 'Exit Menu'}
    
    main_chosen = checkers.option_printer(main_options)

    return main_chosen


# User selects choice to create a new task
def option_one():
    """Function to write a task to the database"""
    emp_first = user_input.ask_first()
    task_date = user_input.ask_date()
    task_name = user_input.ask_name()
    task_time = user_input.ask_time()
    task_note = user_input.ask_note()

    # initizlize database connection
    file_edit.initialize()
    # write task rows to the database
    file_edit.add_row(emp_first, task_date, task_name, task_time, task_note)

    clear_screen()
    print('Success! Entry added to your task manager')


def sub_menu():
    """Sub menu options to search database records"""
    clear_screen()
    search_options = {1: 'Find by Date',
                      2: 'Find by Time Spent',
                      3: 'Find by String Search(Task Name & Notes)',
                      4: 'Find by Employee Name',
                      5: 'Find by Date Range',
                      6: 'Exit Menu'}
    
    sub_chosen = checkers.option_printer(search_options)

    return sub_chosen


def option_two(choice_two):
    """Functions to for different methods to search the database"""
    if choice_two == 1:
        query_sub = search_record.search_date()
    elif choice_two == 2:
        query_sub = search_record.search_time()
    elif choice_two == 3:
        query_sub = search_record.search_string()
    elif choice_two == 4:
        query_sub = search_record.search_employee()
    elif choice_two == 5:
        query_sub = search_record.search_range()
    elif choice_two == 6:
        exit()
    else:
        print("Your choice:{} is not available".format(choice_two))
        sub_menu()

    return query_sub


def search_results(passed_dict):
    """Function to that calls pagination method to display search results"""
    # Print pagination menu of search results if returned results exists
    checkers.pagination_logic(passed_dict)


def run_app():
    """Main function to run task manager database program"""
    option_chosen = main_choice()
    clear_screen()

    # if user selects option one to add a new task to the database
    if option_chosen == 1:
        option_one()
        run_app()

    # calls functions to search records in the database
    elif option_chosen == 2:
        sub_choice = sub_menu()
        dict_results = option_two(sub_choice)
        search_results(dict_results)
        run_app()

    # calls functions to edit or delete records in the database
    elif option_chosen == 3:
        edit.edit_app()
        run_app()

    elif option_chosen == 4:
        exit()

    else:
        print("Your choice is not available")
        run_app()
    

if __name__ == "__main__":
    clear_screen()
    run_app()
