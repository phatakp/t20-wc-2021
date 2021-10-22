from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from .managers import MatchManager, MatchResultManager, BetManager
from .validators import score_validator

from apps.core.statics import (
    GROUP_CHOICES,
    STATUS_CHOICES,
    WIN_CHOICES,
    MATCH_CHOICES,
    BET_STATUS
)

CustomUser = get_user_model()


# Create your models here.


class Team(models.Model):
    shortname = models.CharField(max_length=4, unique=True)
    longname = models.CharField(max_length=20)
    super12 = models.BooleanField(default=True)
    group = models.CharField(max_length=1,
                             choices=GROUP_CHOICES,
                             blank=True, null=True)

    def __str__(self) -> str:
        return self.shortname


class Standing(models.Model):
    team = models.OneToOneField(Team,
                                related_name="standing",
                                on_delete=models.CASCADE)
    played = models.PositiveSmallIntegerField(default=0)
    won = models.PositiveSmallIntegerField(default=0)
    lost = models.PositiveSmallIntegerField(default=0)
    no_result = models.PositiveSmallIntegerField(default=0)
    points = models.PositiveSmallIntegerField(default=0)
    nrr = models.FloatField(default=0)
    for_rr = models.CharField(max_length=10,
                              validators=[score_validator, ],
                              blank=True, null=True)
    against_rr = models.CharField(max_length=10,
                                  validators=[score_validator, ],
                                  blank=True, null=True)

    class Meta:
        ordering = ('-points', '-nrr')

    def __str__(self) -> str:
        return str(self.team)


class Match(models.Model):
    num = models.PositiveSmallIntegerField()
    date = models.DateTimeField()
    type = models.CharField(max_length=10,
                            choices=MATCH_CHOICES,
                            default='super12')
    slug = models.SlugField(max_length=100, unique=True, null=True)
    team1 = models.ForeignKey(Team,
                              related_name='team1',
                              on_delete=models.CASCADE,
                              blank=True, null=True)
    team2 = models.ForeignKey(Team,
                              related_name='team2',
                              on_delete=models.CASCADE,
                              blank=True, null=True)
    venue = models.CharField(max_length=200)
    min_bet = models.PositiveSmallIntegerField(default=50)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='scheduled',
                              db_index=True)

    objects = MatchManager()

    class Meta:
        verbose_name_plural = 'Matches'
        ordering = ('num',)

    def __str__(self) -> str:
        return self.slug[:-11]

    @property
    def is_scheduled(self):
        return self.status == 'scheduled'

    @property
    def is_completed(self):
        return self.status == 'completed'

    @property
    def is_abandoned(self):
        return self.status == 'abandoned'

    @property
    def entry_cutoff_passed(self):
        return timezone.localtime() >= self.date - timedelta(minutes=30)

    @property
    def is_started(self):
        return timezone.localtime() >= self.date


class MatchResult(models.Model):
    match = models.OneToOneField(Match,
                                 related_name="result",
                                 on_delete=models.CASCADE)
    winner = models.ForeignKey(Team,
                               related_name='winner_teams',
                               on_delete=models.CASCADE,
                               blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, null=True)
    team1_score = models.CharField(max_length=10,
                                   validators=[score_validator, ],
                                   blank=True, null=True)
    team2_score = models.CharField(max_length=10,
                                   validators=[score_validator, ],
                                   blank=True, null=True)
    win_type = models.CharField(max_length=10,
                                choices=WIN_CHOICES,
                                blank=True, null=True)
    win_margin = models.PositiveIntegerField(blank=True, null=True)

    objects = MatchResultManager()

    class Meta:
        ordering = ('match__num',)

    def __str__(self) -> str:
        return str(self.match)

    def get_absolute_url(self):
        return reverse("main:match_detail", kwargs={"slug": self.slug})


class Bet(models.Model):
    match = models.ForeignKey(MatchResult,
                              related_name='match_bets',
                              on_delete=models.CASCADE,
                              blank=True, null=True)
    user = models.ForeignKey(CustomUser,
                             related_name='user_bets',
                             on_delete=models.CASCADE)
    bet_team = models.ForeignKey(Team,
                                 related_name='team_bets',
                                 on_delete=models.CASCADE,
                                 blank=True, null=True)

    bet_amt = models.PositiveSmallIntegerField(default=0)
    win_lose_amt = models.FloatField(default=0)
    status = models.CharField(max_length=10,
                              choices=BET_STATUS,
                              default='placed',
                              db_index=True)
    create_upd_time = models.DateTimeField(auto_now=True)
    updated = models.BooleanField(default=False,
                                  db_index=True)

    objects = BetManager()

    def __str__(self) -> str:
        return str(self.match)

    class Meta:
        unique_together = ('match', 'user')
        ordering = ('match', 'create_upd_time',)
