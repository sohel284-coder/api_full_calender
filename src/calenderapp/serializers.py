from django.db.models import fields
from rest_framework import serializers

from calenderapp.models import *


class CalendarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarList
        fields = '__all__'


class CalendarEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvents
        fields = '__all__'

class CalendarAttendeesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CalendarAttendees
        fields = '__all__'

   

    


class CalendarEventWithAttendeeSerializer(serializers.ModelSerializer):
    event_attendee = CalendarAttendeesSerializer(many=True)

    class Meta:
        model = CalendarEvents
        fields = '__all__'


class CalenderWithEventWithAttendeeSerializer(serializers.ModelSerializer):
    calender_event = CalendarEventsSerializer(many=True, )
    calender_attendee = CalendarAttendeesSerializer(many=True, )
    class Meta:
        model = CalendarList
        fields = ('id', 'calender_name', 'user', 'select_fig', 'calender_event', 'calender_attendee', )

    






