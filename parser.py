#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from bs4 import BeautifulSoup
import getpass
import time
import os
import ffmpeg

os.environ['MOZ_HEADLESS'] = '1'
driver = webdriver.Firefox()
wait = ui.WebDriverWait(driver,10)
driver.set_page_load_timeout(15)
driver.get("https://canvas.bham.ac.uk/courses/31135/external_tools/1777/")
username = raw_input("Username: ")
password = getpass.getpass("Password: ")
driver.find_element_by_name("j_username").send_keys(username)
driver.find_element_by_name("j_password").send_keys(password)
time.sleep(1)
driver.find_element_by_css_selector(".btn.btn-primary").click()
driver.get("https://bham.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx?embedded=1#folderID=%2254511c16-cbb6-41c0-86e8-a96b0106b546%22")
wait.until(lambda driver: driver.find_element_by_name("commit"))
driver.find_element_by_name("commit").click()
time.sleep(4)

html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

links_orig = []
ids = []
links = []
soup = BeautifulSoup(html, features="html5lib")
for x in soup.find_all('a', class_="detail-title"):
    cur = str(x.get('href'))
    links_orig.append(cur)
    if cur.find('=') > -1:
        ids.append(cur[cur.index('=')+1:])

for x in ids:
    links.append("https://bham.cloud.panopto.eu/Panopto/Podcast/Social/" + x + ".mp4?mediaTargetType=videoPodcast")

num = 0
for x in links:
    print(x)
    driver.get(x)
    x = driver.current_url
    try:
        (
            ffmpeg
            .input(x)
            .output('output' + str(num) + '.wav', acodec='pcm_s16le', ac=1)
            .run()
        )
    except:
        driver.quit()
    finally:
        driver.quit()
    num = num + 1

driver.quit()
