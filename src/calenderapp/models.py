from django.db import models
from django.contrib.auth.models import User


class CalendarList(models.Model):
    calendar_id = models.CharField(max_length=250, null=True, blank=True, )
    username = models.CharField(max_length=50, null=True, blank=True, )
    calendar_name = models.CharField(max_length=250, )
    access_role = models.CharField(max_length=50, null=True, blank=True, )
    select_flg = models.IntegerField(null=True, blank=True, default=0, )


    def __str__(self):
        return self.calendar_name


class CalendarEvents(models.Model):
    user_event_key = models.CharField(max_length=250, null=True, blank=True, unique=True, )
    event_id = models.CharField(max_length=250, null=True, blank=True, )

    calendar_info_id = models.ForeignKey(CalendarList, on_delete=models.CASCADE, related_name='calender_event')
    event_name = models.CharField(max_length=263, )
    event_name_prev = models.CharField(max_length=250, null=True, blank=True, )
    event_description = models.TextField(null=True, blank=True, )
    event_start_dt = models.DateTimeField()
    event_end_dt = models.DateTimeField()
    event_location = models.TextField(null=True, blank=True, )
    allDay = models.BooleanField(default=False, blank=True, null=True, )
    
    delete_flg = models.IntegerField(null=True, blank=True, default=0)
    new_flg = models.IntegerField(null=True, blank=True, default=0)
    location_missing_flg = models.IntegerField(null=True, blank=True, default=0)

    inperson_flg = models.IntegerField(null=True, blank=True, default=0)
    travel_flg = models.IntegerField(null=True, blank=True, default=0)
    zoom_flg = models.IntegerField(null=True, blank=True, default=0)
    msteams_flg = models.IntegerField(null=True, blank=True, default=0)
    gmeet_flg = models.IntegerField(null=True, blank=True, default=0)
    lunch_flg = models.IntegerField(null=True, blank=True, default=0)
    dinner_flg = models.IntegerField(null=True, blank=True, default=0)
    oneonone_flg = models.IntegerField(null=True, blank=True, default=0)
    all_day_flg = models.IntegerField(null=True, blank=True, default=0)
    event_link = models.URLField(null=True, blank=True, )
    event_call_link = models.URLField(null=True, blank=True, )
    num_attendees = models.IntegerField(null=True, blank=True, )
    organizer_flg = models.IntegerField(null=True, blank=True, default=0)
    creator_flg = models.IntegerField(null=True, blank=True, default=0)
    
     # Not auto-add since we want to captur


    def __str__(self):
        return self.event_name

class CalendarAttendees(models.Model):
    event_info_id = models.ForeignKey(CalendarEvents, on_delete=models.CASCADE, related_name='event_attendee', to_field="user_event_key", null=True, blank=True, )
    calendar_info_id = models.ForeignKey(CalendarList, on_delete=models.CASCADE, related_name='calender_attendee')
    event_attendee = models.CharField(max_length=200, null=True, blank=True, )
    event_attendee_email = models.EmailField(null=True, blank=True, )

    response_status = models.CharField(max_length=50, null=True, blank=True)
    self_flg = models.IntegerField(null=True, blank=True, )

   

    def __str__(self):
        return self.event_info_id.event_name



    
        







