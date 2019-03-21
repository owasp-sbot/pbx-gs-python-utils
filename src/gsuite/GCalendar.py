import datetime

from gsuite.GSuite import GSuite
from gsuite.GDrive import GDrive
from utils.Dev import Dev


class GCalendar:

    def __init__(self, gsuite_secret_id=None):
        self.events = GSuite(gsuite_secret_id).calendar_v3().events()
        self.calendar_id = 'photobox.com_kkecukq11iksaamp12p5mqdku0@group.calendar.google.com'

    def next_10(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print('Getting the upcoming 10 events')
        events_result = self.events.list(calendarId=self.calendar_id, timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        return events_result.get('items', [])