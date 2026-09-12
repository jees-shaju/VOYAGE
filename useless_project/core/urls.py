from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/leaderboard/', views.leaderboard_api, name='leaderboard_api'),
    path('api/submit/', views.submit_score_api, name='submit_score_api'),
]
