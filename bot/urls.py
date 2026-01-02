from django.urls import path
from . import views

urlpatterns = [
    path('', views.bot, name='bot'),
    path('setwebhook/', views.setwebhook, name='setwebhook'),
    # path('getpdf/<int:unitid>/exam.pdf', views.get_pdf, name='get_pdf'),
    path('gethtml/<int:unit_id>', views.get_html, name='get_html'),
    path('scraper/', views.scraper, name="scraper"),
    path('scrape_hamyar/', views.scrape_hamyar, name="scrape_hamyar"),
    path('send_leaderboard/<int:number>', views.send_leaderboard, name="send_leaderboard"),
    path("total_users/", views.total_users_json, name="total_users_json"),
    path('plot_logs_by_hour/', views.plot_logs_by_hour, name="plot_logs_by_hour"),
]