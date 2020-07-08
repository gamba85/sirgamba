# -*- coding: utf-8 -*-
import json
import os
import re
import sys
import urllib
import urlparse

from base import jsunpack
from resources.lib.conector import conect
import xbmcgui
import xbmcplugin


addon_handle = int(sys.argv[1])
default_headers = dict()
default_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'


def test_okru(url):
    response = conect.get_url(url, h=default_headers)
    if response != 'Imposible conectar con el server':
        if response.status_code == 200:
            if 'Video has not been found' in response.content or 'movieBlocked' in response.content:
                return False, 'Link Caido'
            return True, response.content
    return False, 'Imposible conectar con el server'


def calidadesokru(url):
    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace(
        '/videoembed/', '').replace('/video/', '').replace('/live/', '').replace('/', '')
    url = '{}://{}/videoembed/{}'.format(url_attr[0], url_attr[1], id)
    valid, data = test_okru(url)
    calidades = []
    sources = []

    if valid:
        metadata = ''
        options = re.findall('data-options=\"(.*?)\"', data, re.I)
        for option in options:
            if metadata == '':
                option = option.replace('&quot;', '"')
                try:
                    option = json.loads(option)
                    metadata = option.get('flashvars', '')
                    metadata = metadata.get('metadata', '')
                    metadata = json.loads(metadata)
                except:
                    pass

        if metadata != '':
            videos = metadata.get('videos', '')
            for video in videos:
                calidades += [video['name'].title()]
            stream = metadata.get('hlsManifestUrl', None)
            if stream:
                calidades += ['Variable']

            stream = metadata.get('hlsMasterPlaylistUrl', None)
            if stream:
                calidades += ['On Live']

            return True, calidades

    return False, calidades


def urlokru(url):
    calidad = ''
    if 'calidad' in url:
        calidad = urlparse.parse_qs(url)['calidad'][0]
        url = url.split('&')[0]
    url_attr = urlparse.urlparse(url)
    id = url_attr[2].replace('.html', '').replace(
        '/videoembed/', '').replace('/video/', '').replace('/live/', '').replace('/', '')
    url = '{}://{}/videoembed/{}'.format(url_attr[0], url_attr[1], id)
    valid, data = test_okru(url)
    calidades = []
    sources = []

    if valid:
        metadata = ''
        options = re.findall('data-options=\"(.*?)\"', data, re.I)
        for option in options:
            if metadata == '':
                option = option.replace('&quot;', '"')
                try:
                    option = json.loads(option)
                    metadata = option.get('flashvars', '')
                    metadata = metadata.get('metadata', '')
                    metadata = json.loads(metadata)
                except:
                    pass

        if metadata != '':
            header_test = {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
            header_test['origin'] = 'https://ok.ru'
            header_test['referer'] = url
            header_test = '|' + urllib.urlencode(header_test)

            videos = metadata.get('videos', '')
            for video in videos:
                if video['name'].title() == calidad:
                    return True, video['url'] + header_test
            stream = metadata.get('hlsMenifestUrl', None)
            if stream:
                if calidad == 'Variable':
                    return True, stream + header_test
            if calidad != '' and not ('Live' in calidad):
                return True, videos[-1]['url'] + header_test

            live1 = metadata.get('hlsMasterPlaylistUrl', None)
            if live1:
                if calidad == 'On Live' or calidad == '':
                    play_item = xbmcgui.ListItem(
                        path=live1 + '|' + header_test)
                    play_item.setProperty("IsPlayable", "true")
                    play_item.setProperty(
                        'inputstream.adaptive.manifest_type', 'hls')
                    play_item.setMimeType(
                        'application/vnd.apple.mpegstream_url')
                    play_item.setContentLookup(False)
                    play_item.setProperty(
                        'inputstream.adaptive.stream_headers', header_test)
                    xbmcplugin.setResolvedUrl(
                        addon_handle, True, listitem=play_item)
                    exit()
            dialog = xbmcgui.Dialog()
            dialog.notification('FusionOrg', 'Fallo en: ' +
                                url, xbmcgui.NOTIFICATION_INFO, 5000, True)
            xbmc.sleep(1000)
            exit()

    return False, ''
