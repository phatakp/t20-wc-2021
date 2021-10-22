from django.apps import apps

MatchResult = apps.get_model('main', 'MatchResult')


def get_team(team):
    if team:
        return str(team)
    else:
        return 'TBC'


def match_receiver(sender, instance, created, *args, **kwargs):
    if not instance.slug:
        result = []
        result.append(get_team(instance.team1))
        result.append('vs')
        result.append(get_team(instance.team2))
        result.append(instance.date.strftime('%Y-%m-%d'))
        instance.slug = '-'.join(result)
        instance.save()
        if created:
            MatchResult.objects.create(match=instance, slug=instance.slug)
        else:
            MatchResult.objects.filter(
                match=instance).update(slug=instance.slug)
