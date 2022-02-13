import atexit
from calendar import calendar
from functools import partial
from itertools import count
from pickle import TRUE
from unicodedata import name
from urllib import request
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
            
            calendar_name = CalendarList.objects.get(id=dt['calendar_info_id'])
            calendar_attendee = CalendarAttendees.objects.filter(event_info_id=dt['user_event_key']).values('event_attendee_email')
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
           
            # d =  datetime.datetime(val)   
            d = s.split('T')
            d = d[0]
            d1= e.split('T')
            d1= d1[0]
            if dt['all_day_flg'] == 1:
                values['allDay'] = True
            else:
                values['allDay'] = False
            
            # values['allDay'] = dt['allDay']
            values['allday_start_time'] = dt['event_start_dt']
            values['allday_end_time'] = dt['event_end_dt']
               

           
            weeks.append(values)
        return weeks
    def get(self, request, query):
        # query = request.GET.get('q', "")
        today = date.today()
        weekday = today.weekday()

        start_delta = timedelta(days=weekday)
        start_date_week = today - start_delta

        end_date_week = start_date_week + timedelta(days=6)

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


class CalendarListAPIView(CalendarEventListView):
    def get(self, request, format=None):
        calendars = CalendarList.objects.all()
        cal_colors = self.calendar_color()
        print(cal_colors)
        serializers = CalendarListSerializer(calendars, many=True).data
        for serializer in serializers:
            calendar_id = serializer['id']
            if calendar_id in cal_colors.keys():
                get_color = cal_colors[calendar_id]
                print(get_color, calendar_id) 
                serializer['calendar_color'] = get_color
                print(serializer)
        return Response(serializers, status=status.HTTP_200_OK)

class Event(APIView):
    def get(self, request, format=None):
        events = CalendarEvents.objects.all()
        serializer = CalendarEventWithAttendeeSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventDelete(APIView):
    permission_class = (permissions.AllowAny, )
    
    def delete(self, request, event_id):
        event = CalendarEvents.objects.get(id=event_id)
        event.delete()
        # event.save()
        return Response('delete successfully')


class EventEdit(APIView):
    permission_class = (permissions.AllowAny, )

    def save_attendees(self, attendees, calendar_info_id, event):
        print(attendees, 'tte')
        print(event, 'before loop')
        print(calendar_info_id)
        success_attendees = []
        for attendee in attendees:
            try:
                print('try')
                get_event = CalendarEvents.objects.get(id=event).user_event_key
                print(get_event)
                get_attendee = CalendarAttendees.objects.get(event_info_id=event, event_attendee_email=attendee)
                pass
            except:
                print('except')
                attendee_data = {}
                print(event)
                get_event = CalendarEvents.objects.get(id=event).user_event_key
                print(get_event)
                attendee_data['calendar_info_id'] = calendar_info_id
                attendee_data['event_info_id'] = get_event
                attendee_data['event_attendee_email'] = attendee
                print(attendee_data)
                serializer = CalendarAttendeesSerializer(data=attendee_data, partial=True)
                print(serializer)
                if serializer.is_valid(raise_exception=True):

                    serializer.save()
                    print('save')
                    success_attendees.append(attendee)
                else:
                    print(serializer.errors)    
                    
        events = CalendarEvents.objects.get(id=event)
        serializer = CalendarEventWithAttendeeSerializer(events, many=True).data          
        return Response(serializer, status=status.HTTP_200_OK)
    
    def put(self, request, event_id):
        
        
        try:
            calendar_info_id = CalendarList.objects.get(calendar_name=request.data['calendar_info_id']).id
            request.data['calendar_info_id'] = calendar_info_id
        except:
            event = CalendarEvents.objects.get(id=event_id)
            calendar_info_id = CalendarList.objects.get(calendar_name=event.calendar_info_id)
            request.data['calendar_info_id'] = calendar_info_id.id

        event = CalendarEvents.objects.get(id=event_id)
        serializer = CalendarEventsSerializer(event, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            try:
                attendees = request.data['attendees']
                print(event_id, 'before function')
                self.save_attendees(attendees, calendar_info_id, event_id)
            except:
                pass    
            return Response('edit successfully', status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CalendarColor(CalendarEventListView):
    def get(self, request, calendar_name):
        cal_colors = self.calendar_color()
        calendar_id = CalendarList.objects.get(calendar_name=calendar_name).id
        if calendar_id in cal_colors:
            color_name = cal_colors[calendar_id]
            
        return Response(color_name)        

class DragEventSave(APIView):
    def post(self, request, format=None):
        event_name = request.data['event_name']
        event_name = event_name.replace(' ', '_')
        last_event_id = CalendarEvents.objects.last().id
        request.data['user_event_key'] = event_name + '_' + str(last_event_id + 1)
        print(request.data['user_event_key'])

        try:
            print('try')
            attendess = request.data['attendees']
            print(attendess)
            has_attendee = True
            
        except:
            print('except')
            has_attendee = False

        calendar_info_id = CalendarList.objects.get(calendar_name=request.data['calendar_info_id']).id
        request.data['calendar_info_id'] = calendar_info_id
        if request.data['all_day_flg'] == True:
           request.data['all_day_flg'] = 1
        else:
            request.data['all_day_flg'] = 0  

        serializer = CalendarEventsSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            try:
                print('try')
                print(has_attendee)
                if (has_attendee):
                    for attendee in attendess:
                        print(attendee)
                        attendee_data = {}
                        
                        print(request.data['user_event_key'])
                        print(calendar_info_id)
                        attendee_data['calendar_info_id'] = calendar_info_id
                        print(attendee_data['calendar_info_id'])
                        attendee_data['event_info_id'] = request.data['user_event_key']
                        print(attendee_data['event_info_id'])
                        attendee_data['event_attendee_email'] = attendee
                        print(attendee_data['event_attendee_email'])
                        print(attendee_data)
                        serializer = CalendarAttendeesSerializer(data=attendee_data)
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                            print('save')
                        else:
                            print(serializer.errors)    
            except Exception as e:
                print(e)
            return Response('Successfully eventb save', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class AddParticipants(APIView):
    permission_class = (permissions.AllowAny, )
    
    def post(self, request):
        new_attendee = request.data['attendee']
        event = request.data['event']
        is_attendee = False
        try:
            event_info_id = CalendarEvents.objects.get(id=event).user_event_key
            print(event_info_id)
            has_attendees = CalendarAttendees.objects.filter(event_info_id=event_info_id).values('event_attendee_email')
            print(list(has_attendees))
            attendee_emails = list(has_attendees)
            for email in attendee_emails:
                if email['event_attendee_email'] == new_attendee:
                    is_attendee = True
        except:
            pass
          

        return Response(is_attendee)                        
                        
       

