import icalendar
import uuid
import datetime

class ShiftCalendar:
    def __init__(self, tz) -> None:
        self.calendar = icalendar.Calendar()
        self.tz = tz

        # Product Identifier https://www.kanzaki.com/docs/ical/prodid.html
        self.calendar.add("PRODID", "Algonquin timetable to .ics")
        self.calendar.add("VERSION", "2.0") # iCalendar spec version

    def add_shift(self, date: datetime.date, start_time: datetime.time, end_time: datetime.time):
        """Add shift to calendar"""
        
        # Create calendar date info
        dtstart = datetime.datetime.combine(date, start_time, tzinfo=self.tz)
        dtend = datetime.datetime.combine(date, end_time, tzinfo=self.tz)
        dtstamp = datetime.datetime.now(tz=self.tz)

        # Create iCalendar event
        event = icalendar.Event()
        event.add('SUMMARY', "Cineplex Shift")
        event.add('DTSTART', dtstart)
        event.add('DTEND', dtend)
        event.add('DTSTAMP', dtstamp)
        event.add('UID', uuid.uuid4())

        # Add event to calendar
        self.calendar.add_component(event)

    def to_ical(self):
        return self.calendar.to_ical()