from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.http import JsonResponse
from datetime import datetime, timedelta, date, time
from django.utils import timezone
import pytz
from .models import Booking, Court, Event
from django.conf import settings
from .utils import getBookings, getEvents
from django.db.models import Q

# Create your views here.
def calendarView(request, current_date=None, booking_error=0):
	print(request)
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
	NUM_BOOKING_DAYS = getattr(settings, 'NUM_BOOKING_DAYS')

	# 2) Compute number of time slots available
	timeslots = []
	today = date.today()
	# Date validation
	last_day = date.today() + timedelta(days=NUM_BOOKING_DAYS - 1)
	if current_date:
		if (current_date > last_day):
			return redirect('calendar', last_day)
		elif (current_date < date.today()):
			return redirect('calendar', date.today())
		else:
			today = current_date
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

	bookings_today = getBookings(today)
	events_today = getEvents(today)

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


	# Dates for date navigation
	start = date.today()
	datebtns = [start]
	for di in range(1, NUM_BOOKING_DAYS):
		datebtns.append(start + timedelta(days=di))

	context = {
		'courts': Court.objects.all(),
		'timeslots': timeslots,
		'page_title': 'Book a Court',
		'booking_states': booking_states,
		'current': today,
		'datebtns': datebtns,
		'current_is_today': today == date.today(),
		'booking_error': booking_error == 1
	}
	return render(request, 'booking/calendar.html', context)

def book(request):
	if (request.method == "POST"):
		# Deserialize time
		time = datetime.fromisoformat(request.POST['time'])
		court = request.POST['court']
		court_obj = Court.objects.get(id=court)
		booking_approved = False
		if(request.user.is_authenticated):
			# Validate booking rules met
			# Check if pickleball-only court has been booked today
			user_bookings = getBookings(time.date())
			pb_bookings_filtered = user_bookings.filter(user=request.user, court__isTennis=False)
			if not pb_bookings_filtered:
				t_bookings = user_bookings.filter(court__isTennis=True)
				if not court_obj.isTennis:
					if not t_bookings:
						booking_approved = True
				else:
					t_bookings_filtered = t_bookings.filter(~Q(startDateTime=time))
					if not t_bookings_filtered:
						booking_approved = True
			if (booking_approved):
				newBooking = Booking(user=request.user, startDateTime=time, court=court_obj)
				newBooking.save()
	booking_error = 0 if booking_approved else 1
	return JsonResponse({'url': '/calendar/' + datetime.strftime(time.date(),'%Y-%m-%d') + '/' + str(booking_error) + '/'})

def myBookings(request):
	# Get bookings that are either now or in the future
	now_native = datetime.now()
	# Convert to timezone-sensitive
	timezone = pytz.timezone("UTC")
	now = timezone.localize(now_native)
	bookings = Booking.objects.filter(user=request.user, startDateTime__gte=now)
	context = {
		'bookings': bookings,
		'title': 'My Bookings',
		'cancel_action': '/calendar/delete'
	}
	return render(request, 'booking/my_bookings.html', context)

def cancelBooking(request):
	if (request.method == "POST"):
		bid = request.POST['bid']
		booking = Booking.objects.get(id=bid)
		if (booking.user == request.user):
			booking.delete()
			return JsonResponse({'code': 200})
	return JsonResponse({'code': 400})