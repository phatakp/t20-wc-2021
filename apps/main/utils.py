from django.db import transaction
from django.db.models import Sum, F, Q
from django.contrib.auth import get_user_model
from .models import Bet, MatchResult, Standing

CustomUser = get_user_model()


def standardize(overs):
    base = overs // 1
    mantissa = (overs*10) % 10
    if mantissa > 5:
        mantissa = 6-mantissa
        base += 1
    return base + 0.1 * mantissa


def get_rr(rr_str, team_runs, team_overs):
    if rr_str:
        runs, overs = rr_str.split('/')
        runs = int(runs) + int(team_runs)
        overs = float(overs) + float(team_overs)
        overs = standardize(overs)
    else:
        runs, overs = int(team_runs), float(team_overs)
    return f"{runs}/{overs}"


def get_nrr(nrr_str):
    runs, overs = nrr_str.split('/')
    base, mantissa = overs.split('.')
    denom = int(mantissa) / 6
    final_overs = int(base) + denom
    return int(runs)/final_overs


def update_table(match, team1_runs, team1_overs, team2_runs, team2_overs):
    if match.match.team1 == match.winner:
        for_rr = get_rr(match.winner.standing.for_rr, team1_runs, team1_overs)
        against_rr = get_rr(match.winner.standing.against_rr,
                            team2_runs, team2_overs)
        Standing.objects.filter(team=match.match.team1).update(
            played=F('played')+1,
            won=F('won')+1,
            points=F('points')+2,
            for_rr=for_rr,
            against_rr=against_rr,
            nrr=get_nrr(for_rr) - get_nrr(against_rr),
        )

        for_rr = get_rr(match.match.team2.standing.for_rr,
                        team2_runs, team2_overs)
        against_rr = get_rr(match.match.team2.standing.against_rr,
                            team1_runs, team1_overs)
        Standing.objects.filter(team=match.match.team2).update(
            played=F('played')+1,
            lost=F('lost')+1,
            for_rr=for_rr,
            against_rr=against_rr,
            nrr=get_nrr(for_rr) - get_nrr(against_rr),
        )

    else:
        for_rr = get_rr(match.match.team1.standing.for_rr,
                        team1_runs, team1_overs)
        against_rr = get_rr(match.match.team1.standing.against_rr,
                            team2_runs, team2_overs)
        Standing.objects.filter(team=match.match.team1).update(
            played=F('played')+1,
            lost=F('lost')+1,
            for_rr=for_rr,
            against_rr=against_rr,
            nrr=get_nrr(for_rr) - get_nrr(against_rr),
        )

        for_rr = get_rr(match.winner.standing.for_rr, team2_runs, team2_overs)
        against_rr = get_rr(match.winner.standing.against_rr,
                            team1_runs, team1_overs)
        Standing.objects.filter(team=match.match.team2).update(
            played=F('played')+1,
            won=F('won')+1,
            points=F('points')+2,
            for_rr=for_rr,
            against_rr=against_rr,
            nrr=get_nrr(for_rr) - get_nrr(against_rr),
        )


def update_standings(match, status):
    if status == 'abandoned':
        Standing.objects.filter(Q(team=match.match.team1) |
                                Q(team=match.match.team2)).update(played=F('played')+1,
                                                                  no_result=F(
                                                                      'no_result')+1,
                                                                  points=F('points')+1)
    else:
        team1_runs, team1_overs = match.team1_score.split('/')
        team2_runs, team2_overs = match.team2_score.split('/')
        update_table(match, team1_runs, team1_overs, team2_runs, team2_overs)


def update_bet_table(bet, amt):
    if amt < 0:
        bet.status = 'lost'
    else:
        bet.status = 'won'
    bet.win_lose_amt = amt

    # Update user
    user = bet.user
    user.amount = F('amount') + amt

    # Save to DB
    bet.save(update_fields=['win_lose_amt', 'status'])
    user.save(update_fields=['amount'])


def process_winner_prediction_bets(match):
    # Get all bets for IPL Winner
    match_bets = Bet.objects.filter(match__isnull=True)

    if match.winner:  # Match Completed

        # Get winning bets and losing bets
        winning_bets = match_bets.filter(bet_team=match.winner)
        losing_bets = match_bets.exclude(bet_team=match.winner)
        winners = winning_bets.count()

        # Get total win amount and total loss amount
        total_win_amt = winning_bets.aggregate(
            tot_amt=Sum('bet_amt'))['tot_amt']
        total_lost_amt = losing_bets.aggregate(
            tot_amt=Sum('bet_amt'))['tot_amt']
        if total_win_amt and total_lost_amt:  # Some winners and Some losers
            for bet in winning_bets:
                amt = total_lost_amt / winners
                update_bet_table(bet, amt)
            for bet in losing_bets:
                update_bet_table(bet, bet.bet_amt * -1)

        else:  # All winners (bet on same time)
            for bet in match_bets:
                bet.status = 'noresult'
                bet.save(update_fields=['status'])

    else:  # Match Abandoned
        for bet in match_bets:
            bet.status = 'noresult'
            bet.save(update_fields=['status'])


def process_defaulter_bets(match):
    match_bets = Bet.objects.filter(match=match)
    default_cnt = match_bets.filter(status="default").count()
    if default_cnt:  # Defaulter present

        # Get defaulter and non-defaulters
        non_default_bets = match_bets.exclude(status="default")
        default_bets = match_bets.filter(status="default")

        # Get total default amount and total non-default amount
        total_win_amt = non_default_bets.aggregate(
            tot_amt=Sum('bet_amt'))['tot_amt']
        total_lost_amt = default_bets.aggregate(
            tot_amt=Sum('bet_amt'))['tot_amt']
        if total_win_amt:
            for bet in non_default_bets:
                amt = (bet.bet_amt/total_win_amt) * total_lost_amt
                update_bet_table(bet, amt)
            for bet in default_bets:
                update_bet_table(bet, bet.bet_amt * -1)
        else:
            for bet in match_bets:
                bet.status = 'noresult'
                bet.save(update_fields=['status'])
    else:  # No defaulters
        for bet in match_bets:
            bet.status = 'noresult'
            bet.save(update_fields=['status'])


