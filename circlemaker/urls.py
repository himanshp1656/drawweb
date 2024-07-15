from django.contrib import admin
from django.urls import path
from circlemaker import views
from django.urls import include, path


urlpatterns = [
   path('circle/', views.circle, name='circle'),
   path('line/', views.line, name='line'),
   path('signup/', views.signup_view, name='singup'),
   path('login/', views.login_view, name='login'),
   path('logout/', views.logout_view, name='logout'),
   path('profile/', views.profile, name='profile'),
   path('addcoin/', views.addcoin, name='addcoin'),
   path('', views.home, name='home'),
   path('leaderboard/', views.leaderboard, name='leaderboard'),
   path('resetcountshshshshshhsh/', views.resetcounts, name='resetcounts'),

]
