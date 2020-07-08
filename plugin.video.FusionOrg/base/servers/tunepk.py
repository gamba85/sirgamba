import base64
import hashlib
import json
import os
import re
import time
import urllib
import urlparse

from base import jsunpack
from resources.lib.conector import conect
import requests
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
default_headers['Referer'] = 'https://tune.pk/'


def test_tunepk(url):
    response = conect.get_url(url, h=default_headers)
    if response != 'Imposible conectar con el server':
        if response.status_code == 200:
            return True, response.content
        if response.status_code == 404:
            return False, response.content
    return False, 'Imposible conectar con el server'

def tunepk(url):
    calidad = ''
    if 'calidad' in url:
        calidad = urlparse.parse_qs(url)['calidad'][0]
        url = url.split('&')[0]

    valid, data = test_tunepk(url)
    calidades = []
    finallinks = []
    if valid:
        files = re.findall('files:(\{.*?\})\}',data)
        if len(files)>0:
            files = re.findall('\"(\d*)\":{file:\"(.*?)\"', files[0])
            if len(files)>0:
                sources = {}
                for file in files:
                    sources[file[0]]=json.loads('{"'+file[0]+'":"'+file[1]+'"}')[file[0]]
                if len(sources) > 0:
                    if calidad == '':
                        for calidad in sources:
                            calidades += [calidad]
                        return True, calidades
                    else:
                        finallink = sources[calidad]
            if finallink != '':
                url_attr = urlparse.urlparse(finallink)
                url_qs = urlparse.parse_qs(url_attr[4])
                ttl = int(eval(url_qs.get('ttl', ['time.time()+3600'])[0]))
                ttl += 1
                token = hashlib.md5(
                    str(ttl) + url_attr[2] + ' c@ntr@lw3biutun3cb').digest()
                token = base64.urlsafe_b64encode(
                    token).replace('=', '').replace('\n', '')
                query = '?h=' + token + '&ttl=' + str(ttl)
                finallink = url_attr[0] + '://' + \
                    url_attr[1] + url_attr[2] + query
                return True, finallink + '|' + urllib.urlencode(default_headers)
            return True, url
    return False, 'Tunepk Link Caido!!!'
