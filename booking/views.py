from django.shortcuts import render

# Create your views here.
def calendarView(request):
	context = {}
	return render(request, 'booking/calendar.html', context)
