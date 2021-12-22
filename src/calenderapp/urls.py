from django.urls import path
from calenderapp.views import *




urlpatterns = [
    path('', index, name='index'),
    path('api/calenders/', CalenderAPIView.as_view(), name='calender'),
    path('api/calender-events/', CalenderEventAPIView.as_view(), name='calender'),
    path('api/calender-attendee/', CalenderAttendeeAPIView.as_view(), name='calender'),
    path('api/event-create/', CalenderWithEventWithAttendeeAPIView.as_view(), ),
    path('api/event-filter/', CalenderEventListView.as_view(), name='event_filter'),

]


