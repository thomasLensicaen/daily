import unittest
import daily_types as dt



class TestDailyTypesI(unittest.TestCase):

    def test_task_get_default(self):
        print(dt.Task.get_default().to_str())
        print(dt.Task.get_default())
