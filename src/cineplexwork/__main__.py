"""Command line interface"""

import argparse
from dotenv import load_dotenv
from pytz import timezone, all_timezones
import os
from cineplexwork.cineplex import Cineplex
from cineplexwork.schedule import Schedule
from datetime import datetime, timedelta, time
from time import sleep

parser = argparse.ArgumentParser(
    description="Get employee schedule from Cineplex Workbrain",
    epilog="Created by Jaiden Labelle",
)

parser.add_argument(
    "filename", type=str, help="Name of the file to save the schedule to"
)
parser.add_argument(
    "timezone",
    type=str,
    help="Timezone of the schedule (e.g. America/Toronto)",
    choices=all_timezones,
    metavar="timezone",
)
parser.add_argument(
    "--repeat",
    type=str,
    help="Time to repeat the script every day (e.g. 08:00)",
    metavar="time",
)
args = parser.parse_args()

tz = timezone(args.timezone)

load_dotenv()
username = os.environ["CINEPLEX_USERNAME"]
password = os.environ["CINEPLEX_PASSWORD"]
totp_secret = os.environ["CINEPLEX_TOTP_SECRET"]


# Function to sleep until a specific time (roughly)
def sleepUntil(hour, minute):
    t = datetime.today()
    future = datetime(t.year, t.month, t.day, hour, minute)
    if t.timestamp() > future.timestamp():
        future += timedelta(days=1)
    sleep((future - t).total_seconds())


while True:
    print(f"Getting schedule for {username} in timezone {tz}")

    cineplex = Cineplex()
    calendar = Schedule(tz)

    # Load existing calendar
    # try:
    #     calendar.load(args.filename)
    #     print("Existing calendar loaded")
    # except FileNotFoundError:
    #     print("No existing calendar, creating new one")

    # Login to Workday and Workbrain
    cineplex.login(username, password, totp_secret)

    # Check for shifts between the last 7 days and the next 7 days
    start_date = datetime.now(tz=tz).date() - timedelta(days=7)
    end_date = datetime.now(tz=tz).date() + timedelta(days=7)
    shifts = cineplex.get_shifts(start_date, end_date)

    for shift in shifts:
        calendar.add_shift(shift.start.date(), shift.start.time(), shift.end.time())

    # Output .ics file
    with open(args.filename, "wb") as file:
        file.write(calendar.to_ical())
        print("Calendar written")

    # If desired, repeat every day at the specified time
    if args.repeat:
        repeat_time = time.fromisoformat(args.repeat)
        print(f"Sleeping until {repeat_time}")
        sleepUntil(repeat_time.hour, repeat_time.minute)
    else:
        break
