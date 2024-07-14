from django.contrib import admin
from django.urls import path
from circlemaker import views
from django.urls import include, path


urlpatterns = [
   path('circle/', views.circle, name='circle'),
   path('line/', views.line, name='line'),
   path('', views.home, name='home'),

]
