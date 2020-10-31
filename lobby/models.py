from django.db import models


class Rates(models.Model):
    name = models.CharField(max_length=20, blank=True)
    price = models.FloatField(default='0', blank=True)
    percentage = models.FloatField(default='0')
    kill_award = models.FloatField(default='0', blank=True)
    data = models.DateTimeField(auto_now=False, blank=True)
    people_count = models.IntegerField(default='0')

    class Meta:
        verbose_name = 'Rate'
        verbose_name_plural = 'Rates'

    def __str__(self):
        return self.name


class GameMode(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'GameMode'
        verbose_name_plural = 'GameModes'

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    Rate = models.ForeignKey('Rates', on_delete=models.CASCADE)
    mode = models.ForeignKey(GameMode, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Tournament'
        verbose_name_plural = 'Tournaments'

    def __str__(self):
        return self.name

