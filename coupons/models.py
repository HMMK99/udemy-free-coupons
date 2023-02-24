from django.conf import settings
from django.db import models


class Website(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    coupon = models.CharField(max_length=255)
    expiration = models.CharField(max_length=255)
    site = models.ForeignKey(
        Website, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name
