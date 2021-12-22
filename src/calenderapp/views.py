from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import serializers, status

from rest_framework  import filters
# from django_filters import rest_framework as filters
from django_filters.rest_framework import  DjangoFilterBackend


from calenderapp.models import *
from calenderapp.serializers import *
from datetime import date, datetime, timedelta


def index(request, ):
    return HttpResponse('test')



class CalenderAPIView(APIView):
    def get(self, request, format=None):
        calenders = Calender.objects.all()
        return Response(CalenderSerializer(calenders, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CalenderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        


class CalenderEventAPIView(APIView):
    def get(self, request, format=None):
        calender_events = CalendarEvent.objects.all()
        print(calender_events)
        return Response(CalenderEevntSerializer(calender_events, many=True).data, status=status.HTTP_200_OK)

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

        

class CalenderWithEventWithAttendeeAPIView(APIView):
    def get(self, request, format=None):
        calenders = Calender.objects.all()
        return Response(CalenderWithEventWithAttendeeSerializer(calenders, many=True).data)

    def post(self, request, format=None):
        serializer = CalenderWithEventWithAttendeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)    
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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


