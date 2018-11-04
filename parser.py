#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from bs4 import BeautifulSoup
import ffmpeg

import getpass
import time
import os


class Parser(object):

    """Docstring for Parser. """

    os.environ['MOZ_HEADLESS'] = '1'
    driver = webdriver.Firefox()
    wait = ui.WebDriverWait(driver, 10)

    def __init__(self):
        self.driver.set_page_load_timeout(15)
        self.driver.get("https://canvas.bham.ac.uk/courses/31135/external_tools/1777/")

    def login(self, username, password):
        self.driver.find_element_by_name("j_username").send_keys(username)
        self.driver.find_element_by_name("j_password").send_keys(password)
        time.sleep(1)
        try:
            self.driver.find_element_by_css_selector(".btn.btn-primary").click()
        except:
            return False
        return True

    def get_video_urls(self):
        links_orig = []
        ids = []
        links = []
        self.driver.get("https://bham.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx?embedded=1#folderID=%2254511c16-cbb6-41c0-86e8-a96b0106b546%22")
        self.wait.until(lambda driver: driver.find_element_by_name("commit"))
        self.driver.find_element_by_name("commit").click()
        time.sleep(4)
        html = self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

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
            self.driver.get(x)
            time.sleep(1)
            links[num] = self.driver.current_url
            num = num + 1
        self.driver.quit()
        return links

def get_videos(username, password):
    p = Parser()

    if not p.login(username, password):
        print("Problem with login")
        return
    links = p.get_video_urls()
    return links

def get_wav(links):
    links = links[::-1]
    for i, link in enumerate(links):
        if not os.path.isfile("out" + str(i) + ".wav"):
            (
                ffmpeg
                .input(link)
                .output("out" + str(i) + ".wav", acodec='pcm_s16le', ac=1)
                .run()
            )

if __name__ == "__main__":
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    get_wav(get_videos(username, password))
