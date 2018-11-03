#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import mechanize
from bs4 import BeautifulSoup
import cookielib
import getpass

cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_cookiejar(cj)
br.open("https://canvas.bham.ac.uk/courses/31135/external_tools/1777/")
username = raw_input("Username: ")
password = getpass.getpass("Password: ")

br.select_form(nr=0)
br.form['j_username'] = username
br.form['j_password'] = password
br.submit()

br.select_form(nr=0)
br.submit(label="Continue")

print(br.response().read())

print("\nNEW PAGE\n")

print(br.response().read())

br.select_form(nr=0)
br.submit()

print("\nNEW PAGE\n")


output_file = open("output.txt", 'w')
output_file.write(br.response().read())
