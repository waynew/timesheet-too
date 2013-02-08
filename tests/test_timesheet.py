import unittest

from datetime import datetime
from timesheet import Timesheet

class GivenNewTimesheet(unittest.TestCase):

    def setUp(self):
        self.timesheet = Timesheet()
        

    def test_it_should_have_no_time_spent(self):
        self.assertEqual(0, self.timesheet.time_spent())


    def test_adding_time_with_no_parameters_should_TypeError(self):
        with self.assertRaises(TypeError):
            self.timesheet.add_time()


    def test_adding_time_with_bad_format_should_ValueError(self):
        with self.assertRaises(ValueError):
            self.timesheet.add_time("1234")


    def test_adding_time_with_HH_MM_AM_should_not_ValueError(self):
        self.timesheet.add_time("12:42 AM")


    def test_adding_time_with_HH_MM_PM_should_not_ValueError(self):
        self.timesheet.add_time("2:12 PM")


    def test_adding_time_with_two_HH_MM_AM_should_not_error(self):
        self.timesheet.add_time("3:13 AM", "5:17 PM")


    def test_adding_time_with_good_start_bad_end_should_ValueError(self):
        with self.assertRaises(ValueError):
            self.timesheet.add_time("4:14 PM", "sdfkj23")

    
    def test_adding_time_with_good_start_good_end_should_not_error(self):
        self.timesheet.add_time("12:00 AM", "3:33 AM")


    def test_adding_time_with_good_start_end_and_any_task_should_not_error(self):
        self.timesheet.add_time("12:00 AM", "4:44 PM", "fnord")


    def test_adding_time_with_good_start_end_any_task_and_proj_should_not_error(self):
        self.timesheet.add_time("1:43 AM", "4:12 AM", "fnord", "999")

    def test_adding_time_with_good_start_thru_proj_and_bad_date_should_ValueError(self):
        with self.assertRaises(ValueError):
            self.timesheet.add_time("9:42 AM",
                                    "9:59 AM",
                                    "fnord",
                                    "fizz",
                                    "Silly non-date")


    def test_adding_time_with_good_vals_and_good_date_should_not_error(self):
        self.timesheet.add_time("8:12 AM",
                                "8:13 AM",
                                "fnord",
                                "fizzy",
                                "2010-08-14")


class GivenTimesheetWithOneTaskWithStartAndEnd(unittest.TestCase):
    def setUp(self):
        self.timesheet = Timesheet()
        self.timesheet.add_time("10:45 AM", "11:00 AM")


    def test_it_should_use_current_date_as_default(self):
        self.assertEqual(datetime.today().date(),
                         self.timesheet.tasks[-1].date)


    def test_the_project_should_be_None_by_default(self):
        self.assertIsNone(self.timesheet.tasks[-1].project)


    def test_the_task_should_be_None_by_default(self):
        self.assertIsNone(self.timesheet.tasks[-1].task)


    def test_current_task_should_be_None(self):
        self.assertIsNone(self.timesheet.current_task)


class GivenTimesheetWithOneFullyLoadedTask(unittest.TestCase):
    def setUp(self):
        self.start_time = "1:44 AM"
        self.end_time = "9:08 PM"
        self.date = "2010-08-14"
        self.project  = "Silly Project"
        self.task = "Put on some pants"

        self.timesheet = Timesheet()
        self.timesheet.add_time(self.start_time,
                                self.end_time,
                                proj=self.project,
                                task=self.task,
                                date=self.date)


    def test_it_should_use_provided_project(self):
        self.assertEqual(self.project,
                         self.timesheet.tasks[-1].project)


    def test_it_should_use_provided_task(self):
        self.assertEqual(self.task,
                         self.timesheet.tasks[-1].task)



class GivenTimesheetWithOpenInterval(unittest.TestCase):

    def setUp(self):
        self.start_time = "10:13 AM"
        self.timesheet = Timesheet()
        self.timesheet.add_time(self.start_time)

    def test_current_task_should_return_something(self):
        self.assertIsNotNone(self.timesheet.current_task)


    def test_current_task_should_have_correct_start_time(self):
        self.assertEqual(self.start_time,
                         self.timesheet.current_task.start.strftime('%I:%M %p'))

