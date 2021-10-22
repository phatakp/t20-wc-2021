from datetime import timedelta
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView, DetailView, FormView
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import Team, Standing, MatchResult, Bet
from .forms import BetForm, MatchResultForm
from .utils import validate_bet_and_save, validate_result_and_save

CustomUser = get_user_model()
# Create your views here.


class RulesView(TemplateView):
    template_name = 'main/rules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rule_active'] = 'active'
        context['curr_page'] = 'Game Rules'
        return context


class HomeView(TemplateView):
    template_name = 'main/index.html'

    def match_queryset(self):
        curr_day = timezone.localtime()
        fut_day = curr_day + timedelta(days=3)
        matches = MatchResult.objects.filter(
            match__date__gte=curr_day, match__date__lte=fut_day).order_by('match__date')

        if matches.count() < 4:
            matches = matches | \
                MatchResult.objects.filter(
                    match__status='scheduled').order_by('match__date')

        return matches

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group1'] = Standing.objects.select_related(
            'team').filter(team__group='1')
        context['group2'] = Standing.objects.select_related(
            'team').filter(team__group='2')
        context['matches'] = self.match_queryset()
        context['home_active'] = 'active'
        context['curr_page'] = 'Home Page'
        return context


class DashboardView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'main/dashboard.html'
    context_object_name = 'users'
    login_url = reverse_lazy('accounts:login')

    def get_queryset(self):
        return super().get_queryset().exclude(is_staff=True).select_related('team')

    def match_queryset(self):
        curr_day = timezone.localtime()
        fut_day = curr_day + timedelta(days=3)
        matches = MatchResult.objects.filter(
            match__date__gte=curr_day, match__date__lte=fut_day).order_by('match__date')

        if matches.count() < 4:
            matches = matches | \
                MatchResult.objects.filter(
                    match__status='scheduled').order_by('match__date')

        return matches

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dash_active'] = 'active'
        context['curr_page'] = 'Dashboard'
        context['matches'] = self.match_queryset()
        context['bets'] = Bet.objects.filter(
            user=self.request.user).exclude(match__isnull=True).order_by('-match')
        return context


class MatchListView(ListView):
    model = MatchResult
    template_name = 'main/match_list.html'
    context_object_name = 'matches'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['match_active'] = 'active'
        context['curr_page'] = 'T20 WC Fixtures'
        return context


class MatchDetailView(LoginRequiredMixin, DetailView, FormView):
    model = MatchResult
    template_name = 'main/match_detail.html'
    login_url = reverse_lazy('accounts:login')
    context_object_name = 'match'
    form_class = MatchResultForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.object.match.team1 and self.object.match.team2:
            kwargs['win_teams'] = Team.objects.filter(Q(id=self.object.match.team1.id) |
                                                      Q(id=self.object.match.team2.id))
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['team1_score'] = self.object.team1_score
        initial['team2_score'] = self.object.team2_score
        return initial

    def match_queryset(self):
        curr_day = timezone.localtime()
        fut_day = curr_day + timedelta(days=3)
        matches = MatchResult.objects.filter(
            match__date__gte=curr_day, match__date__lte=fut_day).order_by('match__date')

        if matches.count() < 4:
            matches = matches | \
                MatchResult.objects.filter(
                    match__status='scheduled').order_by('match__date')

        return matches

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['match_active'] = 'active'
        context['team1_form_guide'] = self.get_form_guide(
            self.object.match.team1)
        context['team2_form_guide'] = self.get_form_guide(
            self.object.match.team2)
        context['matches'] = self.match_queryset()
        context['match_bets'] = Bet.objects.filter(match=self.object)
        context['curr_bet'] = self.object.match.min_bet
        try:
            bet = Bet.objects.get(match=self.object, user=self.request.user)
        except:
            pass
        else:
            context['curr_bet'] = bet.bet_amt
            context['curr_team'] = bet.bet_team
            if bet.bet_team:
                context['message'] = f"Your Bet - {bet.bet_team.shortname} for Rs.{bet.bet_amt}"
        return context

    def process_bet_form(self):
        extra_context = {}
        try:
            team_id = int(self.request.POST.get('input_team'))
            amount = int(self.request.POST.get('input_amount'))
        except:
            extra_context['message'] = "Team Selection is Mandatory"
        else:
            team = Team.objects.get(id=team_id)
            data = {'user': self.request.user,
                    'match': self.object,
                    'bet_team': team,
                    'bet_amt': amount}

            extra_context['message'] = validate_bet_and_save(**data)
        return extra_context

    def process_winner_form(self, form):
        print(self.request.POST)
        extra_context = {}
        winner = None
        if self.request.POST.get('winner'):
            winner = Team.objects.get(
                id=self.request.POST.get('winner'))
        data = {'match': self.object.match,
                'winner': winner,
                'win_type': self.request.POST.get('win_type'),
                'win_margin': self.request.POST.get('win_margin'),
                'team1_score': self.request.POST.get('team1_score'),
                'team2_score': self.request.POST.get('team2_score'),
                'status': self.request.POST.get('status'),
                }
        extra_context['result_message'] = validate_result_and_save(**data)
        return extra_context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'input_team' and 'input_amount' in request.POST:
            extra_context = self.process_bet_form()
        else:
            winner_form = MatchResultForm(request.POST)
            extra_context = self.process_winner_form(winner_form)

        context = self.get_context_data(**kwargs)
        context.update(extra_context)
        return render(self.request, self.template_name, context)

    def get_form_guide(self, team):
        # Get results of last five matches
        team_form = MatchResult.objects.filter(Q(match__team1=team) |
                                               Q(match__team2=team)).exclude(
                                                   match__status='scheduled').exclude(
                                                       match=self.object.match).order_by('-match__date')
        team_complete_count = team_form.count()
        if team_complete_count < 5:
            # If less than 5 matches played, then get remaining as scheduled matches
            team_form = team_form | \
                MatchResult.objects.filter(Q(match__team1=team) |
                                           Q(match__team2=team)).filter(
                    match__status='scheduled').exclude(
                    match=self.object.match).order_by('match__date')
        return team_form
