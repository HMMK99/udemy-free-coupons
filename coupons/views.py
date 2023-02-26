from django.shortcuts import render
from .models import Logs, Website
from .functions import scrape_answersq, scrape_fc, scrape_yofree, isFree, delete_log
from django.http import HttpResponse
import csv


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

def scrape(request, website_id):
    delete_log()
    max_page = request.POST.get('max_page')
    retries = request.POST.get('retries')
    page = Website.objects.get(id=website_id)
    if page.name == 'yofreesamples':
        lines = isFree(scrape_yofree(), retries, max_page)
    if page.name == 'answersq':
        lines = isFree(scrape_answersq(), retries, max_page)
    if page.name == 'coursefolder':
        lines = isFree(scrape_fc(max_page), retries)
    

    response = HttpResponse(content_type='text/csv',
                            headers={'Content-Disposition':
                                     'attachment; filename="data.csv"'})

    line = ['name,coupon,url,expiration']


    writer = csv.writer(response)
    writer.writerow(line)
    for line in lines:
        writer.writerow(line)
    return response
