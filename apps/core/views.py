from django.shortcuts import redirect, render
from django.utils import timezone

from .utils import (read_html, get_model_objects, Match, )

# Create your views here.


def upload_matches(request):
    html_data = read_html()
    data = get_model_objects(html_data)

    Match.objects.all().delete()
    Match.objects.bulk_create(data)

    # Update Semi Final properties
    Match.objects.filter(num__gt=30,
                         num__lt=33).update(min_bet=100,
                                            type='sf')

    # Update Final properties
    Match.objects.filter(num=33).update(min_bet=200,
                                        type='final')
    return redirect('main:home')
