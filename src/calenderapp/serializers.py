from django.db.models import fields
from rest_framework import serializers

from calenderapp.models import *


class CalenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calender
        fields = '__all__'


class CalenderEevntSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = '__all__'

class CalendarAttendeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CalendarAttendee
        fields = '__all__'

   

    


class CalendarEventWithAttendeeSerializer(serializers.ModelSerializer):
    event_attendee = CalendarAttendeeSerializer(many=True)

    class Meta:
        model = CalendarEvent
        # fields = ('id', 'event_name', 'event_attendee', )
        exclude = ('id', )


class CalenderWithEventWithAttendeeSerializer(serializers.ModelSerializer):
    calender_event = CalenderEevntSerializer(many=True, )
    calender_attendee = CalendarAttendeeSerializer(many=True, )
    class Meta:
        model = Calender
        fields = ('id', 'calender_name', 'user', 'select_fig', 'calender_event', 'calender_attendee', )

    






