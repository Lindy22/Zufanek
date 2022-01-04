import time
import datetime
import smtplib
import random

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

url = "https://www.lepsinalada.cz/"
pripona = "/limitovane-edice/"


TEMPLATE_EMAIL = """Subject: OMFG je v nabidce!

Mazej to koupit na: {url}

"""

TEMPLATE_IAMALIVE = """Robot pořád maká! Bohužel zatím se OMFG 2022 v nabídce ještě neobjevil.
"""

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

def get_token(url,pripona):
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

while True:
    tstart = time.time()
    get_token(url, pripona)
    current_time = datetime.datetime.now()
    print(current_time)
    print("total time", time.time()-tstart)
    i_am_alive(current_time, username, password, fromaddr, lindy_mail)
    #i_am_alive(current_time, username, password, fromaddr, gaba_mail)
    execute_script()