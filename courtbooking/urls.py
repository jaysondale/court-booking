from django.contrib import admin
from django.urls import path, include, register_converter
from datetime import datetime
from booking import views as booking_views
from user_manage.views import registrationView, profileView, deleteView, defaultView
from django.conf import settings
from django.conf.urls.static import static

class DateConverter:
    regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'

    def to_python(self, value: str):
        return datetime.strptime(value, '%Y-%m-%d').date()

    def to_url(self, value: datetime.date):
        return value.strftime('%Y-%m-%d')

register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('', defaultView, name='default'),
    path('admin/', admin.site.urls),
    path('calendar/', booking_views.calendarView, name='calendar'),
    path('calendar/<yyyy:current_date>/', booking_views.calendarView, name='calendar'),
    path('calendar/<yyyy:current_date>/<int:booking_error>/', booking_views.calendarView, name='calendar'),
    path('calendar/book', booking_views.book, name='book'),
    path('calendar/my-bookings', booking_views.myBookings, name="my-bookings"),
    path('calendar/delete', booking_views.cancelBooking, name="cancel-booking"),
    path('registration/', registrationView, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', profileView, name='profile'),
    path('account/<int:pk>/delete/', deleteView, name='delete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)