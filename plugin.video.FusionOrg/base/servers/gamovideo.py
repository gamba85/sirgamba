# -*- coding: utf-8 -*-
import json
import re
import urllib
from urlparse import urlparse

import requests

from base import jsunpack
import xbmcgui


headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'


def urlgamovideo(url):
    url_attr = urlparse(url)
    id_gamovideo = re.findall('(\w{12})', url_attr[2], re.I)[0]
    url = 'http://{}/{}.html'.format(url_attr[1], id_gamovideo)

    s = requests.Session()
    s.headers.update(
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'})

    r = s.get(url)
    source = r.content
    if test_online(source):
        r = s.get(url)
        source = r.content
        if test_online(source):
            source = re.sub('(\r){1,}', '', source)
            source = re.sub('(\n){1,}', '', source)
            source = re.sub('(\t){1,}', '', source)
            source = re.sub('(\s){1,}', ' ', source)
            header_test = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
            jspacks = re.findall(
                "<script type=.text/javascript.>(eval.function.p,a,c,k,e,d..*?)</script>", source, re.IGNORECASE)
            if len(jspacks) > 0:
                for jspack in jspacks:
                    source = source.replace(jspack, jsunpack.unpack(jspack))

            finalurlgamo = re.findall(
                'file:\s*\"(http.*?mp4)\"', source, re.IGNORECASE)[0]
            header_test = '|' + urllib.urlencode(header_test)
            return finalurlgamo + header_test
    exit()


def test_online(source):
    error = ''
    if 'Imposible conectar con el server' in source:
        error = 'Imposible conectar con el server'
    if 'File was deleted' in source or 'File Not Found' in source or 'File was locked by administrator' in source:
        error = 'El archivo no existe o ha sido borrado'
    if 'Video is processing now' in source:
        error = 'El video está procesándose en estos momentos. Inténtelo mas tarde.'
    if 'File is awaiting for moderation' in source:
        error = 'El video está esperando por moderación.'
    if error != '':
        dialog = xbmcgui.Dialog()
        dialog.notification('FusionOrg', 'Fallo: ' + error,
                            xbmcgui.NOTIFICATION_INFO, 5000, True)
        return False
    return True
