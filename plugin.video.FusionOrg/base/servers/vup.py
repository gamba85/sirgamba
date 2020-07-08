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


def test_vup(url):
    response = conect.get_url(url, h=default_headers)
    if response != 'Imposible conectar con el server':
        if response.status_code == 200:
            if 'File Not Found' in response.content or 'File is no longer available as it expired or has been deleted.' in response.content:
                return False, 'Link Caido'
            return True, response.content
    return False, 'Imposible conectar con el server'


def calidadesvup(url):
    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace(
        '/embed-', '').replace('/', '')
    url = '{}://vup.to/embed-{}.html'.format(url_attr[0], id)
    valid, data = test_vup(url)
    calidades = []
    sources = []

    if valid:
        calidades = []
        sources = re.findall('sources\s*:\s*(\[.*?\])', data, re.I)
        if len(sources) > 0:
            sources = re.findall('\"(.*?)\".*?\"(.*?)\"', sources[0], re.I)
            for source in sources:
                calidades += ['Vup.to']

    return calidades


def urlvup(url):
    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace(
        '/embed-', '').replace('/', '')
    url = '{}://vup.to/embed-{}.html'.format(url_attr[0], id)
    valid, data = test_vup(url)
    calidades = []
    sources = []

    if valid:
        sources = re.findall('sources\s*:\s*(\[.*?\])', data, re.I)
        if len(sources) > 0:
            sources = re.findall('\"(.*?)\".*?\"(.*?)\"', sources[0], re.I)
            for source in sources:
                finalurlvup = source[0]
                header_test = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
                header_test['origin'] = '{}://{}'.format(
                    url_attr[0], url_attr[1])
                header_test['referer'] = url
                header_test = '|' + urllib.urlencode(header_test)

                return True, finalurlvup + header_test

    return False, 'Fallo el conector vup'
