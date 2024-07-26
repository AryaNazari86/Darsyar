from django.urls import path
from . import views

urlpatterns = [
    path('', views.bot, name='bot'),
    path('bale_setwebhook/', views.bale_setwebhook, name='bale_setwebhook'),
    path('getpdf/<int:unitid>/exam.pdf', views.get_pdf, name='get_pdf'),
    path('scraper/', views.scraper, name="scraper"),
]