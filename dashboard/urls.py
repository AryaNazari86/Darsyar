from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('statistics/', views.statistics, name='statistics'),
    path('charts/', views.charts, name='charts'),
]