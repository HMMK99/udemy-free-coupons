from django.shortcuts import  render
from .models import Logs, Website, URLs, Page
from .functions import scrape_answersq, scrape_fc, scrape_yofree, isFree, delete_log, log, delete_Page, delete_URLs
from django.http import HttpResponse
import csv
from time import sleep


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

def bs4_scrape(request, website_id):
    delete_log()
    delete_URLs()
    delete_Page()
    max_page = int(request.POST.get('max_page'))
    page = Website.objects.get(id=website_id)
    if max_page < 1:
        return HttpResponse('')
    if page.name == 'yofreesamples':
        urls = scrape_yofree(max_page)
    if page.name == 'answersq':
        urls = scrape_answersq(max_page)
    if page.name == 'coursefolder':
        urls = scrape_fc(max_page)
    
    i = 0
    for url in urls:
        link = URLs(url=url)
        link.save()
        i = i + 1
    response = HttpResponse(i)
    
    return response

def IsFree(request):
    urls = URLs.objects.all()
    if len(urls) == 0:
        return HttpResponse(status=300)
    else:
        retries = int(request.POST.get('retries'))
        link = urls[0]

        isFree(link.url, retries)
        link.delete()
        return HttpResponse('')
    
def printy(request):
    log('FINISHED VERFICATION STEP, THE PAGE WILL DOWNLOAD AUTOMATICALLY')
    response = HttpResponse(content_type='text/csv',
                            headers={'Content-Disposition':
                                     'attachment; filename="data.csv"'})

    line = ['name','coupon','url','expiration']


    writer = csv.writer(response)
    writer.writerow(line)
    pages = Page.objects.all()
    if not pages:
        return response
    for page in pages:
        line = [page.name, page.coupon, page.url, page.expiration]
        writer.writerow(line)
    delete_Page()
    return response
