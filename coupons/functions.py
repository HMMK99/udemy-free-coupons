from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import os
from .models import Logs


def log(msg):
    log = Logs(serial_num=0, msg=msg)
    log.save()

def delete_log():
    for log in Logs.objects.all():
        log.delete()


def scrape_answersq():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64;\
                rv:50.0) Gecko/20100101 Firefox/50.0'}
    html_data = requests.get('https://answersq.com/udemy-paid-courses-for-free-with-certificate/',
                             headers=headers)
    soup = BeautifulSoup(html_data.text, 'html.parser')
    log('searching for udemy courses in answersq')
    lis = soup.find_all('li')
    mylist = []
    for li in lis:
        if li.find('a'):
            if 'Enroll for Free' not in str(li.find('a')):
                continue
            mylist.append(li.find('a')['href'])
    log('finished searching')
    return mylist


def scrape_yofree():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64;\
                rv:50.0) Gecko/20100101 Firefox/50.0'}
    html_data = requests.get('https://yofreesamples.com/courses/free-discounted-udemy-courses-list/',
                            headers=headers)
    soup = BeautifulSoup(html_data.text, 'html.parser')
    log('searching for udemy courses in yofreesamples')

    h4s = soup.find_all('h4')
    mylist = []
    for h4 in h4s:
        if h4.find('a') and h4.find('a')['href']:
            mylist.append(h4.find('a')['href'])
    log('finished searching')
    return mylist


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
    mylist = []
    for h5 in h5s[:max_page+10]:
        if h5.find('a') and h5.find('a')['href']:
            sec_page = get_soup(h5.find('a')['href'])
            btns = sec_page.find_all('button')
            for btn in btns:
                if 'Get on Udemy' not in str(btn):
                    continue
                mylist.append(btn['onclick'].split("'")[1])
    log('finished searching')
    return(mylist)


def isFree(links, retries, max_page=1000):

    mylist = []
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    
    if max_page == 1000:
        max_page = len(links)
    num_page = 0
    for link in links:
        name = link.split('/')[-2]
        log('verifying '+name+' in udemy')
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        driver.get(link)
        element = driver.find_element(By.XPATH,
                                      '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]').text
        search_result = re.search('.*left at this price',
                                  element)
        trials = 0
        if search_result and re.search('Free', element):
            
            coupon = link.split('=')[-1]
            url = link
            expiration = search_result.group(0).split('left')[0]
            line = name + ',' +coupon +',' + url + ',' + expiration
            mylist.append(line)
            log('verified')
            num_page = num_page + 1
            if num_page == max_page:
                break
        else:
            log('failed')
            while trials < retries+1:
                log(trials + ' retry')
                driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
                driver.get(link)
                element = driver.find_element(By.XPATH,
                                              '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]').text
                search_result = re.search('.*left at this price',
                                          element)
                if search_result and re.search('Free', element):
                    name = link.split('/')[-2]
                    coupon = link.split('=')[-1]
                    url = link
                    expiration = search_result.group(0).split('left')[0]
                    line = name + ',' +coupon +',' + url + ',' + expiration


                    mylist.append(line)
                    log('verified')
                    num_page = num_page + 1
                    if num_page == max_page:
                        break
                else:
                    log('failed')
                    if trials == retries:
                        print('not found', link)
                        log('faild to retrieve the free course')
                        break

                    trials = trials + 1

        driver.quit()
    return mylist


# data = isFree(scrape_yofree())
# print(data)
# pd.DataFrame(data, columns=['name', 'coupon', 'url', 'expiration']).to_csv('yofreesamples.csv')

# print(len(scrape_fc()))
# data = isFree(scrape_fc())
# pd.DataFrame(data, columns=['name', 'coupon', 'url', 'expiration']).to_csv('coursefolder.csv')

# data = isFree(scrape_answersq())
# pd.DataFrame(data, columns=['name', 'coupon', 'url', 'expiration']).to_csv('answersq.csv')