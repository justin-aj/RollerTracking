import google

from .views import *
from django.urls import path, include
from google import views as view
from django.contrib.auth import views as auth_views
from .views import home, profile, RegisterView

urlpatterns = [
    path('', view.home, name="home"),
    path('', include('pwa.urls')),
    path('map', view.map, name="map"),
    path('mydata', view.mydata, name="mydata"),
    path('get', view.your_view, name="get"),
    path('check', view.mqtt_check, name='mqtt_check'),
    path('serviceworker.js', view.service_worker),
    path('register/', RegisterView.as_view(), name='google-register'),
    path('profile/', profile, name='google-profile'),
]
