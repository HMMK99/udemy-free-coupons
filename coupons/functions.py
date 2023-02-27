from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import os
from .models import Logs, Page, URLs
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


def log(msg):
    Logs(msg=msg).save()

def delete_Page():
    pages = Page.objects.all()
    if len(pages) != 0:
        for url in pages:
            url.delete()

def create_page(name, url, coupon, expiration):
    page = Page(name=name, url=url, coupon=coupon, expiration=expiration)
    page.save()

def delete_log():
    logs = Logs.objects.all()
    if len(logs)!= 0:
        for log in logs:
            log.delete()

def delete_URLs():
    urls = URLs.objects.all()
    if len(urls) != 0:
        for url in urls:
            url.delete()


def scrape_answersq(max_page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64;\
                rv:50.0) Gecko/20100101 Firefox/50.0'}
    html_data = requests.get('https://answersq.com/udemy-paid-courses-for-free-with-certificate/',
                             headers=headers)
    soup = BeautifulSoup(html_data.text, 'html.parser')
    log('searching for udemy courses in answersq')
    lis = soup.find_all('li')
    # mylist = []
    if max_page+10 > len(lis):
        max_page = len(lis) - 10
    for li in lis[:max_page+10]:
        if li.find('a'):
            if 'Enroll for Free' not in str(li.find('a')):
                continue
            # mylist.append(li.find('a')['href'])
            yield li.find('a')['href']
    log('finished searching')
    # return mylist


def scrape_yofree(max_page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64;\
                rv:50.0) Gecko/20100101 Firefox/50.0'}
    html_data = requests.get('https://yofreesamples.com/courses/free-discounted-udemy-courses-list/',
                            headers=headers)
    soup = BeautifulSoup(html_data.text, 'html.parser')
    log('searching for udemy courses in yofreesamples')

    h4s = soup.find_all('h4')
    # mylist = []
    if max_page+10 > len(h4s):
        max_page = len(h4s) - 10
    for h4 in h4s[:max_page+10]:
        if h4.find('a') and h4.find('a')['href']:
            # mylist.append(h4.find('a')['href'])
            yield h4.find('a')['href']
    log('finished searching')
    # return mylist


def scrape_fc(max_page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64;\
            rv:50.0) Gecko/20100101 Firefox/50.0'}

    def get_soup(url):
        html_data = requests.get(url,
                                 headers=headers)
        soup = BeautifulSoup(html_data.text, 'html.parser')

        return soup

    soup = get_soup('https://coursefolder.net/free-udemy-coupon.php')
    log('searching for udemy courses in coursefolder')

    h5s = soup.find_all('h5')
    # mylist = []
    if max_page+10 > len(h5s):
        max_page = len(h5s) - 10
    for h5 in h5s[:max_page+10]:
        if h5.find('a') and h5.find('a')['href']:
            sec_page = get_soup(h5.find('a')['href'])
            btns = sec_page.find_all('button')
            for btn in btns:
                if 'Get on Udemy' not in str(btn):
                    continue
                # mylist.append(btn['onclick'].split("'")[1])
                yield btn['onclick'].split("'")[1]
    log('finished searching')
    # return(mylist)


def isFree(link, retries):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    chrome_options.add_argument('user-agent={0}'.format(user_agent))
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    name = link.split('/')[-2]
    log('verifying '+name+' in udemy')
    try:
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get(link)
    except:
        log("can't find the page, contiuing to the next link")
        return HttpResponse()
    try:
        element = driver.find_element(By.XPATH,
                                        '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]').text
    except:
        log("can't find the content, contiuing to the next link")
        return HttpResponse()
    search_result = re.search('.*left at this price',
                                element)
    
    trials = 1
    if search_result and re.search('Free', element):
        coupon = link.split('=')[-1]
        url = link
        expiration = search_result.group(0).split('left')[0]
        # line = {"name": name, coupon: coupon, 'url':url, 'expiration':expiration}
        print(type(name), type(coupon), type(url), type(expiration))
        create_page(name=name, coupon=coupon, url=url, expiration=expiration)

        log('verified')
    else:
        log('failed')
        while trials < retries+1:
            log('retry number ' + str(trials))
            try:
                driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
                driver.get(link)
            except:
                log("can't find the page, contiuing to the next link")
                return HttpResponse()
            try:
                element = driver.find_element(By.XPATH,
                                            '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]').text
            except:
                log("can't find the content, contiuing to the next link")
                return HttpResponse()
            search_result = re.search('.*left at this price',
                                        element)
            if search_result and re.search('Free', element):
                name = link.split('/')[-2]
                coupon = link.split('=')[-1]
                url = link
                expiration = search_result.group(0).split('left')[0]

                page = Page(name= name, coupon= coupon, url=url, expiration=expiration)
                page.save()
                log('verified')
                driver.quit()
                return HttpResponse()

            else:
                log('failed')
                if trials == retries:
                    print('not found', link)
                    log('faild to retrieve the free course')
                    return HttpResponse()

                trials = trials + 1

        driver.quit()
    # log('finished, the file should be downloaded qutomatically')
    return


# data = isFree(scrape_yofree())
# print(data)
# pd.DataFrame(data, columns=['name', 'coupon', 'url', 'expiration']).to_csv('yofreesamples.csv')

# print(len(scrape_fc()))
# data = isFree(scrape_fc())
# pd.DataFrame(data, columns=['name', 'coupon', 'url', 'expiration']).to_csv('coursefolder.csv')

# data = isFree(scrape_answersq())
# pd.DataFrame(data, columns=['name', 'coupon', 'url', 'expiration']).to_csv('answersq.csv')