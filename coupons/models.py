from django.conf import settings
from django.db import models


class Website(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class URLs(models.Model):
    url = models.CharField(max_length=500, unique=True)


class Page(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url = models.CharField(max_length=500)
    coupon = models.CharField(max_length=255)
    expiration = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Logs(models.Model):
    msg = models.CharField(max_length=255)
