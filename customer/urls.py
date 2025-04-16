from django.urls import path 
from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register('search', views.SearchAPI, basename='search')

urlpatterns = [
    path('search/', views.SearchAPI.as_view(), name='search')
]