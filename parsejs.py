#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_html import HTMLSession
import cookielib


def parse(url, cookies):
    session = HTMLSession()
    r = session.get(url, cookies=cookies)
    r.html.render()
    htmlRendered = str(r.html)
    return htmlRendered
