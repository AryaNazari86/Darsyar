from django.urls import path
from . import views

urlpatterns = [
    path('', views.bot, name='bot'),
    path('bale_setwebhook/', views.bale_setwebhook, name='bale_setwebhook'),
    # path('getpdf/<int:unitid>/exam.pdf', views.get_pdf, name='get_pdf'),
    path('gethtml/<int:unitid>', views.get_html, name='get_html'),
    path('scraper/', views.scraper, name="scraper"),
    path('scrape_hamyar/', views.scrape_hamyar, name="scrape_hamyar"),
    path('send_leaderboard/<int:number>', views.send_leaderboard, name="send_leaderboard"),
]