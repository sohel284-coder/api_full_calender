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
    # calender_attendee = CalendarAttendeeSerializer(many=True, )
    class Meta:
        model = Calender
        fields = ('calender_event', 'id', )

    def create(self, validated_data):
        event_info = validated_data.pop('calender_event')
        # attendee_info = validated_data.pop('calender_attendee')
        calender = Calender.objects.create(**validated_data)

        event = CalendarEvent.objects.create(**event_info, calender_info=calender)
        return calender







