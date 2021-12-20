from django.urls import path
from calenderapp.views import *




urlpatterns = [
    path('', index, name='index'),
]


