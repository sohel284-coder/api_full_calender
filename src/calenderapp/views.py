from calendar import calendar
from functools import partial
from itertools import count
from django.http.response import HttpResponse
from django.shortcuts import render
from django.db.models import DurationField, ExpressionWrapper, F, IntegerField, Value, Sum
from django.db.models.functions import Coalesce
from django.utils.timesince import timesince
from django.contrib.auth.decorators import login_required

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework  import filters
# from django_filters import rest_framework as filters
from django_filters.rest_framework import  DjangoFilterBackend


from calenderapp.models import *
from calenderapp.serializers import *
from datetime import date, datetime, timedelta
from django.utils import timezone
import time

def index(request, ):
    return render(request, 'index.html', )



class CalendarEventListView(APIView):

    def calendar_color(self):
        count = 0
        colors = ['red', 'green', '#00FF00', 'blue', '#00FFFF', '#800080', '#FF00FF', '#FFC0CB', '#800000', '#808000']
        calenders = CalendarList.objects.filter().values('id')[0:9]
        calendar_color = {}

        for calendar in calenders:
            calendar_id = calendar['id']
            if not calendar_id in calendar_color.keys():
                # val = str(calendar)
                calendar_color[calendar_id] = colors[count]
                count = count + 1

    
        return calendar_color

        
    def weekly_response(self, data):
        weeks = []
        cal_colors = self.calendar_color()
        
        for dt in data:
            # print(dt)
            
            calendar_name = CalendarList.objects.get(id=dt['calendar_info_id'])
            calendar_attendee = CalendarAttendees.objects.filter(event_info_id=dt['user_event_key']).values('event_attendee')
            values = {
                
            }
            if calendar_name.id in cal_colors:
                values['color'] = cal_colors[calendar_name.id]
                
            values['start'] = dt['event_start_dt']

            values['end'] = dt['event_end_dt']
            values['calendar_name'] = calendar_name.calendar_name
            values['calendar_id'] = calendar_name.id
            values['calendar_attendee'] = calendar_attendee
            values['event_location'] = dt['event_location']
            values['event_description'] = dt['event_description']
            values['event_id'] = dt['id']
            
            values['title'] = dt['event_name']
            s = dt['event_start_dt']
            e = dt['event_end_dt']
            # print(val)
            # d =  datetime.datetime(val)   
            d = s.split('T')
            d = d[0]
            d1= e.split('T')
            d1= d1[0]
            if d1 != d:
                values['allDay'] = True
            else:
                values['allDay'] = False
            values['allday_start_time'] = dt['event_start_dt']
            values['allday_end_time'] = dt['event_end_dt']
               

            # print(datetime.strptime(dt['event_start_dt'], '%Y-%m-%d'))
           
            weeks.append(values)
        return weeks
    def get(self, request, query):
        # query = request.GET.get('q', "")
        today = date.today()
        # print(today)
        weekday = today.weekday()

        start_delta = timedelta(days=weekday)
        print(start_delta, 'delta')
        start_date_week = today - start_delta

        end_date_week = start_date_week + timedelta(days=6)

        # print(datetime.now().month, datetime.now().year)
        current_month = datetime.now().month
        current_year = datetime.now().year
        event = CalendarEvents.objects.filter(event_start_dt=today)
        
        if query == 'daily':
            event = CalendarEvents.objects.filter(event_start_dt=today)
        elif query == 'weekly':
            event = CalendarEvents.objects.filter(event_start_dt__gte=start_date_week) and CalendarEvents.objects.filter(event_start_dt__lte=end_date_week)
            event = CalendarEvents.objects.all()
            events = CalendarEventWithAttendeeSerializer(event, many=True).data

            events = self.weekly_response(events)
            
        elif query == 'monthly':
            event = CalendarEvents.objects.filter(event_start_dt__year=current_year, event_start_dt__month=current_month)
        context = {
            'events':events,
            'start_date_week':start_date_week,
            'end_date_week':end_date_week,
        }
        return Response(context, status=status.HTTP_200_OK)


class CalendarListAPIView(APIView):
    def get(self, request, format=None):
        calendars = CalendarList.objects.all()
        return Response(CalendarListSerializer(calendars, many=True).data, status=status.HTTP_200_OK)


class EventDelete(APIView):
    permission_class = (permissions.AllowAny, )
    
    def delete(self, request, event_id):
        print(event_id)
        event = CalendarEvents.objects.get(id=event_id)
        event.delete()
        # event.save()
        return Response('delete successfully')


class CalendarColor(CalendarEventListView):
    def get(self, request, calendar_name):
        cal_colors = self.calendar_color()
        print(cal_colors)
        calendar_id = CalendarList.objects.get(calendar_name=calendar_name).id
        if calendar_id in cal_colors:
            color_name = cal_colors[calendar_id]
            
            print(color_name, calendar_id)
        return Response(color_name)        



