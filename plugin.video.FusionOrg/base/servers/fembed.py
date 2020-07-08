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


def test_fembed(url):
    response = conect.get_url(url, h=default_headers)
    if response != 'Imposible conectar con el server':
        if response.status_code == 200:
            if 'Sorry 404 not found' in response.content or 'Sorry this file does not exist' in response.content:
                return False, 'Link Caido'
            return True, response.content
    return False, 'Imposible conectar con el server'


def calidadesfembed(url):
    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace('/f/', '').replace('/v/', '').replace('/', '')
    url = '{}://feurl.com/f/{}'.format(url_attr[0], id)
    valid, data = test_fembed(url)
    calidades = 'dead'
    sources = []

    if valid:
        calidades = []
        default_headers['Origin'] = 'https://feurl.com'
        default_headers['Referer'] = url
        url = '{}://feurl.com/api/source/{}'.format(url_attr[0], id)
        response = conect.get_url(url, m='post', h=default_headers)
        try:
            for item in response.json()['data']:
                calidades += [item['label']]
        except:
            pass

    return calidades


def urlfembed(url):
    calidad = ''
    if 'calidad' in url:
        calidad = urlparse.parse_qs(url)['calidad'][0]
        url = url.split('&')[0]

    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace('/f/', '').replace('/v/', '').replace('/', '')
    url = '{}://feurl.com/v/{}'.format(url_attr[0], id)
    valid, data = test_fembed(url)
    sources = []
    finalurlfembed = ''
    if valid:
        default_headers['Origin'] = 'https://feurl.com'
        default_headers['Referer'] = url
        url = '{}://feurl.com/api/source/{}'.format(url_attr[0], id)
        response = conect.get_url(url, m='post', h=default_headers, p={'r':'', 'd':'feurl.com'})
        try:
            for item in response.json()['data']:
                if calidad == item['label']:
                    finalurlfembed = item['file']
            if finalurlfembed == '':
                finalurlfembed = item['file']
        except:
            return False, 'Fallo el conector Fembed'
        header_test = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
        header_test = '|' + urllib.urlencode(header_test)

        return True, finalurlfembed + header_test

    return False, ''
