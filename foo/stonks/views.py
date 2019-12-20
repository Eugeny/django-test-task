import time
from django.db import transaction
from django.http import HttpResponse
from random import random

from .models import Stonk


def index_view(request):
    return HttpResponse('''
        <script type="text/javascript">
            async function fluctuate() {
                document.getElementById('fluctuator').innerHTML = await (await fetch('/refresh')).text()
            }

            async function getTop() {
                document.getElementById('top').innerHTML = await (await fetch('/top')).text()
            }
        </script>
        <body>
            <button onclick="fluctuate()">Fluctuate stonks (takes a bit)</button>
            <button onclick="getTop()">Get top stonks</button>
            <div id="fluctuator"></div>
            <div id="top"></div>
        </body>
    ''')


@transaction.atomic
def refresh_view(request):
    for stonk in Stonk.objects.all():
        print(f'Updating stonk {stonk.name}')
        stonk.value += random()
        stonk.save()
        time.sleep(0.005)
    return HttpResponse('Stonks fluctuated')


@transaction.atomic
def top_view(request):
    for stonk in Stonk.objects.filter(value__gt=25000):
        stonk.score += 5
        stonk.save()

    for stonk in Stonk.objects.filter(value__lt=25000):
        stonk.score -= 2
        stonk.save()

    result = ''
    for stonk in Stonk.objects.order_by('-score')[:10]:
        result += f'{stonk.name} = {stonk.value} (score {stonk.score})<br/>'
    return HttpResponse(result)
