from django.urls import path
from calenderapp.views import *




urlpatterns = [
    path('', index, name='index'),

    path('api/events/', Event.as_view(), ),
    path('api/event-filter/<str:query>', CalendarEventListView.as_view(), name='event_filter'),
    path('api/calendars/', CalendarListAPIView.as_view(), ),
    path('api/delete-event/<int:event_id>', EventDelete.as_view(), ),
    path('api/edit-event/<int:event_id>', EventEdit.as_view(), ),
    path('api/cal-color/<str:calendar_name>', CalendarColor.as_view(), ),
    path('api/drag-event-save/', DragEventSave.as_view(), ),
    path('api/add-participant/', AddParticipants.as_view(), )

]


