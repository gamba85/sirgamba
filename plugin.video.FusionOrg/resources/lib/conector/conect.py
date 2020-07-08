# -*- coding: utf-8 -*-
import base64
import os
import pickle

import requests
import xbmc
import xbmcaddon
import xbmcgui


addonInfo = xbmcaddon.Addon().getAddonInfo
headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
addon = xbmcaddon.Addon()
addon_data_dir = xbmc.translatePath(xbmc.translatePath(
    addon.getAddonInfo('profile')).decode('utf-8'))
cookies_path = os.path.join(addon_data_dir, 'cooforg.jar')
dialog = xbmcgui.Dialog()


def get_url(url, m='get', p='', h=headers, r=True, c='', params=''):
    response = 'Imposible conectar con el server'
    if 'fusionorg.net' in url:
        headers['User-Agent'] = 'FusionOrgByTeamFusion/1.0'
    if m == 'get' or m == '':
        try:
            if c == '':
                response = requests.get(
                    url, headers=h, timeout=10, allow_redirects=r, params=params)
            else:
                response = requests.get(
                    url, headers=h, timeout=10, allow_redirects=r, cookies=c, params=params)
        except:
            pass
    if m == 'post':
        try:
            if c == '':
                response = requests.post(
                    url, headers=h, data=p, timeout=10, allow_redirects=r, params=params)
            else:
                response = requests.post(
                    url, headers=h, data=p, timeout=10, allow_redirects=r, cookies=c, params=params)
        except:
            pass

    return response


def get_url_dcl(url, m='get', p='', h=headers, r=True, c=''):
    if 'fusionorg.net' in url:
        headers['User-Agent'] = 'FusionOrgByTeamFusion/1.0'
    response = get_url(url, m=m, p=p, h=headers, r=r, c=c)
    if response == 'Imposible conectar con el server':
        response = get_url(url, m=m, p=p, h=headers, r=r, c=c)
    if response == 'Imposible conectar con el server':
        dialog.notification('FusionOrg', 'Fallo al contactar con el servidor',
                            xbmcgui.NOTIFICATION_INFO, 5000, False)
        exit()
    data = response.content
    cookies = response.cookies
    location = response.headers.get('location')

    return data, cookies, location


def get_url_d(url, m='get', p='', h=headers, r=True, c=''):
    if 'fusionorg.net' in url:
        headers['User-Agent'] = 'FusionOrgByTeamFusion/1.0'
    response = get_url(url, m=m, p=p, h=headers, r=r, c=c)
    if response == 'Imposible conectar con el server':
        response = get_url(url, m=m, p=p, h=headers, r=r, c=c)
    if response == 'Imposible conectar con el server':
        dialog.notification('FusionOrg', 'Fallo al contactar con el servidor',
                            xbmcgui.NOTIFICATION_INFO, 5000, False)
        exit()
    data = response.content

    return data


def get_url_dc(url, m='get', p='', h=headers, r=True, c=''):
    if 'fusionorg.net' in url:
        headers['User-Agent'] = 'FusionOrgByTeamFusion/1.0'
    response = get_url(url, m=m, p=p, h=headers, r=r, c=c)
    if response == 'Imposible conectar con el server':
        response = get_url(url, m=m, p=p, h=headers, r=r, c=c)
    if response == 'Imposible conectar con el server':
        dialog.notification('FusionOrg', 'Fallo al contactar con el servidor',
                            xbmcgui.NOTIFICATION_INFO, 5000, False)
        exit()
    data = response.content
    cookies = response.cookies

    return data, cookies, location


def save_cookies(cookies):
    with open(cookies_path, 'wb') as f:
        pickle.dump(cookies, f)


def load_cookies():
    try:
        if os.path.isfile(cookies_path):
            with open(cookies_path, 'rb') as f:
                return pickle.load(f)
    except:
        pass
    return ''


def clean_cookies(cookies):
    with open(cookies_path, 'wb') as f:
        f.write('')


def post_link_died(server='', tmdbid='', id='', url=''):
    if (server != '' and (id != '' or url != '')):
        headers['User-Agent'] = 'FusionOrgByTeamFusion/1.0'
        dead = {}
        dead[base64.b64encode('server')] = base64.b64encode(server)
        dead[base64.b64encode('tmdbid')] = base64.b64encode(tmdbid)
        dead[base64.b64encode('id')] = base64.b64encode(id)
        dead[base64.b64encode('url')] = base64.b64encode(url)
        url = 'https://fusionorg.net/tools/mtto_gral_json/report_dead/report.php'
        response = get_url(url, m='post', p=dead, h=headers)
        if response == 'Imposible conectar con el server':
            response = get_url(url, m='post', p=dead, h=headers)
