from django.urls import path
from . import views

urlpatterns = [
    path('', views.telegram_bot, name='telegram_bot'),
    path('bale_setwebhook/', views.bale_setwebhook, name='bale_setwebhook'),
]