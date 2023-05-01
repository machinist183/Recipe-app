'''URL Mappings for user api'''

from django.urls import path
from user.views import CreateUserAPIView ,TokenGenerationView , ManageUserApi

app_name='user'

urlpatterns = [
    path('create/' , CreateUserAPIView.as_view() , name='create'),
    path('token/' ,TokenGenerationView.as_view(),name='token'),
    path('me/' ,ManageUserApi.as_view() , name='me' )
]