# -*- coding: utf-8 -*-
import json
import os
import re
import urllib
import urlparse

from base import jsunpack
from resources.lib.conector import conect


default_headers = dict()
default_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
default_headers['Referer'] = 'https://mixdrop.com/'


def test_mixdrop(url):
    response = conect.get_url(url, h=default_headers)
    if response != 'Imposible conectar con el server':
        if response.status_code == 200:
            if 'WE ARE SORRY' in response.content or "We can't find the file you are looking for." in response.content:
                return False, 'Link Caido'
            return True, response.content
    return False, 'Imposible conectar con el server'


def calidadesmixdrop(url):
    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace(
        '/f/', '').replace('/e/', '').replace('/', '')
    url = '{}://{}/e/{}/'.format(url_attr[0], url_attr[1], id)
    valid, data = test_mixdrop(url)
    calidades = []
    sources = []

    if valid:
        jspacks = re.findall(
            "(eval.function.p,a,c,k,e,d.*?)\n", data, re.IGNORECASE)
        if len(jspacks) > 0:
            for jspack in jspacks:
                unpack = jsunpack.unpack(jspack)
                data = data.replace(jspack, unpack)

        items = re.findall('wurl\s*=\s*\"(.+?)\"', data, re.IGNORECASE)
        if len(items) > 0:
            for item in items:
                return ['MIXdrop']

    return calidades


def urlmixdrop(url):
    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace(
        '/f/', '').replace('/e/', '').replace('/', '')
    url = '{}://{}/e/{}/'.format(url_attr[0], url_attr[1], id)
    valid, data = test_mixdrop(url)
    calidades = []
    sources = []
    finalurlmixdrop = ''

    if valid:
        jspacks = re.findall(
            "(eval.function.p,a,c,k,e,d.*?)\n", data, re.IGNORECASE)
        if len(jspacks) > 0:
            for jspack in jspacks:
                unpack = jsunpack.unpack(jspack)
                data = data.replace(jspack, unpack)

        items = re.findall('wurl\s*=\s*\"(.+?)\"', data, re.IGNORECASE)
        if len(items) > 0:
            for item in items:
                if item.startswith('//'):
                    finalurlmixdrop = url_attr[0] + ':' + item
                header_test = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
                header_test['origin'] = url = '{}://{}'.format(
                    url_attr[0], url_attr[1])
                header_test['referer'] = url
                header_test = '|' + urllib.urlencode(header_test)

                return True, finalurlmixdrop + header_test

    return False, ''
