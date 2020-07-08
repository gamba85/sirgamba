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


def test_upstream(url):
    response = conect.get_url(url, h=default_headers)
    if response != 'Imposible conectar con el server':
        if response.status_code == 200:
            if 'File Not Found' in response.content or 'File is no longer available' in response.content:
                return False, 'Link Caido'
            return True, response.content
    return False, 'Imposible conectar con el server'


def calidadesupstream(url):
    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace(
        '/embed-', '').replace('/', '')
    url = '{}://upstream.to/embed-{}.html'.format(url_attr[0], id)
    valid, data = test_upstream(url)
    calidades = []
    sources = []

    if valid:
        calidades = []
        sources = re.findall('sources\s*:\s*.*?\"(.*?)\"', data, re.I)
        if len(sources) > 0:
            return True
    return False


def urlupstream(url):
    #===========================================================================
    # calidad = ''
    # if 'calidad' in url:
    #     calidad = urlparse.parse_qs(url)['calidad'][0]
    #     url = url.split('&')[0]
    #===========================================================================

    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace(
        '/embed-', '').replace('/', '')
    url = '{}://upstream.to/embed-{}.html'.format(url_attr[0], id)
    valid, data = test_upstream(url)
    calidades = []
    sources = []

    if valid:
        sources = re.findall('sources\s*:\s*.*?\"(.*?)\"', data, re.I)
        if len(sources) > 0:
            header_test = {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
            header_test = '|' + urllib.urlencode(header_test)

            return True, sources[0] + header_test

    return False, 'Fallo el conector UpStream'
