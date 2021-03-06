# Generated by Django 3.2.10 on 2021-12-20 17:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Calender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calender_name', models.CharField(max_length=250)),
                ('select_fig', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CalendarEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=263)),
                ('event_description', models.TextField()),
                ('event_start_date', models.DateField()),
                ('event_end_date', models.DateField()),
                ('event_location', models.TextField()),
                ('inperson_flg', models.IntegerField(blank=True, default=0, null=True)),
                ('travel_flg', models.IntegerField(blank=True, default=0, null=True)),
                ('zoom_flg', models.IntegerField(blank=True, default=0, null=True)),
                ('msteams_flg', models.IntegerField(blank=True, default=0, null=True)),
                ('gmeet_flg', models.IntegerField(blank=True, default=0, null=True)),
                ('lunch_flg', models.IntegerField(blank=True, default=0, null=True)),
                ('dinner_flg', models.IntegerField(blank=True, default=0, null=True)),
                ('oneonone_flg', models.IntegerField(blank=True, default=0, null=True)),
                ('all_day_flg', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('calender_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calenderapp.calender')),
            ],
        ),
        migrations.CreateModel(
            name='CalendarAttendee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_attendee', models.TextField(blank=True, null=True)),
                ('event_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('response_status', models.CharField(blank=True, max_length=50, null=True)),
                ('self_flg', models.IntegerField(blank=True, null=True)),
                ('calender_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calenderapp.calender')),
                ('event_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calenderapp.calendarevent')),
            ],
        ),
    ]
