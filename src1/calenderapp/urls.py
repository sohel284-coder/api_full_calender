from django.urls import path
from calenderapp.views import *




urlpatterns = [
    path('', index, name='index'),
    path('api/calenders/', CalenderAPIView.as_view(), name='calender'),
    path('api/calenders/<int:pk>/', SingleCalenderAPIView.as_view(), ),

    path('api/events/', CalenderEventAPIView.as_view(), name='calender'),
    path('api/events/<int:pk>/', SingleCalenderEventAPIView.as_view(), ),


    path('api/attendees/', CalenderAttendeeAPIView.as_view(), name='calender'),
    path('api/attendees/<int:pk>/', SingleCalenderAttendeeAPIView.as_view(), ),

    # path('api/event-create/', CalenderWithEventWithAttendeeAPIView.as_view(), ),
    path('api/create/', CalenderWithEventWithAttendeeAPIView.as_view(), name='create'),

    path('api/event-search/', EventSearch.as_view(), ),
    path('api/today-event/', TodayEvent.as_view(), ),
    path('api/event-filter/', CalenderEventListView.as_view(), name='event_filter'),



]


