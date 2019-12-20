from django.contrib import admin
from django.urls import path
import foo.stonks.views

urlpatterns = [
    path('', foo.stonks.views.index_view),
    path('refresh', foo.stonks.views.refresh_view),
    path('top', foo.stonks.views.top_view),
]
