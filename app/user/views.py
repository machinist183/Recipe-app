from django.shortcuts import render
from user.serializers import  UserSerializer , TokenSerializer
from rest_framework import generics , authentication , permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class TokenGenerationView(ObtainAuthToken):
    serializer_class = TokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class  ManageUserApi(generics.RetrieveUpdateAPIView):

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        '''Retrieve and retrun the user'''
        return self.request.user