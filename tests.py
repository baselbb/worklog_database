import unittest
from unittest.mock import patch
from unittest import mock

import datetime

import menu
import user_input
from file_edit import Task
import file_edit
import search_record
import edit
import checkers


class DBCreate(unittest.TestCase):
    """Class to create and assert database test row created"""

    def test_add_row(self):

        file_edit.add_row('TEST',
                          datetime.datetime.strptime('12/12/2012', '%m/%d/%Y'),
                          'UNITTEST',
                          999,
                          'NONE')

        query = Task.select().where(Task.first_name == 'TEST')

        assert len(list(query)) >= 1


class CheckerTests(unittest.TestCase):
    """Class to test functions in checkers.py"""

    @patch('checkers.option_printer', return_value=1)
    def test_option_printer_valid_input(self, option_printer):
        sample_dict = {
            1: 'value',
            2: 'two'
        }
        ret_val = option_printer(sample_dict)
        self.assertEqual(ret_val, 1)
        self.assertIn(ret_val, sample_dict)

    def test_option_printer_patch_input_invalid(self):
        sample_dict = {
            1: 'value',
            2: 'two'
        }
        with patch('builtins.input', return_value='2s'):
            self.assertRaises(ValueError, checkers.option_printer, sample_dict)

    def test_option_printer_patch_input_valid(self):
        sample_dict = {
            1: 'value',
            2: 'two'
        }
        with patch('builtins.input', return_value='2'):
            self.assertEqual(checkers.option_printer(sample_dict), 2)

    def test_return_date_parsed(self):
        fake_date = '12/12/2012'
        self.assertEqual(checkers.return_date_parsed(fake_date),
                         datetime.datetime.strptime(fake_date, '%m/%d/%Y'))

    def test_return_date_string(self):
        fake_date = datetime.datetime.strptime('12/12/2012', '%m/%d/%Y')
        self.assertEqual(checkers.return_date_string(fake_date),
                         datetime.datetime.strftime(fake_date, '%m/%d/%Y'))

    def test_return_int(self):
        self.assertEqual(checkers.return_int(str(5)), 5)

    @patch('checkers.pagination_logic')
    def test_pagination_logic(self, pagination_logic):
        test_list = {'key': 'value'}
        pagination_logic.return_value = test_list
        assert checkers.pagination_logic(test_list) == test_list


class UserInputTests(unittest.TestCase):
    """Class to test functions in user_input.py"""

    @patch('user_input.ask_first', return_value='Robert')
    def test_ask_first(self, input):
        self.assertEqual(user_input.ask_first(), 'Robert')

    @patch('user_input.ask_name', return_value='TaskName')
    def test_ask_name(self, input):
            self.assertEqual(user_input.ask_name(), 'TaskName')

    @patch('user_input.ask_date', return_value='12/12/2012')
    def test_ask_date(self, input):
        self.assertEqual(user_input.ask_date(), '12/12/2012')

    @patch('user_input.ask_time', return_value=500)
    def test_ask_time(self, input):
        self.assertEqual(user_input.ask_time(), 500)

    @patch('user_input.ask_note', return_value='TaskNote')
    def test_ask_note(self, input):
        self.assertEqual(user_input.ask_note(), 'TaskNote')


class MenuTests(unittest.TestCase):
    """Class to test function menu.py"""

    @patch('menu.main_choice', return_value=1)
    def test_main_choice(self, input):
        self.assertEqual(menu.main_choice(), 1)

    @patch('menu.sub_menu', return_value=1)
    def test_sub_menu(self, input):
        self.assertEqual(menu.sub_menu(), 1)

    def test_option_two(self):
        query = Task.select().where(Task.first_name == 'Test')

        with patch('builtins.input', return_value='12/12/2012'):
            self.assertEqual(menu.option_two(1), query)

        with patch('builtins.input', return_value='999'):
            self.assertEqual(menu.option_two(2), query)

        with patch('builtins.input', return_value='UNITTEST'):
            self.assertEqual(menu.option_two(3), query)


class TestSearchRecord(unittest.TestCase):
    """Class to test function for searching entries in
    search_record.py
    """

    @mock.patch('search_record.query_to_dict')
    def test_query_to_dict(self, query_to_dict):
        query = Task.select().where(Task.time_spent == 500)
        result = search_record.query_to_dict(query)
        query_to_dict.return_value = query
        assert search_record.query_to_dict(query) == result

    def test_emp_query(self):
        query = Task.select().where(Task.first_name == 'Sara')
        with mock.patch('builtins.input', return_value='1'):
           assert len(list(search_record.emp_query(query))) == 1

    def test_search_string(self):
        query = Task.select().where(Task.first_name == 'Sara')
        with mock.patch('builtins.input', return_value='Sara'):
            assert search_record.search_string() == query

    def test_search_time(self):
        with mock.patch('builtins.input', return_value='555'):
            assert len(list(search_record.search_time())) == 1

    @patch('search_record.date_checker', return_value='12/12/2012')
    def test_date_checker(self, input):
        self.assertEqual(search_record.date_checker(), '12/12/2012')


class TestEdit(unittest.TestCase):
    """Class to test functions to edit a database entry"""

    @mock.patch('edit.search_valid_name')
    def test_search_valid_name(self, search_valid_name):
        search_valid_name.return_value = 'Sara'
        assert edit.search_valid_name('Sara') == 'Sara'

    def test_matching_id(self):
        query = Task.select().where(Task.first_name == 'Sara')
        with mock.patch('builtins.input', query):
            assert len(list(edit.matching_id(query))) == 1

    def test_select_id(self):
        with mock.patch('builtins.input', return_value='1'):
            assert edit.select_id([1]) == 1

    def test_choice(self):
        with patch('builtins.input', return_value='1'):
            self.assertEqual(edit.choice(), 1)

    def test_select_task_header(self):
        with patch('builtins.input', return_value='1'):
            self.assertEqual(edit.select_task_header(), 1)

    def test_edit_task(self):
        headers = ['Date', 'Task Name', 'Time Spent', 'Task Note']
        query = Task.select().where(Task.first_name == 'TEST')
        id = []
        for item in query:
            id.append(item.id)

        newdate = '9/9/2009'
        with patch('builtins.input', return_value=newdate):
            edit.edit_task(id[0], 1)
        query = Task.select().where(Task.date == datetime.datetime.strptime(newdate, '%m/%d/%Y'))
        assert len(list(query)) >= 1

        newname = 'NEWTEST'
        with patch('builtins.input', return_value=newname):
            edit.edit_task(id[0], 2)
        query = Task.select().where(Task.task == newname)
        assert len(list(query)) >= 1

        newtime = 777
        with patch('builtins.input', return_value=newtime):
            edit.edit_task(id[0], 3)
        query = Task.select().where(Task.time_spent == newtime)
        assert len(list(query)) >= 1

        newnote = 'NEWNOTE'
        with patch('builtins.input', return_value=newnote):
            edit.edit_task(id[0], 4)
        query = Task.select().where(Task.note == newnote)
        assert len(list(query)) >= 1

    def test_delete_task(self):
        query = Task.select().where(Task.first_name == 'TEST')
        id = []
        for item in query:
            id.append(item.id)

        checkers.delete_task(id[0])
        query = Task.select().where(Task.task == 'NEWTEST')
        assert len(list(query)) == 0


if __name__ == '__main__':
    unittest.main()
