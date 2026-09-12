from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check, name='api_health_check'),
    path('health/', views.health_check, name='health_check'),
    path('leaderboard/', views.leaderboard_api, name='leaderboard_api'),
    path('submit/', views.submit_score_api, name='submit_score_api'),
]
