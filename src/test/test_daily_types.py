import unittest
import daily_types as dt


class TestDailyTypes(unittest.TestCase):

    def test_task_get_default(self):
        expected = '=>\tnothing'
        self.assertEqual(dt.Task.get_default().to_str(), expected)
