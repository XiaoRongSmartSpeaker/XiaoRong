from pprint import pprint
from datetime import datetime, timedelta, date
from cal_setup import get_calendar_service
from TextToSpeech import TextToSpeech


class Calendar:
    def __init__(self):
        pass

    def add_calendar(self, s_time, e_time, event):
        self.s_time = s_time
        self.e_time = e_time
        self.event = event

        # set hour adjustment with seconds attached
        hour_adjustment = ':00+08:00'
        service = get_calendar_service()

        today = datetime.today()
        # see if both are valid time
        # set end time as start time + 1hr if no value
        if(e_time == None):
            e_time = datetime.strptime(
                s_time, "%Y-%m-%d %H:%M") + timedelta(hours=1)
            e_time = e_time.strftime("%Y-%m-%dT%H:%M")
        # see if s_time < e_time, if not then add one day to e_time
            
        else:
            t1 = datetime.strptime(s_time, "%Y-%m-%d %H:%M")
            t2 = datetime.strptime(e_time, "%Y-%m-%d %H:%M")
            if(t1 >= t2):
                # inc e_time date
                e_time = datetime.strptime(
                    e_time, "%Y-%m-%d %H:%M") + timedelta(days=1)
                e_time = e_time.strftime("%Y-%m-%dT%H:%M")
        # see if is past time, if so then add a year
        if(datetime.strptime(s_time, "%Y-%m-%d %H:%M") < today):
            s_time = datetime.strptime(
                s_time, "%Y-%m-%d %H:%M") + timedelta(days=365)
            e_time = datetime.strptime(
                e_time, "%Y-%m-%d %H:%M") + timedelta(days=365)
            s_time = s_time.strftime("%Y-%m-%dT%H:%M")
            e_time = e_time.strftime("%Y-%m-%dT%H:%M")

        s_time = s_time.replace(' ', 'T')
        e_time = e_time.replace(' ', 'T')

        event_request_body = {
            'start': {
                #date and time
                'dateTime': s_time+hour_adjustment,
                'timeZone': 'Asia/Taipei'
            },
            'end': {
                #date and time
                'dateTime': e_time+hour_adjustment,
                'timeZone': 'Asia/Taipei'
            },
            "reminders": {
                "useDefault": False,
            },
            'summary': event,  # event name
            'colorId': 5,
            'status': 'confirmed',
            'transparency': 'opaque',
            'visibility': 'private',
        }

        sendNotification = False
        sendUpdate = 'none'

        response = service.events().insert(
            calendarId='primary',
            sendNotifications=sendNotification,
            sendUpdates=sendUpdate,
            body=event_request_body
        ).execute()
        if(response):
            text_to_speech('行事歷添加成功')
            print('success')

    def add_calendar_day(self, s_time, e_time, event):
        self.s_time = s_time
        self.e_time = e_time
        self.event = event

        # set hour adjustment
        hour_adjustment = ':00+08:00'
        service = get_calendar_service()

        today = date.today()

        # set end time as start time + 1 if no value
        if(e_time == None):
            e_time = datetime.strptime(
                str(today)+'T'+s_time, "%Y-%m-%dT%H:%M") + timedelta(hours=1)
            e_time = e_time.strftime("%Y-%m-%dT%H:%M")
        # see if s_time < e_time, if not then add one day to e_time
        else:
            t1 = datetime.strptime(s_time, "%H:%M")
            t2 = datetime.strptime(e_time, "%H:%M")
            if(t1 >= t2):
                # inc e_time date
                e_time = datetime.strptime(
                    str(today)+'T'+e_time, "%Y-%m-%dT%H:%M") + timedelta(days=1)
                e_time = e_time.strftime("%Y-%m-%dT%H:%M")
            else:
                e_time = str(today) + 'T' + e_time

        # pprint(e_time)
        until_time = str(today.year) + '1231T240000Z'
        # pprint(until_time)

        event_request_body = {
            'start': {
                #date and time
                'dateTime': str(today)+'T'+s_time+hour_adjustment,
                'timeZone': 'Asia/Taipei'
            },
            'end': {
                #date and time
                'dateTime': e_time+hour_adjustment,
                'timeZone': 'Asia/Taipei'
            },
            "reminders": {
                "useDefault": False,
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;UNTIL=' + until_time,
            ],
            'summary': event,  # event name
            'colorId': 5,
            'status': 'confirmed',
            'transparency': 'opaque',
            'visibility': 'private',
        }

        sendNotification = False
        sendUpdate = 'none'

        response = service.events().insert(
            calendarId='primary',
            sendNotifications=sendNotification,
            sendUpdates=sendUpdate,
            body=event_request_body
        ).execute()
        if(response):
            text_to_speech('行事歷添加成功')
            print('success')

    def add_calendar_week(self, day, s_time, e_time, event):
        self.day = day
        self.s_time = s_time
        self.e_time = e_time
        self.event = event

        # set hour adjustment
        hour_adjustment = ':00+08:00'
        service = get_calendar_service()

        today = date.today()
        offset = (today.weekday() - (day-1)) % 7 - 7
        next_day = today - timedelta(days=offset)

        # set end time as start time + 1 if no value
        if(e_time == None):
            e_time = datetime.strptime(
                str(next_day)+'T'+s_time, "%Y-%m-%dT%H:%M") + timedelta(hours=1)
            e_time = e_time.strftime("%Y-%m-%dT%H:%M")
        else:
            t1 = datetime.strptime(s_time, "%H:%M")
            t2 = datetime.strptime(e_time, "%H:%M")
            if(t1 >= t2):
                # inc e_time date
                e_time = datetime.strptime(
                    str(next_day)+'T'+e_time, "%Y-%m-%dT%H:%M") + timedelta(days=1)
                e_time = e_time.strftime("%Y-%m-%dT%H:%M")
            else:
                e_time = str(next_day) + 'T' + e_time

        # pprint(e_time)
        until_time = str(next_day.year) + '1231T240000Z'
        # pprint(until_time)

        event_request_body = {
            'start': {
                #date and time
                'dateTime': str(next_day)+'T'+s_time+hour_adjustment,
                'timeZone': 'Asia/Taipei'
            },
            'end': {
                #date and time
                'dateTime': e_time+hour_adjustment,
                'timeZone': 'Asia/Taipei'
            },
            "reminders": {
                "useDefault": False,
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;UNTIL=' + until_time,
            ],
            'summary': event,  # event name
            'colorId': 5,
            'status': 'confirmed',
            'transparency': 'opaque',
            'visibility': 'private',
        }

        sendNotification = False
        sendUpdate = 'none'

        response = service.events().insert(
            calendarId='primary',
            sendNotifications=sendNotification,
            sendUpdates=sendUpdate,
            body=event_request_body
        ).execute()
        if(response):
            text_to_speech('行事歷添加成功')
            print('success')

    def read_calendar(self, day,):
        self.day = day

        service = get_calendar_service()
        # Call the Calendar API
        today = date.today()
        if(self.day == None):
            self.day = str(today)
        else:
            self.day = str(today.year)+'-'+self.day
        print('Get event on'+' '+day)
        events_result = service.events().list(
            calendarId='primary',
            timeMin=self.day+'T00:00:00+08:00',
            timeMax=self.day+'T23:59:59+08:00',
            singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            text_to_speech('您沒有預定行程')
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime')
            end = event['end'].get('dateTime')
            start = start[11:16]+ ' 到 ' + end[11:16]
            text_to_speech((start, event['summary'])
            print(start, event['summary'])

    def read_calendar_next(self):
        service = get_calendar_service()
        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Get next event')
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=1, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            text_to_speech('您沒有預定行程')
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime')
            end = event['end'].get('dateTime')
            start = start[11:16]+ ' 到 ' + end[11:16]
            text_to_speech((start, event['summary'])
            print(start, event['summary'])
