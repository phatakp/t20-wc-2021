from django.db import models
from django.db.models.signals import post_save


class MatchManager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        a = super().bulk_create(objs, **kwargs)
        for i in objs:
            post_save.send(i.__class__, instance=i, created=True)
        return a

    def get_queryset(self):
        return super().get_queryset().select_related('team1',
                                                     'team2')


class MatchResultManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('match',
                                                     'winner',
                                                     'match__team1',
                                                     'match__team2')


class BetManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('user',
                                                     'match',
                                                     'bet_team',
                                                     'match__winner',
                                                     'match__match__team1',
                                                     'match__match__team2')
