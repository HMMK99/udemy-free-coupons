from django.shortcuts import render
from .models import Page, Website


def landing(request):
    websites = Website.objects.all()

    return render(request,
                  'landing.html',
                  {'websites': websites})

def logs(request, str=''):

    if str == '':
        return render(request,
                    'log.html')
    return render(request,
                  'log.html',
                  {'str':str})
