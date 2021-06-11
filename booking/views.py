from django.shortcuts import render
from datetime import datetime, timedelta, date, time
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
	today = date.today()
	time_cursor = datetime.combine(today, FIRST_BOOKING)
	LAST_BOOKING_DATETIME = datetime.combine(today, LAST_BOOKING) # convert to datetime for comparison
	while(time_cursor <= LAST_BOOKING_DATETIME):
		timeslots.append(time_cursor)
		time_cursor = time_cursor + timedelta(hours=1)

	# 3) Iterate over time slots and courts to look for pre-existing bookings OR club events
	# Initialize dictionary to store states
	booking_states = {}

	# Get today's bookings & events
	today_min = datetime.combine(today, time.min)
	today_max = datetime.combine(today, time.max)
	bookings_today = Booking.objects.filter(startDateTime__gte=today_min, startDateTime__lte=today_max)
	events_today = Event.objects.filter(firstDay__lte=today, lastDay__gte=today)

	# Get courts
	courts = Court.objects.all()

	# Iterate through time slots, bookings, events
	for court in courts:
		bookings_court = bookings_today.filter(court__pk=court.pk)
		events = events_today.filter(court__pk=court.pk)
		for timeslot in timeslots:
			bookings = bookings_court.filter(startDateTime__e=timeslot)




	context = {
		'now': datetime.now(),
		'courts': Court.objects.all()
	}
	return render(request, 'booking/calendar.html', context)
