from django.template.defaulttags import register
from datetime import timedelta
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
		return "<button class='btn available'>Book</button>"

@register.filter
def get_next_hour(timeslot):
	return timeslot + timedelta(hours=1)