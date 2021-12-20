from django.db import models
from django.contrib.auth.models import User


class Calender(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    calender_name = models.CharField(max_length=250, )
    select_fig = models.BooleanField(default=False, )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return self.calender_name


class CalendarEvent(models.Model):

    calender_info = models.ForeignKey(Calender, on_delete=models.CASCADE, )
    event_name = models.CharField(max_length=263, )
    event_description = models.TextField()
    event_start_date = models.DateField()
    event_end_date = models.DateField()
    event_location = models.TextField()

    inperson_flg = models.IntegerField(null=True, blank=True, default=0)
    travel_flg = models.IntegerField(null=True, blank=True, default=0)
    zoom_flg = models.IntegerField(null=True, blank=True, default=0)
    msteams_flg = models.IntegerField(null=True, blank=True, default=0)
    gmeet_flg = models.IntegerField(null=True, blank=True, default=0)
    lunch_flg = models.IntegerField(null=True, blank=True, default=0)
    dinner_flg = models.IntegerField(null=True, blank=True, default=0)
    oneonone_flg = models.IntegerField(null=True, blank=True, default=0)
    all_day_flg = models.IntegerField(null=True, blank=True, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, )  # Not auto-add since we want to captur


    def __str__(self):
        return self.event_name


class CalendarAttendee(models.Model):
    event_info = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE, )
    calender_info = models.ForeignKey(Calender, on_delete=models.CASCADE, )
    event_attendee = models.TextField(null=True, blank=True, )
    event_email = models.EmailField(null=True, blank=True, )
    response_status = models.CharField(max_length=50, null=True, blank=True)
    self_flg = models.IntegerField(null=True, blank=True, )

    def __str__(self):
        return self.event_info.event_name



    
        







