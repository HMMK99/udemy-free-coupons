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
    page = Website.objects.get(id=website_id)
    if page.name == 'yofreesamples':
        lines = isFree(scrape_yofree())
    if page.name == 'answersq':
        lines = isFree(scrape_answersq())
    if page.name == 'coursefolder':
        lines = isFree(scrape_fc())
    

    response = HttpResponse(content_type='text/csv',
                            headers={'Content-Disposition':
                                     'attachment; filename="data.csv"'})

    line = ['name,coupon,url,expiration']


    writer = csv.writer(response)
    writer.writerow(line)
    for line in lines:
        writer.writerow(line)
    return response
    # delete_log()
    # page = Website.objects.get(id=website_id)
    # if page.name == 'yofreesamples':
    #     lines = scrape_yofree()
    # if page.name == 'answersq':
    #     lines = scrape_answersq()
    # if page.name == 'coursefolder':
    #     lines = scrape_fc()
    
    # response = HttpResponse(content_type="text/csv")
    # response["Content-Disposition"] = f"attachment; filename=data.csv"
    # writer = csv.writer(response)
    # line = 'name,coupon,url,expiration'

    # writer.writerow(line)
    # for l in lines:
    #     writer.writerow(l)