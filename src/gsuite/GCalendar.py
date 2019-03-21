import datetime

from gsuite.GSuite import GSuite
from gsuite.GDrive import GDrive
from utils.Dev import Dev


class GCalendar:

    def __init__(self, gsuite_secret_id=None):
        self.events = GSuite(gsuite_secret_id).calendar_v3().events()


    def gs_team(self):
        self.calendar_id = 'photobox.com_kkecukq11iksaamp12p5mqdku0@group.calendar.google.com'
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        #Dev.pprint(now
        time_min = '2019-03-17T00:00:00Z'
        time_max = '2019-03-23T00:00:00Z'
        #time_min = "2019-03-17T05:00:00-06:00Z",
        #time_max = "2017-03-23T20:00:01-06:00Z",
        events_result = self.events.list(calendarId = self.calendar_id,
                                         timeMin    = time_min,
                                         timeMax    = time_max,
                                         #maxResults=100,
                                         singleEvents=True,
                                         orderBy='startTime').execute()
        return events_result.get('items', [])