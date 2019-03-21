from unittest import TestCase
from gsuite.GCalendar import GCalendar
from utils.Dev import Dev


class Test_GCalendar(TestCase):
    def setUp(self):
        self.calendar = GCalendar()

    def test_next_10(self):
        events = self.calendar.next_10()
        for event in events:
            Dev.pprint(event.get('summary'))