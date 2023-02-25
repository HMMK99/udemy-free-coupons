from django.shortcuts import render
from .models import Logs, Website


def landing(request):
    websites = Website.objects.all()

    return render(request,
                  'landing.html',
                  {'websites': websites})

def logs(request):

    logs = Logs.objects.all()
    return render(request,
                  'log.html',
                  {'logs':logs})
