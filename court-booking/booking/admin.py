from django.contrib import admin
from .models import Booking, Event, Court

# Register your models here.
admin.site.register(Booking)
admin.site.register(Event)
admin.site.register(Court)