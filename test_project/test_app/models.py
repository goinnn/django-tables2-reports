from django.db import models


class Person(models.Model):
    first = models.CharField(max_length=200)
    last = models.CharField(max_length=200)
    dob = models.DateField()
    active = models.BooleanField(default=True)
