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
default_headers['Referer'] = 'https://clipwatching.com/'


def test_clipwatching(url):
    response = conect.get_url(url, h=default_headers)
    if response != 'Imposible conectar con el server':
        if response.status_code == 200:
            if 'The file you were looking for could not be found' in response.content or '404 File not found!' in response.content:
                return False, 'Link Caido'
            return True, response.content
    return False, 'Imposible conectar con el server'


def calidadesclipwatching(url):
    url_attr = urlparse.urlparse(url)
    id = url_attr[2]
    id = id.split('/')[1]
    id = id.replace('.html', '').replace(
        'embed-', '').replace('/', '')
    url = '{}://{}/embed-{}.html'.format(url_attr[0], url_attr[1], id)
    valid, data = test_clipwatching(url)
    calidades = []
    sources = []

    if valid:
        jspacks = re.findall(
            "(eval.function.p,a,c,k,e,d.*?)\n", data, re.IGNORECASE)
        if len(jspacks) > 0:
            for jspack in jspacks:
                unpack = jsunpack.unpack(jspack)
                data = data.replace(jspack, unpack)
        items = re.findall('sources.*?(\[.*?\])', data, re.IGNORECASE)
        if len(items) > 0:
            for item in items:
                item = json.loads(item.replace(
                    'src', '"src"').replace('type', '"type"'))
                sources += item
        if len(sources) > 0:
            for source in sources:
                cals = ['360p', '720p']
                i2 = 0
                if 'm3u8' in source['src']:
                    calidades += ['Variable']
                    others = source['src'].split(',')
                    i1 = 0
                    for other in others:
                        if not 'm3u8' in other and not 'http' in other:
                            if i1 == 0:
                                calidades += ['360p']
                            else:
                                calidades += ['720p']
                            i1 += 1
                else:
                    calidades += [cals[i2]]
                    i2 += 1

    return calidades


def urlclipwatching(url):
    calidad = ''
    if 'calidad' in url:
        calidad = urlparse.parse_qs(url)['calidad'][0]
        url = url.split('&')[0]

    url_attr = urlparse.urlparse(url)
    id = url_attr[2]
    id = id.split('/')[1]
    id = id.replace('.html', '').replace(
        'embed-', '').replace('/', '')
    url = '{}://{}/embed-{}.html'.format(url_attr[0], url_attr[1], id)
    valid, data = test_clipwatching(url)
    sources = []
    finalurlclipwatching = ''
    if valid:
        jspacks = re.findall(
            "(eval.function.p,a,c,k,e,d.*?)\n", data, re.IGNORECASE)
        if len(jspacks) > 0:
            for jspack in jspacks:
                unpack = jsunpack.unpack(jspack)
                data = data.replace(jspack, unpack)
        items = re.findall('sources.*?(\[.*?\])', data, re.IGNORECASE)
        if len(items) > 0:
            for item in items:
                item = json.loads(item.replace(
                    'src', '"src"').replace('type', '"type"'))
                sources += item
        i1 = len(sources)
        cals = ['360p', '720p']
        finalurlsclipwatching = {}
        finalurlsclipwatching['Variable'] = ''
        finalurlsclipwatching['360p'] = ''
        finalurlsclipwatching['720p'] = ''
        if len(sources) > 0:
            for source in sources:
                i2 = 0
                if 'm3u8' in source['src']:
                    finalurlsclipwatching['Variable'] = source['src']
                    others = source['src'].split(',')
                    i1 = 0
                    for other in others:
                        if not 'm3u8' in other and not 'http' in other:
                            if i1 == 0:
                                finalurlsclipwatching['360p'] = others[0] + ',' +\
                                    other + ',' + others[-1]
                            else:
                                finalurlsclipwatching['720p'] = others[0] + ',' + \
                                    other + ',' + others[-1]
                            i1 += 1
                else:
                    finalurlsclipwatching[cals[i2]] = source
                    i2 += 1
        if finalurlsclipwatching[calidad] == '':
            for link in finalurlsclipwatching:
                if link != '':
                    finalurlclipwatching = link
        else:
            finalurlclipwatching = finalurlsclipwatching[calidad]
        header_test = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
        header_test = '|' + urllib.urlencode(header_test)

        return True, finalurlclipwatching + header_test

    return False, ''
