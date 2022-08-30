from django.contrib import admin
from .models import Booking, Event, Court

# Register your models here.
admin.site.register(Booking)
admin.site.register(Court)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "firstDay", "lastDay", "startTime", "court", "periods")
    list_filter = ("firstDay", "lastDay", "court")