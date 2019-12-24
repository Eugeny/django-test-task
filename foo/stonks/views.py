import time
from django.db import transaction
from django.http import HttpResponse
from random import random

from .models import Stonk


def index_view(request):
    return HttpResponse('''
    <!DOCTYPE html>
    <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css">
            <script type="text/javascript">
                async function fluctuate() {
                    document.getElementById('fluctuator').innerHTML = await (await fetch('/refresh')).text()
                }

                async function getTop() {
                    document.getElementById('top').innerHTML = await (await fetch('/top')).text()
                }
            </script>
        </head>
        <body>
            <div class="container">
                <div>
                    <button onclick="fluctuate()" class="button is-primary">Fluctuate stonks (takes a bit)</button>
                    <button onclick="getTop()" class="button is-primary">Get top stonks</button>
                </div>
                <div id="fluctuator"></div>
                <div id="top"></div>
            </div>
        </body>
        </html>
    ''')


@transaction.atomic
def refresh_view(request):
    for stonk in Stonk.objects.all():
        fluctuate_stonk(stonk)
    return HttpResponse('Stonks fluctuated')


@transaction.atomic
def top_view(request):
    for stonk in Stonk.objects.filter(value__gt=25000):
        bump_stonk(stonk)

    for stonk in Stonk.objects.filter(value__lt=25000):
        hump_stonk(stonk)

    result = ''
    for stonk in Stonk.objects.order_by('-score')[:10]:
        result += f'{stonk.name} = {stonk.value} (score {stonk.score})<br/>'
    return HttpResponse(result)


def fluctuate_stonk(stonk):
    # Do not change
    print(f'Updating stonk {stonk.name}')
    stonk.value += random()
    stonk.save()
    time.sleep(0.005)


def bump_stonk(stonk):
    # Do not change
    stonk.score += 5
    stonk.save()


def hump_stonk(stonk):
    # Do not change
    stonk.score -= 2
    stonk.save()
