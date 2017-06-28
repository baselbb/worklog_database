""" Import required built in python modules. 
to write task entries in database"""

from peewee import *

db = SqliteDatabase('task_manager.db')


class Task(Model):
    """ Class to create tasks and write to database """
    # define fields/columns of the database
    first_name = CharField()
    date = DateTimeField()
    task = CharField()
    time_spent = IntegerField()
    note = TextField()

    class Meta:
        database = db


# assign database tasks to our Task Model
def initialize():
    """ Create the database and the table if they don't exist"""
    db.connect()
    db.create_tables([Task], safe=True)

# add entry to our database

def add_row(emp_first, task_date, task_name, task_time, task_note):
    """
    Function to write task details to database Entry table

    Arguments required:
    emp_first: Employee  name
    task_date: Task Date in strf format
    task_name: Task Name as a string
    task_time: Time Spent on task in minutes
    task_note: Task Note, any additional notes on the task
    """

    # Write a row of task details using create row
    Task.create(first_name=emp_first,
                date=task_date,
                task=task_name,
                time_spent=task_time,
                note=task_note)

