from django import forms
from apps.core.statics import STATUS_CHOICES
from .models import Bet, MatchResult


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ('bet_team', 'bet_amt')


class MatchResultForm(forms.ModelForm):
    RESULT_CHOICES = [(None, '----'), ] + STATUS_CHOICES[1:]
    status = forms.ChoiceField(label="Status", choices=RESULT_CHOICES)

    class Meta:
        model = MatchResult
        fields = ('winner', 'team1_score', 'team2_score',
                  'win_type', 'win_margin')

    def __init__(self, *args, **kwargs):
        win_teams = kwargs.pop('win_teams', None)
        super().__init__(*args, **kwargs)
        print(self.instance.team1_score)
        if win_teams:
            self.fields['winner'].queryset = win_teams
        for field in self.fields:
            self.fields[field].required = False
