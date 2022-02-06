import time
import datetime
import smtplib
import random
import urllib3
import lxml.etree

from selenium import webdriver
from selenium.webdriver.common.by import By
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

fromaddr = 'lindybot22@gmail.com'
lindy_mail = 'tomaslindauer@gmail.com'
gaba_mail = 'kovac.gabriel@gmail.com'
username = "lindybot22"
password = "raspibot99"

hour = [6, 7, 8, 11, 13, 15, 17, 19, 21, 23]
minute = [55, 56, 57]

httpcon = urllib3.PoolManager()
url = "https://www.lepsinalada.cz/"
pripona = "/limitovane-edice/"


TEMPLATE_EMAIL = """Subject: OMFG je v nabidce!

Mazej to koupit na: {url}

"""

TEMPLATE_IAMALIVE = """Robot pořád maká! Bohužel zatím se OMFG 2022 v nabídce ještě neobjevil.
"""


def get_url(httpcon, url):
    headers = {}
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    headers["Accept-Encoding"] = "gzip, deflate"
    headers["Accept-Language"] = "cs,en-us;q=0.7,en;q=0.3"
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"
    # headers["Cookie"]="op_cookie-test=ok;op_oddsportal=cv704mv1ek2l60ijve9iq9hn62;op_user_cookie=32830896;D_UID=739B93C4-5FB3-34AB-A4B5-0C2C36C3347E"
    res = httpcon.urlopen("GET", url, headers=headers)

    if res.status != 200:
        print(res.status)
        raise Exception("Unable to get_url " + url)
    # print res.data
    return res.data

def execute_script():
    time.sleep(random.uniform(60, 120))

def i_am_alive(current_time,username,password, fromaddr,toaddr):
    if current_time.hour in hour and current_time.minute in minute:
    #if current_time.hour in hour:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        msg = MIMEMultipart()
        msg['Subject'] = str("Žufánek jede!")
        body = MIMEText(TEMPLATE_IAMALIVE)
        msg.attach(body)
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()

def send_email(username,password, fromaddr,toaddr,url):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    msg = TEMPLATE_EMAIL.format(url = url)
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()

def get_page_browser(url,pripona):
    browser = webdriver.Firefox()
    # time.sleep(10)
    browser.get(url+pripona)
    time.sleep(3)
    browser.find_element(By.XPATH, '//div[@class="colorbox-html-content"]/div[@class="site-agreement-inner"]/div[@class="site-agreement-buttons"]/a[@id="site-agree-button"]').click()
    time.sleep(3)
    element = browser.find_elements(By.XPATH, '//div[@id="products"]/div[@class="product"]/div[@class="p"]/a')
    omfg_url = []
    for elem in element:
        elem_href = elem.get_attribute("href")
        if "omfg" in elem_href:
            omfg_url.append(elem_href)
        else:
            pass
    for urls in omfg_url:
        print(urls)
        browser.get(urls)
        time.sleep(3)
        availability = browser.find_element(By.CLASS_NAME, "availability-label").text
        if availability == "Vyprodáno":
            print(availability)
        else:
            send_email(username, password, fromaddr, lindy_mail, urls)
            send_email(username, password, fromaddr, gaba_mail, urls)
            print("Je v nabídce!")
    browser.close()

def get_page_raspi(httpcon, url,pripona):
    print(url+pripona)
    htmlparser = lxml.etree.HTMLParser()
    page = get_url(httpcon, url+pripona)
    p = lxml.etree.fromstring(page, htmlparser)
    #print(''.join(p.itertext()).encode('utf-8'))
    element = p.xpath(u'//div[@id="products"]/div[@class="product"]/div[@class="p"]/a/@href')
    #print(element)
    omfg_url = []
    for elem_href in element:
        if "omfg" in elem_href:
            omfg_url.append(elem_href)
        else:
            pass
    for urls in omfg_url:
        #print(urls)
        page_omfg = get_url(httpcon, url + urls)
        p_omfg = lxml.etree.fromstring(page_omfg, htmlparser)
        availability_xpath = p_omfg.xpath(u'//div[@class="availability-value"]/span[@class="availability-label"]/text()')
        availability = availability_xpath[0].strip()
        #print(availability)
        if availability == "Vyprodáno":
            print(availability)
        else:
            #send_email(username, password, fromaddr, lindy_mail, urls)
            #send_email(username, password, fromaddr, gaba_mail, urls)
            print("Je v nabídce!")

while True:
    tstart = time.time()
    get_page_browser(url, pripona)
    #get_page_raspi(httpcon, url, pripona)
    current_time = datetime.datetime.now()
    print(current_time)
    print("total time", time.time()-tstart)
    i_am_alive(current_time, username, password, fromaddr, lindy_mail)
    #i_am_alive(current_time, username, password, fromaddr, gaba_mail)
    execute_script()