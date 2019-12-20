from django.db import models


class Stonk(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    value = models.FloatField()
    score = models.IntegerField()
