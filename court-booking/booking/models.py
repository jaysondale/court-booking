from django.db import models
from django.conf import settings
from datetime import datetime

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL')

# Booking object model
class Booking(models.Model):
	startDateTime = models.DateTimeField(null=True)
	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
	court = models.ForeignKey('Court', on_delete=models.CASCADE)

	# Getter methods
	def get_start_time(self):
		return self.startTime

	def get_user(self):
		return self.user

	def get_court(self):
		return self.court

	def __str__(self):
		return self.user.get_full_name()

# Club event model
class Event(models.Model):
	firstDay = models.DateField(null=True)
	lastDay = models.DateField(null=True)
	startTime = models.TimeField(null=True)
	periods = models.IntegerField()
	name = models.CharField(max_length=120)
	court = models.ForeignKey('Court', on_delete=models.CASCADE)


	# Getter methods
	def get_periods(self):
		return self.periods

	def get_name(self):
		return self.name

	def __str__(self):
		return self.get_name()

# Court model
class Court(models.Model):
	name = models.CharField(max_length=120)

	# Boolean field to determine if tennis booking rules apply
	isTennis = models.BooleanField(default=False)

	def __str__(self):
		return self.name