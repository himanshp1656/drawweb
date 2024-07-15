from django.contrib import admin

# Register your models here.
from .models import UserProfile,prize
from django.contrib import admin
from django.urls import path
admin.site.register(UserProfile)
admin.site.register(prize)
