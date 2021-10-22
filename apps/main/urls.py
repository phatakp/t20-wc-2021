from django.urls import path
from .views import (DashboardView, HomeView,
                    MatchListView,
                    MatchDetailView, RulesView)

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('rules/', RulesView.as_view(), name='rules'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('matches/fixtures/', MatchListView.as_view(), name='match_list'),
    path('match/<slug:slug>/', MatchDetailView.as_view(), name='match_detail'),
]
