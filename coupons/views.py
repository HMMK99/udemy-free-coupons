from django.shortcuts import render
from .models import Page, Website


def landing(request):
    websites = Website.objects.all()

    return render(request,
                  'landing.html',
                  {'websites': websites})

def logs(request):

    return render(request,
                  'log.html')
