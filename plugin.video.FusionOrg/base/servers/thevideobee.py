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


def test_thevideobee(url):
    response = conect.get_url(url, h=default_headers)
    if response != 'Imposible conectar con el server':
        if response.status_code == 200:
            if 'File Not Found' in response.content or 'ile is no longer available as it expired or has been deleted.' in response.content:
                return False, 'Link Caido'
            return True, response.content
    return False, 'Imposible conectar con el server'


def calidadesthevideobee(url):
    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace(
        '/embed-', '').replace('/', '')
    url = '{}://{}/embed-{}.html'.format(url_attr[0], url_attr[1], id)
    valid, data = test_thevideobee(url)
    calidades = []
    sources = []

    if valid:
        calidades = []
        sources = re.findall('sources\s*:\s*(\[.*?\])', data, re.I)
        if len(sources) > 0:
            sources = eval(sources[0])
            for source in sources:
                if 'm3u8' in source:
                    calidades += ['Variable']
                    others = source.split(',')
                    i = 0
                    for other in others:
                        if not 'm3u8' in other and not 'http' in other:
                            if i == 0:
                                calidades += ['Low']
                            elif i == 1:
                                calidades += ['Med']
                            elif i == 2:
                                calidades += ['High']
                            else:
                                calidades += ['Higher']
                            i += 1

    return calidades


def urlthevideobee(url):
    calidad = ''
    if 'calidad' in url:
        calidad = urlparse.parse_qs(url)['calidad'][0]
        url = url.split('&')[0]

    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace(
        '/embed-', '').replace('/', '')
    url = '{}://{}/embed-{}.html'.format(url_attr[0], url_attr[1], id)
    valid, data = test_thevideobee(url)
    calidades = []
    sources = []

    if valid:
        sources = re.findall('sources\s*:\s*(\[.*?\])', data, re.I)
        if len(sources) > 0:
            sources = eval(sources[0])
            for source in sources:
                if 'm3u8' in source:
                    if calidad == 'Variable':
                        finalurlthevideobee = source
                    else:
                        others = source.split(',')
                        i = 0
                        others[0] = others[0].replace('/hls/', '/')
                        for other in others:
                            if not 'm3u8' in other and not 'http' in other:
                                if calidad == 'Low' and i == 0:
                                    finalurlthevideobee = others[0] + \
                                        other + '/v.mp4'
                                elif calidad == 'Med' and i == 1:
                                    finalurlthevideobee = others[0] + \
                                        other + '/v.mp4'
                                elif calidad == 'High' and i == 2:
                                    finalurlthevideobee = others[0] + \
                                        other + '/v.mp4'
                                elif calidad == 'Higher' and i > 2:
                                    finalurlthevideobee = others[0] + \
                                        other + '/v.mp4'
                                i += 1

                    header_test = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
                    header_test['origin'] = '{}://{}'.format(
                        url_attr[0], url_attr[1])
                    header_test['referer'] = url
                    header_test = '|' + urllib.urlencode(header_test)

                    return True, finalurlthevideobee + header_test

    return False, 'Fallo el conector thevideobee'
