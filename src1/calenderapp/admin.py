from django.contrib import admin

from calenderapp.models import *


admin.site.register(Calender)
admin.site.register(CalendarEvent)
admin.site.register(CalendarAttendee)


