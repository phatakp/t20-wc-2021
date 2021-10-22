from django.apps import apps
from django.db.models import Q
from datetime import datetime, timedelta

import pytz

Team = apps.get_model('main', 'Team')  # Team model
Match = apps.get_model('main', 'Match')  # Match model


def get_team(name):
    try:
        team_obj = Team.objects.get(
            Q(longname=name) | Q(shortname=name))
        return team_obj
    except:
        return


def read_html():
    from requests_html import HTMLSession
    session = HTMLSession()
    url = 'https://www.t20worldcup.com/fixtures/men'
    r = session.get(url)

    if r.status_code == 200:
        table = r.html.find('.match-block__body')
        table_data = []
        for element in table:
            row_data = element.text.split('\n')
            if len(row_data) == 7:
                table_data.append(row_data)

        cleaned_data = [row[1:4] for row in table_data]
        return cleaned_data


def get_model_objects(html_data):
    num = 0
    data = []
    result = []
    for (desc, team1, team2) in html_data:
        venue, desc_text = desc.split(',')
        date_text = desc_text.split()
        date = datetime.strptime(
            ' '.join(date_text[-5:-1] + ['2021']), '%H:%M %a %d %B %Y') + timedelta(hours=1, minutes=30)
        timezone = pytz.timezone('Asia/Kolkata')
        date = timezone.localize(date)
        if date >= datetime(2021, 10, 23, 0, 0, 0, 0, tzinfo=pytz.timezone('Asia/Kolkata')):
            num += 1
            match = Match(
                num=num,
                venue=venue + ',' + ' '.join(date_text[:-5]),
                date=date,
                team1=get_team(team1),
                team2=get_team(team2),
            )
            data.append(match)
    return data
