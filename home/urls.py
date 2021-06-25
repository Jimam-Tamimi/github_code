
##1st line sof working code

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index')
]