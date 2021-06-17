from django.template.defaulttags import register
from django import template
import pytz

register = template.Library()

@register.filter
def get_court(dictionary, court):
	return dictionary, court

@register.filter
def get_time(dictionary_court, timeslot):
	dictionary, court = dictionary_court
	print(dictionary[court])
	if timeslot in dictionary[court].keys():
		return str(dictionary[court][timeslot])
	else:
		return "<button class='btn btn-success'>Available</button>"

