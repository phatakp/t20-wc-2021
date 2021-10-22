from django.apps import apps

Bet = apps.get_model('main', 'Bet')


def user_bet_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Bet.objects.create(user=instance,
                           bet_team=instance.team,
                           bet_amt=500)
