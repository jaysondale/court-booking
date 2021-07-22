from datetime import time, datetime
from .models import Booking, Event
import pytz

def getTodayMinMax(today):
	# Get today's min and max times
	timezone = pytz.timezone("America/New_York")
	today_min_native = datetime.combine(today, time.min)
	today_min = timezone.localize(today_min_native)
	today_max_native = datetime.combine(today, time.max)
	today_max = timezone.localize(today_max_native)
	return (today_min, today_max)

def getBookings(today):
	today_min, today_max = getTodayMinMax(today)
	return Booking.objects.filter(startDateTime__gte=today_min, startDateTime__lte=today_max)

def getEvents(today):
	today_min, today_max = getTodayMinMax(today)
	return Event.objects.filter(firstDay__lte=today, lastDay__gte=today, firstDay__week_day=(today.weekday()+2)%7)