def process_match_completed(match):
    match_bets = Bet.objects.filter(match=match)

    # Get winning bets and losing bets
    winning_bets = match_bets.filter(bet_team=match.winner)
    losing_bets = match_bets.exclude(bet_team=match.winner)

    # Get total win amount and total loss amount
    total_win_amt = winning_bets.aggregate(
        tot_amt=Sum('bet_amt'))['tot_amt']
    total_lost_amt = losing_bets.aggregate(
        tot_amt=Sum('bet_amt'))['tot_amt']
    if total_win_amt and total_lost_amt:  # Some winners and Some losers
        for bet in winning_bets:
            amt = (bet.bet_amt/total_win_amt) * total_lost_amt
            update_bet_table(bet, amt)
        for bet in losing_bets:
            update_bet_table(bet, bet.bet_amt * -1)
    elif total_lost_amt:  # Either defaulters or everyone bet on non winning team
        process_defaulter_bets(match)
    else:  # All winners (bet on same time)
        for bet in match_bets:
            bet.status = 'noresult'
            bet.save(update_fields=['status'])


def settle_bets(match):

    if match.winner:   # Match Completed
        process_match_completed(match)
    else:  # Match Abandoned
        process_defaulter_bets(match)

    if match.match.type == 'final':
        process_winner_prediction_bets(match)


def validate_bet_and_save(user, match, bet_team, bet_amt):

    def get_existing_bet():
        try:
            return Bet.objects.get(match=match, user=user)
        except:
            return

    existing_bet = get_existing_bet()
    if existing_bet and existing_bet.bet_team == bet_team and existing_bet.bet_amt < bet_amt:
        existing_bet.bet_amt = bet_amt
        existing_bet.updated = True
        existing_bet.save(update_fields=['bet_amt', 'updated'])
        return f"Bet increased for {bet_team.shortname} to Rs.{bet_amt}"
    elif existing_bet and existing_bet.bet_team == bet_team:
        return f"For Bet change amount should be more than Rs.{existing_bet.bet_amt}"
    elif existing_bet and existing_bet.bet_team != bet_team and (existing_bet.bet_amt*2) > bet_amt:
        return f"For Team Change minimum amount is Rs.{existing_bet.bet_amt*2}"
    elif existing_bet and existing_bet.bet_team != bet_team:
        existing_bet.bet_team = bet_team
        existing_bet.bet_amt = bet_amt
        existing_bet.updated = True
        existing_bet.save(update_fields=['bet_team', 'bet_amt', 'updated'])
        return f"Bet changed to {bet_team.shortname} for Rs.{bet_amt}"
    elif match.match.entry_cutoff_passed:
        return f"Cutoff Passed for New Bet entry"
    else:
        Bet.objects.create(user=user,
                           match=match,
                           bet_team=bet_team,
                           bet_amt=bet_amt)
        return f"Your Bet - {bet_team.shortname} for Rs.{bet_amt}"


def winner_entered(**data):
    return data.get('winner') or data.get('win_type') or data.get('win_margin')


def winner_valid(**data):
    return data.get('winner') and data.get('win_type') and data.get('win_margin')


def default_bets_placed(obj):
    # Check if number of bets for match is same as number of players
    player_count = CustomUser.objects.exclude(is_staff=True).count()
    bet_placed_count = Bet.objects.filter(
        match=obj).count()
    return player_count == bet_placed_count


def bet_for_match_exists(user, obj):
    return Bet.objects.filter(user=user,
                              match=obj,
                              status='placed').exists()


def add_default_bets(obj):
    # Add default bets for all players where no match bet exists
    all_users = CustomUser.objects.exclude(is_staff=True)
    for user in all_users:
        if not bet_for_match_exists(user, obj):
            Bet.objects.create(user=user,
                               match=obj,
                               bet_amt=obj.match.min_bet,
                               status="default")


@transaction.atomic
def validate_result_and_save(**data):
    match = data.get('match')
    db_obj = MatchResult.objects.get(match=match)
    status = data.get('status')

    if not default_bets_placed(db_obj):
        add_default_bets(db_obj)

    # No Match Status Sent but Winner updated
    if not status and winner_entered(**data):
        return f"Set Match status to Completed"
    elif not status:
        db_obj.team1_score = data.get('team1_score')
        db_obj.team2_score = data.get('team2_score')
        db_obj.save(update_fields=['team1_score', 'team2_score'])
        return f"Team Score(s) Updated"
    elif status == 'abandoned':
        db_obj.team1_score = data.get('team1_score')
        db_obj.team2_score = data.get('team2_score')
        db_obj.save(update_fields=['team1_score', 'team2_score'])

        match.status = status
        match.save(update_fields=['status'])
        if match.type == 'super12':
            update_standings(db_obj, status)
        settle_bets(db_obj)
        return f"Match Updated"
    elif winner_valid(**data):
        match.status = status
        match.save(update_fields=['status'])

        db_obj.team1_score = data.get('team1_score')
        db_obj.team2_score = data.get('team2_score')
        db_obj.winner = data.get('winner')
        db_obj.win_type = data.get('win_type')
        db_obj.win_margin = data.get('win_margin')
        db_obj.save()

        if match.type == 'super12':
            update_standings(db_obj, status)
        settle_bets(db_obj)
        return f"Match Updated"
    else:
        return f"Set all attributes for the win"
