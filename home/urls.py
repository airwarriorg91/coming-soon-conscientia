from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('events', views.events, name='events'),
    path('continue-registration', views.register2, name='register2'),
]