from django.urls import path
from . import views

urlpatterns = [
    path('leaderboard/', views.leaderboard_api, name='leaderboard_api'),
    path('submit/', views.submit_score_api, name='submit_score_api'),
]
