from django.contrib import admin
from lobby.models import Tournament, GameMode, Rates

admin.site.register(Tournament)
admin.site.register(Rates)
admin.site.register(GameMode)
# Register your models here.
