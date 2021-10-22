from django.urls import path
from .views import upload_matches

app_name = 'site_admin'

urlpatterns = [
    path('match-upload/', upload_matches, name='matchup'),
]
