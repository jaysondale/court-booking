from django.template.defaulttags import register
from datetime import timedelta, datetime
from django import template
import pytz

register = template.Library()

@register.filter
def get_court(dictionary, court):
	return dictionary, court

@register.filter
def get_time(dictionary_court, timeslot):
	dictionary, court = dictionary_court
	if timeslot in dictionary[court].keys():
		booking = dictionary[court][timeslot]
		col = 'member' if booking.__class__.__name__ == 'Booking' else 'event'
		return f"<button class='btn btn-block {col}'>" + str(booking) + "</button>"
	else:
		timezone = pytz.timezone("America/New_York")
		if (timeslot >= timezone.localize(datetime.now())):
			return f"<button meta='{timeslot.isoformat()}' time='{timeslot.strftime('%a, %b %d %H:%M %p')}' courtname='{court}' court='{court.pk}' class='btn available'>Book</button>"
		else:
			return "<button class='btn btn-outline-secondary'>Unavailable</button>"

@register.filter
def get_next_hour(timeslot):
	return timeslot + timedelta(hours=1)

@register.filter
def get_time_fmt(time):
	timezone = pytz.timezone("America/New_York")
	return timezone.localize(time)