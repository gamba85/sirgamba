# coding=utf-8
import base64
import hashlib
import json
import os
import re
import time
import urllib
import urlparse

import requests

from base import jsunpack
from resources.lib.conector import conect
import xbmc
import xbmcaddon
import xbmcgui


addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
addon_dir = xbmc.translatePath(xbmc.translatePath(
    addon.getAddonInfo('Path')).decode('utf-8'))

data_path = xbmc.translatePath(addon.getAddonInfo('Profile'))
if not os.path.exists(data_path):
    os.makedirs(data_path)

icon = os.path.join(addon_dir, 'icon.png')


default_headers = dict()
default_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
default_headers['Referer'] = 'https://gounlimited.to/'


def test_gounlimited(url):
    response = conect.get_url(url, h=default_headers)
    if response != 'Imposible conectar con el server':
        if response.status_code == 200:
            if 'Watch output mp4' in response.content or 'x3gnlvr6xn1y.html' in response.content or 'File Not Found' in response.content:
                return False, response.content
            return True, response.content
    return False, 'Imposible conectar con el server'


def gounlimited(url):
    calidad = ''
    if 'calidad' in url:
        calidad = urlparse.parse_qs(url)['calidad'][0]
        url = url.split('&')[0]

    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace(
        'embed-', '').replace('/', '')
    url = '{}://{}/{}.html'.format(url_attr[0], url_attr[1], id)
    valid, data = test_gounlimited(url)
    calidades = []
    finallinks = []
    subtitles = []
    media_subtitles = []
    if valid:
        jspacks = re.findall(
            "(eval.function.p,a,c,k,e,d.*?)\n", data, re.IGNORECASE)
        if len(jspacks) > 0:
            for jspack in jspacks:
                unpack = jsunpack.unpack(jspack)
                data = data.replace(jspack, unpack)

        sources = re.findall(
            "player.src\((\[.*?\])\)", data, re.IGNORECASE)
        if len(sources) > 0:
            sources = sources[0].replace('src', '"src"').replace('type', '"type"').replace('res', '"res"').replace('label', '"label"')
            sources = json.loads(sources)

        subtitles = re.findall("externalTracks:(\[.*?\])", data, re.IGNORECASE)

        if len(subtitles) > 0:
            subtitles = subtitles[0].replace('src', '"src"').replace(
                'label', '"label"').replace('lang', '"lang"')
            subtitles = json.loads(subtitles)
        else:
            subtitles = []

        for subtitle in subtitles:
            media_subtitles.append(
                (subtitle['src'], subtitle['lang'], subtitle['label']))

        calidades = re.findall(
            "Resolution:.*?>\d*x(\d*)<.*?", data, re.IGNORECASE)
        if len(calidades) > 0:
            calidades = [calidades[0]]
        else:
            calidades = re.findall("Size:\s*<.*?>(.*?)<", data, re.IGNORECASE)
            if len(calidades) > 0:
                calidades = [calidades[0]]
            else:
                calidades = ['720']

        if calidad == '':
            return True, calidades, media_subtitles
        else:
            finallink = sources[0]['src']
            default_headers['Referer'] = '{}://{}/embed-{}.html'.format(
                url_attr[0], url_attr[1], id)
            default_headers['cookie'] = 'lang=1'
            return True, finallink + '|' + urllib.urlencode(default_headers)
    else:
        return False, 'Link Muerto :(', media_subtitles
    return False, 'Gounlimited fallo!!!', media_subtitles
