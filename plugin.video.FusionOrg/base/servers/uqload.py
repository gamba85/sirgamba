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


def test_uqload(url):
    response = conect.get_url(url, h=default_headers)
    if response != 'Imposible conectar con el server':
        if response.status_code == 200:
            if 'File Not Found' in response.content or 'File was deleted' in response.content:
                return False, 'Link Caido'
            return True, response.content
    return False, 'Imposible conectar con el server'


def calidadesuqload(url):
    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace(
        'embed-', '').replace('/', '')
    url = '{}://{}/embed-{}.html'.format(url_attr[0], url_attr[1], id)
    valid, data = test_uqload(url)
    calidades = []
    sources = []

    if valid:
        jspacks = re.findall(
            "(eval.function.p,a,c,k,e,d.*?)\n", data, re.IGNORECASE)
        if len(jspacks) > 0:
            for jspack in jspacks:
                unpack = jsunpack.unpack(jspack)
                data = data.replace(jspack, unpack)

        items = re.findall('sources.*?\[(.*?)\]', data, re.IGNORECASE)
        if len(items) > 0:
            for item in items:
                item = (item.replace('"', '').replace("'", '').replace('{', '{"').replace('}', '"}').replace(',', '","').replace(':', '":"').replace(' ', '').replace('":"//', '://').replace('}","{', '},{'))
                sources += item

        if len(sources) > 0:
            return True

    return False


def urluqload(url):
    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace(
        'embed-', '').replace('/', '')
    url = '{}://{}/embed-{}.html'.format(url_attr[0], url_attr[1], id)
    valid, data = test_uqload(url)
    calidades = []
    sources = []

    if valid:
        jspacks = re.findall(
            "(eval.function.p,a,c,k,e,d.*?)\n", data, re.IGNORECASE)
        if len(jspacks) > 0:
            for jspack in jspacks:
                unpack = jsunpack.unpack(jspack)
                data = data.replace(jspack, unpack)

        header_test = {'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
                       'referer': url}
        header_test = '|' + urllib.urlencode(header_test)
        items = re.findall('sources.*?\[(.*?)\]', data, re.IGNORECASE)
        if len(items) > 0:
            for item in items:
                item = (item.replace('"', '').replace("'", '').replace('{', '{"').replace('}', '"}').replace(',', '","').replace(':', '":"').replace(' ', '').replace('":"//', '://').replace('}","{', '},{'))
                finalurluqload = item
                return True, finalurluqload + header_test

    return False, ''
