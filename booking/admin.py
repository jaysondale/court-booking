from django.contrib import admin
from .models import Booking, Event, Court

# Register your models here.
admin.register(Booking)
admin.register(Event)
admin.register(Court)