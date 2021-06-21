from django.shortcuts import render
from django.template.defaulttags import register
from datetime import datetime, timedelta, date, time
from django.utils import timezone
import pytz
from .models import Booking, Court, Event
from django.conf import settings

# Create your views here.
def calendarView(request):
	'''
	Method Objectives:
	1) Gather system parameters - FIRST_BOOKING, LAST_BOOKING
	2) Compute number of time slots available
	3) Iterate over time slots and courts to look for pre-existing bookings OR club events
	4) Map a list of booking states to time slots (e.g., {'9am': [state1, state2, state3...], ...})
	5) Pass dictionary of booking states into context
	'''

	# 1) Gather system parameters
	FIRST_BOOKING = getattr(settings, 'FIRST_BOOKING')
	LAST_BOOKING = getattr(settings, 'LAST_BOOKING')

	# 2) Compute number of time slots available
	timeslots = []
	today = date.today() # TODO: UPDATE SO THIS IS A PARAMETER
	time_cursor_native = datetime.combine(today, FIRST_BOOKING)
	LAST_BOOKING_DATETIME_native = datetime.combine(today, LAST_BOOKING) # convert to datetime for comparison

	# Convert to timezone-sensitive
	timezone = pytz.timezone("America/New_York")

	time_cursor = timezone.localize(time_cursor_native)
	LAST_BOOKING_DATETIME = timezone.localize(LAST_BOOKING_DATETIME_native)

	while(time_cursor <= LAST_BOOKING_DATETIME):
		timeslots.append(time_cursor)
		time_cursor = time_cursor + timedelta(hours=1)

	# 3) Iterate over time slots and courts to look for pre-existing bookings OR club events
	# Initialize dictionary to store states
	booking_states = {}

	# Get today's bookings & events
	today_min_native = datetime.combine(today, time.min)
	today_min = timezone.localize(today_min_native)
	today_max_native = datetime.combine(today, time.max)
	today_max = timezone.localize(today_max_native)

	bookings_today = Booking.objects.filter(startDateTime__gte=today_min, startDateTime__lte=today_max)
	# Filter events ocurring today
	events_today = Event.objects.filter(firstDay__lte=today, lastDay__gte=today, firstDay__week_day=(today.weekday()+2)%7)

	# Get courts
	courts = Court.objects.all()
	# Iterate through time slots, bookings, events
	for court in courts:
		bookings_court = bookings_today.filter(court__id=court.pk)
		events = events_today.filter(court__id=court.pk)
		#print(events)
		booking_states[court] = {}
		for timeslot in timeslots:

			booking = bookings_court.filter(startDateTime=timeslot)

			# Get events that start now or before the timeslot
			events_filtered = events.filter(startTime__lte=timeslot.time())
			# Iterate through events and check number of periods
			event = None # Assuming only one event will fit this criteria
			for event_i in events_filtered:
				endtime = datetime.combine(today, event_i.startTime) + timedelta(hours=event_i.periods)
				if timeslot.time() < endtime.time():
					event = event_i
			#print(event)
			#print(bookings_court.get().startDateTime)
			if event:
				booking_states[court][timeslot] = event
			elif booking:
				booking_states[court][timeslot] = booking.get()



	print(request.user.is_authenticated)
	context = {
		'now': datetime.now(),
		'courts': Court.objects.all(),
		'timeslots': timeslots,
		'title': 'Book a Court',
		'booking_states': booking_states
	}
	return render(request, 'booking/calendar.html', context)
