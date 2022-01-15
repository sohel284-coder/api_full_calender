from django.contrib import admin

from calenderapp.models import *


admin.site.register(CalendarList)
admin.site.register(CalendarEvents)
admin.site.register(CalendarAttendees)


