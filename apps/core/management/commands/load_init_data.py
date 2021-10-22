from django.core.management.base import BaseCommand
from django.apps import apps
from django.contrib.auth import get_user_model
from apps.accounts.forms import CustomUser
from core.statics import TEAM_CHOICES
from core.views import upload_matches

CustomUser = get_user_model()
Team = apps.get_model('main', 'Team')
Standing = apps.get_model('main', 'Standing')


class Command(BaseCommand):
    help = 'Loads Initial Data to DB'

    def handle(self, *args, **kwargs):
        for user in CustomUser.objects.all():
            user.amount = 0
            user.save()
        self.load_teams()
        upload_matches()

    def load_teams(self):
        Team.objects.all().delete()
        for choices in TEAM_CHOICES:
            team = Team.objects.create(**choices)
            if choices['super12']:
                Standing.objects.create(team=team)
        print('Team details saved')
