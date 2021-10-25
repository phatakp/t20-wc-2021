from django.contrib import admin

from .models import Team, Standing, Match, MatchResult, Bet

# Register your models here.


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('shortname', 'longname', 'super12', 'group')


@admin.register(Standing)
class StandingAdmin(admin.ModelAdmin):
    list_display = ('team', 'played', 'won', 'lost',
                    'no_result', 'nrr', 'points', 'for_rr', 'against_rr')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('slug', 'num', 'date', 'team1', 'team2', 'status',
                    'min_bet', 'venue', 'type')
    list_filter = ('team1', 'team2', 'venue')


@admin.register(MatchResult)
class MatchResultAdmin(admin.ModelAdmin):
    list_display = ('match', 'winner', 'team1_score', 'team2_score', 'win_type',
                    'win_margin')
    list_filter = ('match__team1', 'match__team2')


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'bet_team', 'bet_amt',
                    'win_lose_amt', 'status', 'updated', 'create_upd_time')
