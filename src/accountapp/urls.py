from django.urls import path
from knox import views as knox_views
from accountapp.views import *


urlpatterns = [
    path('api/user-register/', UserRegisterAPIView.as_view(), name='user_register'),
    path('api/user-login/', LoginAPI.as_view(), name='login'),
    path('api/user-logout/', knox_views.LogoutView.as_view(), name='logout'),
]