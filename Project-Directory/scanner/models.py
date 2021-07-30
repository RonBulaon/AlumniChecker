from django.db import models
from django.db.models.deletion import CASCADE


class Visitor(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)

    def __str__(self):
        return self.barcode

 
class Visit(models.Model):
    barcode = models.CharField(max_length=100)
    membership = models.CharField(max_length=100)
    name = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    status = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.barcode


class PeakHours(models.Model):
    hour = models.CharField(max_length=100)

    def __str__(self):
        return self.hour


class Configuration(models.Model):
    api = models.CharField(max_length=300)
    visits_pagination = models.PositiveSmallIntegerField(default=100, blank=False, null=False)

    def __str__(self):
        return self.api