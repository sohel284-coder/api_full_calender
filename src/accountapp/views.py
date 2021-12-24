from django.shortcuts import render
from django.contrib.auth import login

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from knox.models import AuthToken
from .serializers import *

# Register API
class UserRegisterAPIView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        if request.data.get('email') and request.data.get('password'):
            try:
                email = request.data.get('email')
                account = User.objects.get(email=email)
                password = request.data.get('password')
                account_info = {
                    "username": account.username,
                    "password": password,
                }
                serializer = AuthTokenSerializer(data=account_info)

                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data['user']
                login(request, user)
                return super(LoginAPI, self).post(request, format=None)
            except:
                return Response('Given Credential is not valid', status=status.HTTP_401_UNAUTHORIZED)    

        return Response('Email and password fields are required', status=status.HTTP_401_UNAUTHORIZED)    
