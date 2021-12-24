from django.http.response import HttpResponse
from django.shortcuts import render
from django.db.models import DurationField, ExpressionWrapper, F, IntegerField, Value, Sum
from django.db.models.functions import Coalesce
from django.utils.timesince import timesince
from django.contrib.auth.decorators import login_required

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
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
    return HttpResponse('test')



class CalenderAPIView(APIView):
    
    def get(self, request, format=None):
        # user_id = request.user.id
        attendee = CalendarAttendee.objects.filter(event_email=request.user.email).values('calender_info')
        calenders = Calender.objects.filter(id__in=attendee)
        if calenders:
            return Response(CalenderWithEventWithAttendeeSerializer(calenders, many=True).data, status=status.HTTP_200_OK)
        return Response('data not found', status=status.HTTP_404_NOT_FOUND) 

    def post(self, request, format=None):
        request.data['user'] = request.user.id
        print(request.data)
        serializer = CalenderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingleCalenderAPIView(APIView):
    def get(self, request, pk):
        try:
            calender = Calender.objects.get(id=pk)
            return Response(CalenderWithEventWithAttendeeSerializer(calender).data, status=status.HTTP_200_OK)
        except:
            return Response('data not found', status=status.HTTP_404_NOT_FOUND) 

    def put(self, request, pk):
        try:
            calender = Calender.objects.get(id=pk)
            if calender.user.id == request.user.id:
                serializer = CalenderSerializer(calender, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response('User not allow', status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response('data not found', status=status.HTTP_404_NOT_FOUND) 


    def delete(self, request, pk):
        try:
            calender = Calender.objects.get(id=pk)
            if calender.user.id == request.user.id:
                calender.delete()
                return Response('calender deleted', status=status.HTTP_200_OK)
            return Response('User not allow', status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response('data not found', status=status.HTTP_404_NOT_FOUND) 



class SingleCalenderEventAPIView(APIView):
    def get(self, request, pk):
        try:
            calender_event = CalendarEvent.objects.get(id=pk)
            return Response(CalenderEevntSerializer(calender_event).data, status=status.HTTP_200_OK)
        except:
            return Response('data not found', status=status.HTTP_404_NOT_FOUND) 
                

    def put(self, request, pk):
        try:
            calender_event = CalendarEvent.objects.get(id=pk)
            calender= Calender.objects.get(id=calender_event.calender_info.id)
        
            if calender.user.id == 2:
                serializer = CalenderEevntSerializer(calender_event, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response('User not allow', status=status.HTTP_401_UNAUTHORIZED)

        except:
            return Response('data not found', status=status.HTTP_404_NOT_FOUND) 

    def delete(self, request, pk):
        try:
            calender_event = CalendarEvent.objects.get(id=pk)
            print(calender_event)
            print(calender_event.calender_info)
            calender = Calender.objects.get(id=calender_event.calender_info.id)

            if calender.user.id == 2:
                calender_event.delete()
                return Response('calender deleted', status=status.HTTP_200_OK)
            return Response('User not allow', status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response('data not found', status=status.HTTP_404_NOT_FOUND) 


class SingleCalenderAttendeeAPIView(APIView):
    def get(self, request, pk):
        try:
            calender_attendee = CalendarAttendee.objects.get(id=pk)
            return Response(CalendarAttendeeSerializer(calender_attendee).data, status=status.HTTP_200_OK)
        except:
            return Response('data not found', status=status.HTTP_404_NOT_FOUND) 
            
    def put(self, request, pk):
        try:
            calender_attendee = CalendarAttendee.objects.get(id=pk)
            calender_attendee_email = calender_attendee.event_email
            print(calender_attendee_email)
            if calender_attendee_email == 'rana123@gmail.com':
                serializer = CalendarAttendeeSerializer(calender_attendee, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response('User not allow', status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response('data not found', status=status.HTTP_404_NOT_FOUND) 

    def delete(self, request, pk):
        try:
            calender_attendee = CalendarAttendee.objects.get(id=pk)
            print(calender_attendee)
            calender = Calender.objects.get(id=calender_attendee.calender_info.id)

            if calender.user.id == 3:
                calender_attendee.delete()
                return Response('Calender Attendee deleted', status=status.HTTP_200_OK)
            return Response('User not allow', status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response('data not found', status=status.HTTP_404_NOT_FOUND) 


        
        


class CalenderEventAPIView(APIView):
    def get(self, request, format=None):
        calender_events = CalendarEvent.objects.all()
        if calender_events:
            return Response(CalenderEevntSerializer(calender_events, many=True).data, status=status.HTTP_200_OK)
        return Response('data not found', status=status.HTTP_404_NOT_FOUND) 

    def post(self, request, format=None):
        serializer = CalenderEevntSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class CalenderAttendeeAPIView(APIView):
    def get(self, request, format=None):
        calenders = CalendarAttendee.objects.all()
        return Response(CalendarAttendeeSerializer(calenders, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        event_id = request.data['event_info']
        calender_id = request.data['calender_info']
        if event_id != calender_id:
            return Response('Calender and Event shoud be same', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = CalendarAttendeeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

# class CalenderWithEventWithAttendeeAPIView(APIView):
#     def get(self, request, format=None):
#         calenders = Calender.objects.all()
#         return Response(CalenderWithEventWithAttendeeSerializer(calenders, many=True).data)

#     def post(self, request, format=None):
#         serializer = CalenderWithEventWithAttendeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         print(serializer.errors)    
#         return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CalenderEventListView(APIView):
    def get(self, request, format=None):
        query = request.GET.get('q', "")
        today = date.today()
        weekday = today.weekday()
        start_delta = timedelta(days=weekday)
        start_date_week = today - start_delta
        end_date_week = start_date_week + timedelta(days=6)

        print(datetime.now().month, datetime.now().year)
        current_month = datetime.now().month
        current_year = datetime.now().year
        event = CalendarEvent.objects.filter(event_start_date=today)
        
        print(today)
        if query == 'daily':
            event = CalendarEvent.objects.filter(event_start_date=today)
        elif query == 'weekly':
            event = CalendarEvent.objects.filter(event_start_date__gte=start_date_week) and CalendarEvent.objects.filter(event_start_date__lte=end_date_week)

        elif query == 'monthly':
            event = CalendarEvent.objects.filter(event_start_date__year=current_year, event_start_date__month=current_month)
            print(event)
        return Response(CalendarEventWithAttendeeSerializer(event, many=True).data, status=status.HTTP_200_OK)

class EventSearch(APIView):
    def get(self, request, format=None):
        query = request.GET.get('q', "")
        attendee = CalendarAttendee.objects.filter(event_email='rana@gmail.com')

        # events = CalendarEvent.objects.filter(id__in=attendee, event_name__icontains=query, event_description__icontains=query)
        events = CalendarEvent.objects.filter(event_name__icontains=query, id__in=attendee) or CalendarEvent.objects.filter(event_description__icontains=query ,id__in=attendee)
    
        return Response(CalenderEevntSerializer(events, many=True).data, status=status.HTTP_200_OK)
       

        
class TodayEvent(APIView):
    def get(self, request, format=None):
        start_time = str(date.today())
        start_time += " " + "00:00:00.000000"
        print(start_time)
        end_time = str(date.today()) + " " + "23:59:59.000000"
        print(end_time)
        attendee = CalendarAttendee.objects.filter(event_email='rana@gmail.com')
        events = CalendarEvent.objects.filter(event_start_date__gte=start_time, id__in=attendee)
        events = events.filter(event_end_date__lte=end_time)


        print(events)
        new_time = timedelta(hours=0)
        data = CalenderEevntSerializer(events, many=True).data
        dict = {
            'free_time':''
        }
        for event in events:
            total_time = event.event_end_date - event.event_start_date
            new_time = total_time + new_time
        print(new_time)
        dict['free_time'] = timedelta(hours=24) - new_time
        
        data.append(dict)
         
        return Response(data, status=status.HTTP_200_OK)
       

              



class CalenderWithEventWithAttendeeAPIView(APIView):
    def post(self, request, format=None):
        calender_serializer = CalenderSerializer(data=request.data)
        if calender_serializer.is_valid():
            calender = calender_serializer.save()
            event = request.data['event_info']
            event['calender_info'] = calender.id
            event_serializer = CalenderEevntSerializer(data=event)
            if event_serializer.is_valid():
                calender_event = event_serializer.save()
                attendee = request.data['attendee_info']

                ###inserting owner when no attendee
                if(len(attendee) == 0):
                    attendee.append({})

                    attendee[0]['calender_info'] = calender.id
                    attendee[0]['event_info'] = calender_event.id
                    attendee[0]['event_email'] = "rana@gmail.com" ### todo
                    attendee[0]['self_flg'] = 1

                else:
                    for single_attendee in attendee:
                        single_attendee['calender_info'] = calender.id
                        single_attendee['event_info'] = calender_event.id
                        # if single_attendee['event_email'] == request.user.email:
                        # single_attendee.self_flg = 1
                        
                    ###inserting owner at the end of the attendee 
                    get_len = len(attendee)
                    attendee.append({})
                    attendee[get_len]['calender_info'] = calender.id
                    attendee[get_len]['event_info'] = calender_event.id
                    attendee[get_len]['event_email'] = 'rana@gmail.com' #### todo
                    attendee[get_len]['self_flg'] = 1

                attendee_serializer = CalendarAttendeeSerializer(data=attendee, many=True)
                if attendee_serializer.is_valid():
                    calender_attendee = attendee_serializer.save()

                    get_all_data = CalenderWithEventWithAttendeeSerializer(Calender.objects.get(id=calender.id))
                    # return Response(attendee_serializer.data, status=status.HTTP_201_CREATED)
                    return Response(get_all_data.data, status=status.HTTP_201_CREATED)

                return Response(attendee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

                # return Response(event_serializer.data, status=status.HTTP_201_CREATED)
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # return Response(calender_serializer.data, status=status.HTTP_201_CREATED)

            # return Response(calender_serializer.data, status=status.HTTP_201_CREATED)
        return Response(calender_serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
