# -*- coding: utf-8 -*-
import base64
import json
import os
import pickle
import re
import sys
import urllib

import requests

from base import jsunpack
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin


addon_handle = int(sys.argv[1])
addonInfo = xbmcaddon.Addon().getAddonInfo
ansc = ['kZ1c2lvblR2LlJlcXVlc3Q', 'mxpdmUuc3RyZWFtc3Bybw=',
        'kZ1c2lvbk9yZw=', 'mxpdmUuc3RyZWFtRnVzaW9u']
ans = []
headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
addon = xbmcaddon.Addon()
addon_data_dir = xbmc.translatePath(xbmc.translatePath(
    addon.getAddonInfo('profile')).decode('utf-8'))
cookies_path = os.path.join(addon_data_dir, 'coo_ws.jar')
dialog = xbmcgui.Dialog()


def p(ansc=ansc, ans=ans):
    for an in ansc:
        ans += [base64.b64decode('cGx1Z2luLnZpZGVvL' + an + '=')]

    if addonInfo('id') in ans:
        return base64.b64decode('VHJ1ZQ===')
    return False


def load_cookies():
    try:
        if os.path.isfile(cookies_path):
            with open(cookies_path, 'rb') as (f):
                return pickle.load(f)
    except:
        pass

    return ''


def save_cookies(cookies):
    if not os.path.exists(addon_data_dir):
        os.mkdir(addon_data_dir)
    with open(cookies_path, 'wb') as (f):
        pickle.dump(cookies, f)


def get_url(url, m='get', p='', h=headers, r=True, c=''):
    data = 'Imposible conectar con el server'
    cookies = ''
    location = ''
    if m == 'get' or m == '':
        try:
            if c == '':
                response = requests.get(
                    url, headers=h, timeout=10, allow_redirects=r)
            else:
                response = requests.get(
                    url, headers=h, timeout=10, allow_redirects=r, cookies=c)
        except:
            return (
                data, cookies, location)

    if m == 'post':
        try:
            if c == '':
                response = requests.post(
                    url, headers=h, data=p, timeout=10, allow_redirects=r)
            else:
                response = requests.post(
                    url, headers=h, data=p, timeout=10, allow_redirects=r, cookies=c)
        except:
            return (
                data, cookies, location)

    if response.status_code == 200:
        data = response.content
        cookies = response.cookies
        location = response.headers.get('location')
    return (data, cookies, location)


def resolver(url, referer='', headers_tv=headers):
    if not p():
        dialog.notification(base64.b64decode('RnVzaW9uIFRFQU0='), base64.b64decode(
            'SW5zdGFsYSBGdXNpb25PcmcgcGFyYSB2ZXIgZXN0ZSBjb250ZW5pZG8='), xbmcgui.NOTIFICATION_INFO, 20000, True)
        exit()
    url = re.sub('(\r){1,}', '', url)
    url = re.sub('(\n){1,}', '', url)
    url = re.sub('(\t){1,}', '', url)
    url = re.sub('(\s){1,}', '', url)
    if type(referer) == list:
        referer = referer[0]
    if type(referer) == tuple:
        referer = referer[0]
    referer = re.sub('(\r){1,}', ' ', referer)
    referer = re.sub('(\r){1,}', ' ', referer)
    referer = re.sub('(\n){1,}', ' ', referer)
    referer = re.sub('(\t){1,}', ' ', referer)
    referer = re.sub('(\s){1,}', ' ', referer)
    if referer == '':
        if 'referer' in url:
            url = url.split('referer')
            referer = url[1].replace('=', '')
            url = url[0]
    if not 'referer' in url:
        url = url.replace('&', '')

    if referer == '':
        if 'football-live.stream' in url:
            headers_tv['Referer'] = 'https://football-live.stream'
        if 'wstream' in url:
            headers_tv['Referer'] = 'https://wstream.to/'
    else:
        headers_tv['Referer'] = referer

    try:
        data, cookies, location = get_url(url, h=headers_tv)
        if 'p,a,c,k,e,d' in data:
            packeds = re.findall('(eval\\(function\\(p,a,c,k,e,d.*)', data)
            for packed in packeds:
                unpacked = jsunpack.unpack(packed).replace('\\', '')
                data = data.replace(packed, unpacked)
        data = re.sub('(\r){1,}', ' ', data)
        data = re.sub('(\n){1,}', ' ', data)
        data = re.sub('(\t){1,}', ' ', data)
        data = re.sub('(\s){1,}', ' ', data)

        if 'football-live.stream' in url:
            headers_tv['Origin'] = 'https://football-live.stream'
            headers_tv['Referer'] = url
        if 'wstream' in url:
            headers_tv['Origin'] = 'https://wstream.to'
            headers_tv['Referer'] = url
        final_link = re.findall('source:\"(.*?)"', data, re.I)
        if len(final_link) == 0:
            final_link = re.findall("source:\s*\'(.*?)'", data, re.I)
        if len(final_link) > 0:
            headers_play = headers_tv
            headers_play = urllib.urlencode(headers_play)
            url = final_link[0]

            dialog = xbmcgui.Dialog()
            dialog.notification("FusionOrg", "Iniciando reproducción",
                                xbmcgui.NOTIFICATION_INFO, 5000, False)
            headers_play = headers_play.replace('Origin', 'origin').replace(
                'Referer', 'referer').replace('User-Agent', 'user-agent')
            play_item = xbmcgui.ListItem(path=url + '|' + headers_play )
            xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
            version=float(xbmc_version[:4])
            if version <= 18.6:
                play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
            else:
                play_item.setProperty('inputstream', 'inputstream.adaptive')
            play_item.setProperty("IsPlayable", "true")
            play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
            play_item.setMimeType('application/vnd.apple.mpegstream_url')
            play_item.setContentLookup(False)
            play_item.setProperty(
                'inputstream.adaptive.stream_headers', headers_play)
            xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
            return True
        if 'telerium.tv/embed/' in data:
            srcs = re.findall('iframe.*?src\s*=\s*\"(.*?telerium.tv\/embed\/.*?)\".*?\/iframe', data, re.I)
            if len(srcs) > 0:
                import telerium
                telerium.resolver(srcs[0],referer=referer)
                return True
        if '://embed.telerium.tv/embed.js' in data:
            srcs = re.findall('script.*?id=\"(\d*)\"', data, re.I)
            if len(srcs) > 0:
                import telerium
                telerium.resolver('https://telerium.tv/embed/' + srcs[0] + '.html',referer=referer)
                return True
    except:
        pass
    dialog = xbmcgui.Dialog()
    dialog.notification('FusionOrg', 'Fallo en: ' +
                        url, xbmcgui.NOTIFICATION_INFO, 5000, True)
    xbmc.sleep(1000)
    exit()
