from django.contrib import admin
from django.urls import include, path
from Tweet import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search')
    
]