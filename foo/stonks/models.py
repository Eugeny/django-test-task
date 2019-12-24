from django.db import models


class Stonk(models.Model):
    name = models.CharField(max_length=255)
    value = models.FloatField()
    score = models.IntegerField(db_index=True)
