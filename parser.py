#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import getpass
import time
import sys


reload(sys)
sys.setdefaultencoding('utf-8')
driver = webdriver.Firefox()
driver.get("https://canvas.bham.ac.uk/courses/31135/external_tools/1777/")
username = raw_input("Username: ")
password = getpass.getpass("Password: ")
driver.find_element_by_name("j_username").send_keys(username)
driver.find_element_by_name("j_password").send_keys(password)
time.sleep(1)
driver.find_element_by_css_selector(".btn.btn-primary").click()
driver.get("https://bham.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx?embedded=1#folderID=%2254511c16-cbb6-41c0-86e8-a96b0106b546%22")
time.sleep(4)
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

for x in links:
    driver.get(x)
    time.sleep(0.5)
    x = driver.current_url
    print(x)

