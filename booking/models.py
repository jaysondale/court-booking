from django.db import models
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL')

# Booking object model
class Booking(models.Model):
	startTime = models.DateTimeField()
	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
	court = models.ForeignKey('Court', on_delete=models.CASCADE)

	# Getter methods
	def get_start_time(self):
		return self.startTime

	def get_user(self):
		return self.user

	def get_court(self):
		return self.court

# Club event model
class Event(Booking):
	periods = models.IntegerField()
	name = models.CharField(max_length=120)

	# Getter methods
	def get_periods(self):
		return self.periods

	def get_name(self):
		return self.name

# Court model
class Court(models.Model):
	name = models.CharField(max_length=120)

	def get_name(self):
		return self.name