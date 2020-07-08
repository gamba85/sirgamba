# coding=utf-8
import base64
import cookielib
import json
import os
import os.path
import re
import sqlite3
import sys
import time
import urllib
import urllib2
import urlparse

import requests

import control
import navigator
from resources.lib.conector import conect
from resources.lib.vtt2srt import vtt2srt
from servers import *
import urlresolver
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])

addon = xbmcaddon.Addon()
addon_dir = xbmc.translatePath(xbmc.translatePath(
    addon.getAddonInfo('Path')).decode('utf-8'))
addon_data_dir = xbmc.translatePath(xbmc.translatePath(
    addon.getAddonInfo('profile')).decode('utf-8'))

if not os.path.exists(addon_data_dir):
    os.makedirs(addon_data_dir)

addonname = addon.getAddonInfo('name')
username = addon.getSetting('username')
password = addon.getSetting('password')
#=========================================================================
# language = addon.getSetting('language')
#=========================================================================

language = 'Latino'

args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)


def mensaje(mensaje):
    xbmcgui.Dialog().ok(addonname, mensaje)


def build_url(query):
    if query == {'mode': 'request'}:
        return 'plugin://plugin.video.FusionTv.Request/'
    if query == {'mode': 'loguploader'}:
        return 'plugin://script.kodi.loguploader/'

    return base_url + '?' + urllib.urlencode(query)


def addMenuitem(url, li, folder):
    return xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=folder)


def endMenu():
    xbmcplugin.endOfDirectory(addon_handle)


def Directorios():
    addon_data = xbmc.translatePath(
        "special://userdata/addon_data/plugin.video.FusionOrg")
    try:
        os.stat(addon_data)
    except:
        os.mkdir(addon_data)

    dir_downloads = addon_data + '/descargas'
    try:
        os.stat(dir_downloads)
    except:
        os.mkdir(dir_downloads)
    masterlistLocal = open(addon_data + '/masterlist.json', 'a')
    masterlistLocal.close()


def menuppal(categorias, infos, fanarts, modes, posters):
    xbmcplugin.setContent(addon_handle, 'albums')
    xbmcplugin.setPluginCategory(addon_handle, 'Menu')
    for categoria, info, fanart, mode, poster in zip(categorias, infos, fanarts, modes, posters):
        url = build_url({'mode': mode})
        li = xbmcgui.ListItem('[COLOR white][B]' + categoria + '[/B][/COLOR]')
        li.setInfo("video", {"Plot": info})
        li.setArt({'fanart': fanart, 'poster': poster})
        addMenuitem(url, li, True)
    endMenu()


def menucategoriasmovies(categorias, infos, fanarts, modes, posters, archivos):
    xbmcplugin.setContent(addon_handle, 'albums')
    xbmcplugin.setPluginCategory(addon_handle, 'Categorias')
    serial = 'aHR0cDovL2Z1c2lvbm9yZy5uZXQvY2F0ZWdvcmllcy9tb3ZpZXMv'
    serial = base64.b64decode(serial)
    add_search_item()
    for categoria, info, fanart, mode, poster, archivo in zip(categorias, infos, fanarts, modes, posters, archivos):
        url = build_url({'mode': mode, 'direccion': serial +
                         archivo + '.php', 'categoria': categoria})
        li = xbmcgui.ListItem('[COLOR white][B]' + categoria + '[/B][/COLOR]')
        li.setInfo("video", {"Plot": info})
        li.setArt({'fanart': fanart, 'poster': poster})
        addMenuitem(url, li, True)
    endMenu()


def menucategoriastvshows(categorias, infos, fanarts, modes, posters, tags):
    xbmcplugin.setContent(addon_handle, 'albums')
    xbmcplugin.setPluginCategory(addon_handle, 'Categorias')
    serial = 'aHR0cDovL2Z1c2lvbm9yZy5uZXQvdHZzaG93cy9sYXRpbm8vaW5kZXgucGhwP3RhZz0='
    serial = base64.b64decode(serial)
    add_search_item()
    for categoria, info, fanart, mode, poster, tags in zip(categorias, infos, fanarts, modes, posters, tags):
        url = build_url({'mode': mode, 'direccion': serial +
                         tags, 'categoria': categoria})
        li = xbmcgui.ListItem('[COLOR white][B]' + categoria + '[/B][/COLOR]')
        li.setInfo("video", {"Plot": info})
        li.setArt({'fanart': fanart, 'poster': poster})
        addMenuitem(url, li, True)
    endMenu()


def movieslist(web, mode, categoria):
    xbmcplugin.setContent(addon_handle, 'movies')
    xbmcplugin.setPluginCategory(addon_handle, categoria.title())
    data = conect.get_url_d(web)
    matches = re.findall('<ppal(.*?)<\/ppal', data, re.MULTILINE)
    path_db = control.db_path()
    if path_db != '':
        try:
            conn = sqlite3.connect(path_db)
            cursor = conn.cursor()
            sql_con = True
        except:
            sql_con = False

    add_search_item()
    for match in matches:
        try:
            title = re.findall('titulo.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
            title = base64.b64decode(title)
        except:
            try:
                title = re.findall('title.*?lue=(.*?)\/>',
                                   match, re.MULTILINE)[0]
                title = base64.b64decode(title)
            except:
                title = 'Sin Titulo (reportar video)'

        poster = re.findall('thumb.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        poster = base64.b64decode(poster)
        fanart = re.findall('fanart.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        fanart = base64.b64decode(fanart)
        post_img_qy = addon.getSetting('pos_qy').replace(' px', '')
        if post_img_qy != 'Mejor':
            poster = poster.replace('/original/', '/w' + post_img_qy + '/')
        fan_img_qy = addon.getSetting('fan_qy').replace(' px', '')
        if fan_img_qy != 'Mejor':
            fanart = fanart.replace('/original/', '/w' + fan_img_qy + '/')
        sinopsis = re.findall('info.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        link = re.findall('link.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        link = base64.b64decode(link)
        year = re.findall('id=.year.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        yeari = int(base64.b64decode(year))
        years = base64.b64decode(year)
        tmdbid = re.findall('tmdbid.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        tmdbid = base64.b64decode(tmdbid)

        url = build_url({'mode': mode, 'foldername': title, 'direccion': link, 'thumbnail': poster,
                         'fanart': fanart, 'info': sinopsis, 'year': years, 'tmdbid': tmdbid})
        video = {"Title": title, "Plot": sinopsis, "MediaType": "Movie",
                 "OriginalTitle": title, "SortTitle": title}
        li = xbmcgui.ListItem(iconImage=poster, thumbnailImage=poster)
        li.setProperty('IsPlayable', 'False')
        if sql_con:
            query = "SELECT * FROM files WHERE strFilename LIKE '%FusionOrg%tmdbid=" + \
                tmdbid + "%' AND strFilename NOT LIKE '%season%episode%' AND playCount > 0"
            result = cursor.execute(query)
            result = cursor.fetchall()
            if len(result) > 0:
                video["playcount"] = int(len(result))
        video["year"] = yeari
        li.setArt({'fanart': fanart, 'poster': poster})
        li.setProperty('fanart_image', fanart)
        if years == '0' or years == '0000':
            title = '[COLOR white][B]' + title + '[/B][/COLOR]'
        else:
            title = '[COLOR white][B]' + title + \
                '[/B][/COLOR]  [COLOR blue][B](' + years + ')[/B][/COLOR]'
        li.setLabel(title)
        li.setLabel2(title)
        li.setInfo('video', video)
        addMenuitem(url, li, True)
    if sql_con:
        cursor.close()
    endMenu()


def movieslistyear(web, mode, categoria):
    xbmcplugin.setContent(addon_handle, 'albums')
    xbmcplugin.setPluginCategory(addon_handle, categoria.title())
    dir_pos_pel = os.path.join(
        get_dir_addon(), 'resources', 'media', 'peliculas', 'poster')
    poster = os.path.join(dir_pos_pel, 'year.png')
    dir_fan_pel = os.path.join(
        get_dir_addon(), 'resources', 'media', 'peliculas', 'fanart')
    fanart = os.path.join(dir_fan_pel, 'fanart.png')
    data = conect.get_url_d(web)
    matches = re.findall('<ppal(.*?)<\/ppal', data, re.MULTILINE)
    add_search_item()
    for match in matches:
        try:
            title = re.findall('titulo.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
            title = base64.b64decode(title)
        except:
            try:
                title = re.findall('title.*?lue=(.*?)\/>',
                                   match, re.MULTILINE)[0]
                title = base64.b64decode(title)
            except:
                title = 'Sin Titulo (reportar video)'

        sinopsis = re.findall('info.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        link = re.findall('link.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        link = base64.b64decode(link)
        year = re.findall('id=.year.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        yeari = int(base64.b64decode(year))
        years = base64.b64decode(year)

        url = build_url({'mode': mode, 'foldername': title, 'direccion': link, 'thumbnail': poster,
                         'fanart': fanart, 'info': sinopsis, 'year': years, 'categoria': years})
        li = xbmcgui.ListItem(iconImage=poster, thumbnailImage=poster)
        if yeari == 0:
            li.setInfo("video", {"Title": title, "Plot": sinopsis,
                                 "MediaType": "Movie", "OriginalTitle": title, "SortTitle": title})
        else:
            li.setInfo("video", {"Title": title, "Plot": sinopsis, "Year": yeari,
                                 "MediaType": "Movie", "OriginalTitle": title, "SortTitle": title})
        li.setArt({'fanart': fanart, 'poster': poster})
        li.setProperty('fanart_image', fanart)
        if years == '0' or years == '0000':
            title = '[COLOR white][B]' + title + '[/B][/COLOR]'
        else:
            title = '[COLOR white][B]' + title + \
                '[/B][/COLOR]  [COLOR blue][B](' + years + ')[/B][/COLOR]'
        li.setLabel(title)
        li.setLabel2(title)
        addMenuitem(url, li, True)
    endMenu()


def tvshowslist(web, mode, categoria):
    xbmcplugin.setContent(addon_handle, 'tvshows')
    xbmcplugin.setPluginCategory(addon_handle, categoria.title())
    data = conect.get_url_d(web)
    matches = re.findall('<ppal>(.*?)<\/ppal', data, re.MULTILINE)
    add_search_item()
    for match in matches:
        title = re.findall('titulo.*?value=(.*?)\/>', match, re.MULTILINE)[0]
        sinopsis = re.findall('info.*?value=(.*?)\/>', match, re.MULTILINE)[0]
        link = re.findall('link.*?value=(.*?)\/>', match, re.MULTILINE)[0]
        thumbnail = re.findall(
            'thumbnail.*?value=(.*?)\/>', match, re.MULTILINE)[0]
        fanart = re.findall('fanart.*?value=(.*?)\/>', match, re.MULTILINE)[0]
        post_img_qy = addon.getSetting('pos_qy').replace(' px', '')
        if post_img_qy != 'Mejor':
            thumbnail = thumbnail.replace('/original/', '/w' + post_img_qy + '/')
        fan_img_qy = addon.getSetting('fan_qy').replace(' px', '')
        if fan_img_qy != 'Mejor':
            fanart = fanart.replace('/original/', '/w' + fan_img_qy + '/')
        tmdbid = re.findall('tmdbid.*?value=(.*?)\/>', match, re.MULTILINE)[0]

        url = build_url({'mode': mode, 'direccion': link, 'fanart': fanart,
                         'info': sinopsis, 'tmdbid': tmdbid, 'serie': title})
        li = xbmcgui.ListItem(title, iconImage=thumbnail,
                              thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "Plot": sinopsis})
        li.setArt({'fanart': fanart, 'poster': thumbnail})
        li.setProperty('fanart_image', fanart)
        li.setLabel('[COLOR white][B]' + title + '[/B][/COLOR]')
        li.setProperty('IsPlayable', 'False')
        addMenuitem(url, li, True)
    endMenu()


def seasonlist(web, fanart, sinopsis, mode, tmdbid, serie):
    xbmcplugin.setContent(addon_handle, 'seasons')
    xbmcplugin.setPluginCategory(addon_handle, serie.title())
    data = conect.get_url_d(web)
    matches = re.findall('<season>(.*?)<\/season', data, re.MULTILINE)
    add_search_item()
    for match in matches:
        title = re.findall('temporada.*?value=(.*?)\/>',
                           match, re.MULTILINE)[0]
        title = title.replace('Temporada', 'Temporada ')
        sinopsis = sinopsis
        link = re.findall('link.*?value=(.*?)\/>', match, re.MULTILINE)[0]
        thumbnail = re.findall('poster.*?value=(.*?)\/>',
                               match, re.MULTILINE)[0]
        fanart = fanart
        post_img_qy = addon.getSetting('pos_qy').replace(' px', '')
        if post_img_qy != 'Mejor':
            thumbnail = thumbnail.replace('/original/', '/w' + post_img_qy + '/')
        fan_img_qy = addon.getSetting('fan_qy').replace(' px', '')
        if fan_img_qy != 'Mejor':
            fanart = fanart.replace('/original/', '/w' + fan_img_qy + '/')

        url = build_url({'mode': mode, 'direccion': link,
                         'tmdbid': tmdbid, 'serie': serie})
        li = xbmcgui.ListItem(title, iconImage=thumbnail,
                              thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "Plot": sinopsis})
        li.setArt({'fanart': fanart, 'poster': thumbnail})
        li.setProperty('fanart_image', fanart)
        li.setLabel('[COLOR white][B]' + title + '[/B][/COLOR]')
        li.setProperty('IsPlayable', 'False')
        addMenuitem(url, li, True)
    endMenu()


def episodeslist(web, mode, tmdbid, serie):
    xbmcplugin.setContent(addon_handle, 'episodes')
    xbmcplugin.setPluginCategory(addon_handle, serie.title())
    data = conect.get_url_d(web)
    matches = re.findall('<episodio>(.*?)<\/episodio', data, re.IGNORECASE)
    path_db = control.db_path()
    add_search_item()
    if path_db != '':
        try:
            conn = sqlite3.connect(path_db)
            cursor = conn.cursor()
            sql_con = True
        except:
            sql_con = False
    for match in matches:
        title = re.findall('title.*?value=(.*?)\/>', match, re.MULTILINE)[0]
        sinopsis = re.findall('sinopsis.*?value=(.*?)\/>',
                              match, re.MULTILINE)[0]
        link = re.findall('link.*?value=(.*?)\/>', match, re.MULTILINE)[0]
        thumbnail = re.findall(
            'thumbnail.*?value=(.*?)\/>', match, re.MULTILINE)[0]
        fanart = re.findall('fanart.*?value=(.*?)\/>', match, re.MULTILINE)[0]
        post_img_qy = addon.getSetting('pos_qy').replace(' px', '')
        if post_img_qy != 'Mejor':
            thumbnail = thumbnail.replace('/original/', '/w' + post_img_qy + '/')
        fan_img_qy = addon.getSetting('fan_qy').replace(' px', '')
        if fan_img_qy != 'Mejor':
            fanart = fanart.replace('/original/', '/w' + fan_img_qy + '/')
        season = int(re.findall('S(.*?)E.*?', title)[0])
        episode = int(re.findall('.*?E(.*?)-', title)[0])
        url = build_url({'mode': mode, 'direccion': link, 'tmdbid': tmdbid,
                         "episode": episode, "season": season, "serie": serie})
        li = xbmcgui.ListItem(iconImage=thumbnail, thumbnailImage=thumbnail)
        video = {"Title": title, "Plot": sinopsis, "MediaType": "episode",
                 "OriginalTitle": title, "SortTitle": title}
        if sql_con:
            query = "SELECT * FROM files WHERE strFilename LIKE '%FusionOrg%tmdbid=" + tmdbid + \
                "%season=" + str(season) + "%episode=" + \
                str(episode) + "%' AND playCount > 0"
            result = cursor.execute(query)
            result = cursor.fetchall()
            if len(result) > 0:
                video["playcount"] = int(len(result))
        li.setInfo("video", video)
        li.setProperty('fanart_image', fanart)
        li.setArt({'fanart': fanart, 'poster': thumbnail})
        li.setLabel('[COLOR white][B]' + title + '[/B][/COLOR]')
        li.setProperty('IsPlayable', 'False')
        addMenuitem(url, li, True)
    if sql_con:
        cursor.close()
    endMenu()


def servidores(titulo, thumbnail, fanart, sinopsis, url):
    xbmcplugin.setContent(addon_handle, 'movies')
    try:
        titulo = titulo.decode('utf-8')
    except:
        try:
            titulo = titulo.encode('utf-8')
        except:
            pass
    xbmcplugin.setPluginCategory(addon_handle, titulo.title())
    html = conect.get_url_d(url)
    items = re.findall("<ppal>(.*?)<\/ppal>", html, re.MULTILINE)
    trailer = re.findall(
        "trailer.*?value=(.*?)\/\>\<\/trailer", html, re.MULTILINE)[0]
    trailer = base64.b64decode(trailer)
    add_search_item()
    if trailer != 'novideo':
        titletrailer = '[COLOR orange][B]Trailer:[/B][/COLOR] [COLOR white][B]' + \
            titulo + '[/B][/COLOR]'
        url = build_url({'mode': 'play', 'playlink': trailer, 'tmdbid': '0'})
        li = xbmcgui.ListItem(
            titletrailer, iconImage=thumbnail, thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": titletrailer, "Plot": sinopsis})
        li.setArt({'fanart': fanart, 'poster': thumbnail})
        li.setProperty('IsPlayable', 'true')
        li.setProperty('fanart_image', fanart)
        addMenuitem(url, li, False)
    tmdbid = re.findall("tmdbid.*?value=(.*?)\/\>\<\/tmdbid",
                        html, re.MULTILINE)[0]
    tmdbid = base64.b64decode(tmdbid)
    year = re.findall("year.*?value=(.*?)\/\>\<\/year", html, re.MULTILINE)[0]
    year = base64.b64decode(year)
    for item in items:
        url = re.findall('link.*?value=(.*?)\/\>\<\/br\>',
                         item, re.IGNORECASE)[0]
        url = base64.b64decode(url)
        if url != '':
            servidores3(url, titulo, thumbnail, fanart, sinopsis,
                        tmdbid, year, season='', episode='')
    endMenu()


def servidores2(web, tmdbid, season, episode, serie):
    xbmcplugin.setContent(addon_handle, 'episodes')
    xbmcplugin.setPluginCategory(addon_handle, serie.title())
    data = conect.get_url_d(web)
    matches = re.findall('<episodio>(.*?)<\/episodio', data, re.MULTILINE)
    name = re.findall('title.*?value=(.*?)\/>', data, re.MULTILINE)[0]
    try:
        name = name.decode('utf-8')
    except:
        try:
            name = name.encode('utf-8')
        except:
            pass
    sinopsis = re.findall('sinopsis.*?value=(.*?)\/>',
                          data, re.MULTILINE)[0]
    thumbnail = re.findall(
        'thumbnail.*?value=(.*?)\/>', data, re.MULTILINE)[0]
    fanart = re.findall('fanart.*?value=(.*?)\/>', data, re.MULTILINE)[0]
    post_img_qy = addon.getSetting('pos_qy').replace(' px', '')
    if post_img_qy != 'Mejor':
        thumbnail = thumbnail.replace('/original/', '/w' + post_img_qy + '/')
    fan_img_qy = addon.getSetting('fan_qy').replace(' px', '')
    if fan_img_qy != 'Mejor':
        fanart = fanart.replace('/original/', '/w' + fan_img_qy + '/')
    add_search_item()
    for match in matches:
        url = re.findall('link.*?value=(.*?)\/>', match, re.MULTILINE)[0]
        if url != '':
            servidores3(url, name, thumbnail, fanart, sinopsis,
                        tmdbid, '', season, episode, serie)
    endMenu()


def servidores3(url, titulo, thumbnail, fanart, sinopsis, tmdbid, year='', season='', episode='', serie=''):
    media_subtitles = []
    video_info = {}
    video_info['Title'] = titulo
    video_info['Plot'] = sinopsis
    video_info['mediatype'] = 'movie'
    art_info = {'fanart': fanart, 'poster': thumbnail,
                'thumb': thumbnail, 'landscape': fanart, 'icon': thumbnail}
    if year != '':
        video_info['Year'] = year
    if season != '':
        video_info['Season'] = season
        video_info['mediatype'] = 'season'
    if episode != '':
        video_info['Episode'] = episode
        video_info['mediatype'] = 'episode'
        art_info['clearlogo'] = thumbnail
    if serie != '':
        video_info['tvshowtitle'] = serie

    if 'drive.google.com' in url:
        from base.servers import gvideo
        try:
            calidades = gvideo.google_calidades(url)
            for calidad in calidades:
                video_info['Title'] = '[COLOR orange][B][Gvideo=' + calidad + \
                    '][/B][/COLOR] [COLOR white][B]' + titulo + '[/B][/COLOR]'
                if year != '':
                    video_info['Title'] = video_info['Title'] + \
                        ' [COLOR blue][B](' + year + ')[/B][/COLOR]'
                if season != '' and episode != '':
                    url2 = build_url({'mode': 'play', 'playlink': url + '&q=' + calidad,
                                      'tmdbid': tmdbid, 'season': season, 'episode': episode})
                else:
                    url2 = build_url(
                        {'mode': 'play', 'playlink': url + '&q=' + calidad, 'tmdbid': tmdbid})
                li = xbmcgui.ListItem(
                    video_info['Title'], iconImage=thumbnail, thumbnailImage=thumbnail)
                li.setInfo("video", video_info)
                li.setProperty('IsPlayable', 'true')
                li.setProperty('fanart_image', fanart)
                li.setIconImage(thumbnail)
                li.setArt(art_info)
                addMenuitem(url2, li, False)
        except:
            pass

    elif 'clipwatching.com' in url:
        calidades = calidadesclipwatching(url)
        if calidades != 'dead':
            for calidad in calidades:
                video_info['Title'] = '[COLOR orange][B][Clipwatching=' + calidad + \
                    '][/B][/COLOR] [COLOR white][B]' + titulo + '[/B][/COLOR]'
                if year != '':
                    video_info['Title'] = video_info['Title'] + \
                        ' [COLOR blue][B](' + year + ')[/B][/COLOR]'
                if season != '' and episode != '':
                    url2 = build_url({'mode': 'play', 'playlink': url + '&calidad=' + calidad,
                                      'tmdbid': tmdbid, 'season': season, 'episode': episode})
                else:
                    url2 = build_url(
                        {'mode': 'play', 'playlink': url + '&calidad=' + calidad, 'tmdbid': tmdbid})
                li = xbmcgui.ListItem(
                    video_info['Title'], iconImage=thumbnail, thumbnailImage=thumbnail)
                li.setInfo("video", video_info)
                li.setProperty('IsPlayable', 'true')
                li.setProperty('fanart_image', fanart)
                li.setArt(art_info)
                addMenuitem(url2, li, False)

    elif 'gamovideo.com' in url:
        video_info['Title'] = '[COLOR orange][B][Gamovideo][/B][/COLOR] [COLOR white][B]' + \
            titulo + '[/B][/COLOR]'
        if year != '':
            video_info['Title'] = video_info['Title'] + \
                ' [COLOR blue][B](' + year + ')[/B][/COLOR]'
        if season != '' and episode != '':
            url = build_url({'mode': 'play', 'playlink': url,
                             'tmdbid': tmdbid, 'season': season, 'episode': episode})
        else:
            url = build_url(
                {'mode': 'play', 'playlink': url, 'tmdbid': tmdbid})
        li = xbmcgui.ListItem(
            video_info['Title'], iconImage=thumbnail, thumbnailImage=thumbnail)
        li.setInfo("video", video_info)
        li.setProperty('IsPlayable', 'true')
        li.setProperty('fanart_image', fanart)
        li.setIconImage(thumbnail)
        li.setArt(art_info)
        addMenuitem(url, li, False)

    elif 'uptobox.com' in url or 'uptostream.com' in url:
        servers, media_subtitles = uptoboxtest(
            url, tmdbid + 'S' + season + 'E' + episode)
        if len(servers) > 0:
            for server in servers:
                if server == 'uptostream':
                    for calidad in servers['uptostream']:
                        video_info['Title'] = '[COLOR orange][B]' + servers['uptostream'][calidad][0] + \
                            '[/B][/COLOR] [COLOR white][B]' + \
                            titulo + '[/B][/COLOR]'
                        if year != '':
                            video_info['Title'] = video_info['Title'] + \
                                ' [COLOR blue][B](' + year + ')[/B][/COLOR]'
                        if season != '' and episode != '':
                            url = build_url(
                                {'mode': 'play', 'playlink': servers['uptostream'][calidad][1], 'tmdbid': tmdbid, 'season': season, 'episode': episode})
                        else:
                            url = build_url(
                                {'mode': 'play', 'playlink': servers['uptostream'][calidad][1], 'tmdbid': tmdbid})
                        li = xbmcgui.ListItem(
                            video_info['Title'], iconImage=thumbnail, thumbnailImage=thumbnail)
                        li.setInfo("video", video_info)
                        li.setProperty('IsPlayable', 'true')
                        li.setProperty('fanart_image', fanart)
                        li.setArt(art_info)
                        addMenuitem(url, li, False)

                if server == 'uptobox':
                    for calidad in servers['uptobox']:
                        video_info['Title'] = '[COLOR orange][B]' + servers['uptobox'][calidad][0] + \
                            '[/B][/COLOR] [COLOR white][B]' + \
                            titulo + '[/B][/COLOR]'
                        if year != '':
                            video_info['Title'] = video_info['Title'] + \
                                ' [COLOR blue][B](' + year + ')[/B][/COLOR]'
                        if season != '' and episode != '':
                            url = build_url(
                                {'mode': 'play', 'playlink': servers['uptobox'][calidad][1], 'tmdbid': tmdbid, 'season': season, 'episode': episode})
                        else:
                            url = build_url(
                                {'mode': 'play', 'playlink': servers['uptobox'][calidad][1], 'tmdbid': tmdbid})
                        li = xbmcgui.ListItem(
                            video_info['Title'], iconImage=thumbnail, thumbnailImage=thumbnail)
                        li.setInfo("video", video_info)
                        li.setProperty('IsPlayable', 'true')
                        li.setProperty('fanart_image', fanart)
                        li.setArt(art_info)
                        addMenuitem(url, li, False)

    elif 'tune.pk' in url:
        echo, calidades = tunepk(url)
        if echo and len(calidades) > 0:
            for calidad in calidades:
                video_info['Title'] = '[COLOR orange][B][Tune.pk=' + calidad + 'p][/B][/COLOR] [COLOR white][B]' + \
                    titulo + '[/B][/COLOR]'
                if year != '':
                    video_info['Title'] = video_info['Title'] + \
                        ' [COLOR blue][B](' + year + ')[/B][/COLOR]'
                if season != '' and episode != '':
                    url2 = build_url({'mode': 'play', 'playlink': url + '&calidad=' + calidad,
                                      'tmdbid': tmdbid, 'season': season, 'episode': episode})
                else:
                    url2 = build_url(
                        {'mode': 'play', 'playlink': url + '&calidad=' + calidad, 'tmdbid': tmdbid})
                li = xbmcgui.ListItem(
                    video_info['Title'], iconImage=thumbnail, thumbnailImage=thumbnail)
                li.setInfo("video", video_info)
                li.setProperty('IsPlayable', 'true')
                li.setProperty('fanart_image', fanart)
                li.setArt(art_info)
                addMenuitem(url2, li, False)

    elif 'gounlimited' in url or 'tazmovies' in url:
        echo, calidades, media_subtitles = gounlimited(url)
        if echo and len(calidades) > 0:
            for calidad in calidades:
                video_info['Title'] = '[COLOR orange][B][Gounlimited=' + calidad + 'p][/B][/COLOR] [COLOR white][B]' + \
                    titulo + '[/B][/COLOR]'
                if year != '':
                    video_info['Title'] = video_info['Title'] + \
                        ' [COLOR blue][B](' + year + ')[/B][/COLOR]'
                if season != '' and episode != '':
                    url2 = build_url({'mode': 'play', 'playlink': url + '&calidad=' + calidad,
                                      'tmdbid': tmdbid, 'season': season, 'episode': episode})
                else:
                    url2 = build_url(
                        {'mode': 'play', 'playlink': url + '&calidad=' + calidad, 'tmdbid': tmdbid})
                li = xbmcgui.ListItem(
                    video_info['Title'], iconImage=thumbnail, thumbnailImage=thumbnail)
                li.setInfo("video", video_info)
                li.setProperty('IsPlayable', 'true')
                li.setProperty('fanart_image', fanart)
                li.setArt(art_info)
                addMenuitem(url2, li, False)

    elif 'fembed' in url or 'feurl.com' in url:
        calidades = calidadesfembed(url)
        if calidades != 'dead':
            for calidad in calidades:
                video_info['Title'] = '[COLOR orange][B][Fembed=' + calidad + \
                    '][/B][/COLOR] [COLOR white][B]' + titulo + '[/B][/COLOR]'
                if year != '':
                    video_info['Title'] = video_info['Title'] + \
                        ' [COLOR blue][B](' + year + ')[/B][/COLOR]'
                if season != '' and episode != '':
                    url2 = build_url({'mode': 'play', 'playlink': url + '&calidad=' + calidad,
                                      'tmdbid': tmdbid, 'season': season, 'episode': episode})
                else:
                    url2 = build_url(
                        {'mode': 'play', 'playlink': url + '&calidad=' + calidad, 'tmdbid': tmdbid})
                li = xbmcgui.ListItem(
                    video_info['Title'], iconImage=thumbnail, thumbnailImage=thumbnail)
                li.setInfo("video", video_info)
                li.setProperty('IsPlayable', 'true')
                li.setProperty('fanart_image', fanart)
                li.setArt(art_info)
                addMenuitem(url2, li, False)

    elif 'uqload.com' in url:
        calidades = calidadesuqload(url)
        if calidades:
            video_info['Title'] = '[COLOR orange][B][Uqload][/B][/COLOR] [COLOR white][B]' + \
                titulo + '[/B][/COLOR]'
            if year != '':
                video_info['Title'] = video_info['Title'] + \
                    ' [COLOR blue][B](' + year + ')[/B][/COLOR]'
            if season != '' and episode != '':
                url2 = build_url({'mode': 'play', 'playlink': url,
                                  'tmdbid': tmdbid, 'season': season, 'episode': episode})
            else:
                url2 = build_url(
                    {'mode': 'play', 'playlink': url, 'tmdbid': tmdbid})
            li = xbmcgui.ListItem(
                video_info['Title'], iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", video_info)
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            li.setArt(art_info)
            addMenuitem(url2, li, False)

    elif 'ok.ru' in url or 'odnoklassniki.ru' in url:
        echo, calidades = calidadesokru(url)
        if echo and len(calidades) > 0:
            for calidad in calidades:
                video_info['Title'] = '[COLOR orange][B][Ok.ru=' + calidad + '][/B][/COLOR] [COLOR white][B]' + \
                    titulo + '[/B][/COLOR]'
                if year != '':
                    video_info['Title'] = video_info['Title'] + \
                        ' [COLOR blue][B](' + year + ')[/B][/COLOR]'
                if season != '' and episode != '':
                    url2 = build_url({'mode': 'play', 'playlink': url + '&calidad=' + calidad,
                                      'tmdbid': tmdbid, 'season': season, 'episode': episode})
                else:
                    url2 = build_url(
                        {'mode': 'play', 'playlink': url + '&calidad=' + calidad, 'tmdbid': tmdbid})
                li = xbmcgui.ListItem(
                    video_info['Title'], iconImage=thumbnail, thumbnailImage=thumbnail)
                li.setInfo("video", video_info)
                li.setProperty('IsPlayable', 'true')
                li.setProperty('fanart_image', fanart)
                li.setArt(art_info)
                addMenuitem(url2, li, False)

    elif 'upstream.to' in url:
        online = calidadesupstream(url)
        if online:
            video_info['Title'] = '[COLOR orange][B][UpStream][/B][/COLOR] [COLOR white][B]' + \
                titulo + '[/B][/COLOR]'
            if year != '':
                video_info['Title'] = video_info['Title'] + \
                    ' [COLOR blue][B](' + year + ')[/B][/COLOR]'
            if season != '' and episode != '':
                url2 = build_url({'mode': 'play', 'playlink': url,
                                  'tmdbid': tmdbid, 'season': season, 'episode': episode})
            else:
                url2 = build_url(
                    {'mode': 'play', 'playlink': url, 'tmdbid': tmdbid})
            li = xbmcgui.ListItem(
                video_info['Title'], iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", video_info)
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            li.setArt(art_info)
            addMenuitem(url2, li, False)

    elif 'mixdrop' in url:
        calidades = calidadesmixdrop(url)
        for calidad in calidades:
            video_info['Title'] = '[COLOR orange][B][' + calidad + '][/B][/COLOR] [COLOR white][B]' + \
                titulo + '[/B][/COLOR]'
            if year != '':
                video_info['Title'] = video_info['Title'] + \
                    ' [COLOR blue][B](' + year + ')[/B][/COLOR]'
            if season != '' and episode != '':
                url2 = build_url({'mode': 'play', 'playlink': url,
                                  'tmdbid': tmdbid, 'season': season, 'episode': episode})
            else:
                url2 = build_url(
                    {'mode': 'play', 'playlink': url, 'tmdbid': tmdbid})
            li = xbmcgui.ListItem(
                video_info['Title'], iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", video_info)
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            li.setArt(art_info)
            addMenuitem(url2, li, False)

    elif 'vup.to' in url:
        calidades = calidadesvup(url)
        for calidad in calidades:
            video_info['Title'] = '[COLOR orange][B][' + calidad + '][/B][/COLOR] [COLOR white][B]' + \
                titulo + '[/B][/COLOR]'
            if year != '':
                video_info['Title'] = video_info['Title'] + \
                    ' [COLOR blue][B](' + year + ')[/B][/COLOR]'
            if season != '' and episode != '':
                url2 = build_url({'mode': 'play', 'playlink': url,
                                  'tmdbid': tmdbid, 'season': season, 'episode': episode})
            else:
                url2 = build_url(
                    {'mode': 'play', 'playlink': url, 'tmdbid': tmdbid})
            li = xbmcgui.ListItem(
                video_info['Title'], iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", video_info)
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            li.setArt(art_info)
            addMenuitem(url2, li, False)

    elif 'thevideobee' in url:
        calidades = calidadesthevideobee(url)
        for calidad in calidades:
            video_info['Title'] = '[COLOR orange][B][The Video Bee=' + calidad + '][/B][/COLOR] [COLOR white][B]' + \
                titulo + '[/B][/COLOR]'
            if year != '':
                video_info['Title'] = video_info['Title'] + \
                    ' [COLOR blue][B](' + year + ')[/B][/COLOR]'
            if season != '' and episode != '':
                url2 = build_url({'mode': 'play', 'playlink': url + '&calidad=' + calidad,
                                  'tmdbid': tmdbid, 'season': season, 'episode': episode})
            else:
                url2 = build_url(
                    {'mode': 'play', 'playlink': url + '&calidad=' + calidad, 'tmdbid': tmdbid})
            li = xbmcgui.ListItem(
                video_info['Title'], iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", video_info)
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            li.setArt(art_info)
            addMenuitem(url2, li, False)

    subs_file = os.path.join(addon_data_dir, 'subtitles.json')
    new_subs_file = {}
    new_subs_file['counter'] = 0
    new_subs_file['subtitulos'] = []
    new_subs_file['tmdbid'] = str(tmdbid) + 'S' + season + 'E' + episode
    if os.path.isfile(subs_file):
        try:
            subs_content = open(subs_file, 'rb').read()
            subs_content = json.loads(subs_content)
            if subs_content.get('tmdbid', '') == new_subs_file['tmdbid'] and subs_content.get('counter', '0') != '0' and len(subs_content.get('subtitulos', [])) > 0:
                new_subs_file = subs_content
        except:
            pass
    if len(media_subtitles) > 0:
        for media_subtitle in media_subtitles:
            if not media_subtitle[0] in [x[0] for x in new_subs_file['subtitulos']]:
                new_subs_file['subtitulos'].append(media_subtitle)
                new_subs_file['counter'] += 1
    open(subs_file, 'wb').write(json.dumps(new_subs_file))


def search(text=''):
    add_search_item()
    xbmcplugin.setContent(addon_handle, 'albums')
    website = 'https://fusionorg.net/searching.php?'
    if text == '':
        kb = xbmc.Keyboard('default', 'heading')
        kb.setDefault('')
        kb.setHeading('Buscar en la Coleccion Fusion')
        kb.setHiddenInput(False)
        kb.doModal()
        if kb.isConfirmed():
            text = kb.getText()
        else:
            dialog = xbmcgui.Dialog()
            dialog.notification("Fusion", 'La Busqueda se cancelo',
                                xbmcgui.NOTIFICATION_INFO, 3500, False)
            exit()

    if text == '':
        duration = 3500
        dialog = xbmcgui.Dialog()
        dialog.notification("Fusion", 'No se detecto nada escrito en el buscador Vuelve a Intentar',
                            xbmcgui.NOTIFICATION_INFO, duration, False)
    else:
        search_term = kb.getText()
        xbmcplugin.setPluginCategory(
            addon_handle, 'Buscar: ' + search_term.title())
        search_term = urllib.urlencode({'search': search_term})
        dir = website + search_term
        html = conect.get_url_d(dir)
        pattern = "<ppal>(.*?)<\/ppal>"

        matches = re.findall(
            '<ppalseries>(.*?)<\/ppalseries', html, re.MULTILINE)
        for match in matches:
            title = re.findall('titulo.*?value=(.*?)\/>',
                               match, re.MULTILINE)[0]
            sinopsis = re.findall(
                'info.*?value=(.*?)\/>', match, re.MULTILINE)[0]
            link = re.findall('link.*?value=(.*?)\/>',
                              match, re.MULTILINE)[0]
            thumbnail = re.findall(
                'thumbnail.*?value=(.*?)\/>', match, re.MULTILINE)[0]
            fanart = re.findall(
                'fanart.*?value=(.*?)\/>', match, re.MULTILINE)[0]
            tmdbid = re.findall(
                'tmdbid.*?value=(.*?)\/>', match, re.MULTILINE)[0]
            post_img_qy = addon.getSetting('pos_qy').replace(' px', '')
            if post_img_qy != 'Mejor':
                thumbnail = thumbnail.replace('/original/', '/w' + post_img_qy + '/')
            fan_img_qy = addon.getSetting('fan_qy').replace(' px', '')
            if fan_img_qy != 'Mejor':
                fanart = fanart.replace('/original/', '/w' + fan_img_qy + '/')
            url = build_url({'mode': 'seasons', 'direccion': link, 'fanart': fanart,
                             'info': sinopsis, 'tmdbid': tmdbid, 'serie': title})
            title = '[COLOR white][B]' + title + \
                '[/B][/COLOR]  [COLOR orange][B][TV Show][/B][/COLOR]'
            li = xbmcgui.ListItem(
                title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "Plot": sinopsis})
            li.setProperty('fanart_image', fanart)
            li.setArt({'fanart': fanart, 'poster': thumbnail})
            addMenuitem(url, li, True)

        items = re.findall(pattern, html, re.MULTILINE)
        for item in items:
            try:
                title = re.findall('titulo.*?lue=(.*?)\/>',
                                   item, re.MULTILINE)[0]
                title = base64.b64decode(title)
            except:
                try:
                    title = re.findall(
                        '.*title.*?=(.*?)\/>', item, re.MULTILINE)[0]
                    title = base64.b64decode(title)
                except:
                    title = 'Sin Titulo (reportar video)'

            pattern = 'info.*?lue=(.*?)\/>'
            plot = re.findall(pattern, item, re.IGNORECASE)[0]

            pattern = 'thumb.*?lue=(.*?)\/>'
            thumbnail = re.findall(pattern, item, re.IGNORECASE)[0]
            thumbnail = base64.b64decode(thumbnail)

            pattern = 'fanart.*?lue=(.*?)\/>'
            fanart = re.findall(pattern, item, re.IGNORECASE)[0]
            fanart = base64.b64decode(fanart)

            post_img_qy = addon.getSetting('pos_qy').replace(' px', '')
            if post_img_qy != 'Mejor':
                thumbnail = thumbnail.replace('/original/', '/w' + post_img_qy + '/')
            fan_img_qy = addon.getSetting('fan_qy').replace(' px', '')
            if fan_img_qy != 'Mejor':
                fanart = fanart.replace('/original/', '/w' + fan_img_qy + '/')

            pattern = '.*lin.*?lue=(.*?)\/>'
            url = re.findall(pattern, item, re.IGNORECASE)[0]
            url = base64.b64decode(url)

            year = re.findall('id=.year.*?lue=(.*?)\/>',
                              item, re.IGNORECASE)[0]
            yeari = int(base64.b64decode(year))
            years = base64.b64decode(year)

            url = build_url({'mode': 'servidores', 'foldername': title, 'direccion': url,
                             'thumbnail': thumbnail, 'fanart': fanart, 'info': plot, 'year': years})
            li = xbmcgui.ListItem(
                iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "Plot": plot, "Year": yeari,
                                 "MediaType": "Movie", "OriginalTitle": title, "SortTitle": title})
            li.setProperty('fanart_image', fanart)
            li.setArt({'fanart': fanart, 'poster': thumbnail})
            li.setLabel('[COLOR white][B]' + title + '[/B][/COLOR] [COLOR blue][B](' +
                        years + ')[/B][/COLOR] [COLOR orange][B][Película][/B][/COLOR]')
            li.setLabel2('[COLOR white][B]' + title + '[/B][/COLOR] [COLOR blue][B](' +
                         years + ')[/B][/COLOR] [COLOR orange][B][Película][/B][/COLOR]')
            addMenuitem(url, li, True)

        matches = re.findall(
            '<ppalcollections(.*?)<\/ppalcollections', html, re.MULTILINE)
        for match in matches:
            id = re.findall('id.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
            id = base64.b64decode(id)
            sinopsis = re.findall(
                'info.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
            sinopsis = base64.b64decode(sinopsis)
            titulo = re.findall('titulo.*?lue=(.*?)\/>',
                                match, re.MULTILINE)[0]
            titulo = base64.b64decode(titulo)
            link = re.findall('link.*?lue=(.*?)\/>',
                              match, re.MULTILINE)[0]
            link = base64.b64decode(link)
            poster = re.findall('thumb.*?lue=(.*?)\/>',
                                match, re.MULTILINE)[0]
            poster = base64.b64decode(poster)
            fanart = re.findall('fanart.*?lue=(.*?)\/>',
                                match, re.MULTILINE)[0]
            fanart = base64.b64decode(fanart)
            url = build_url({'mode': 'movies', 'foldername': titulo, 'direccion': link,
                             'thumbnail': poster, 'fanart': fanart, 'info': sinopsis, 'categoria': titulo})
            titulo = '[COLOR white][B]' + titulo + \
                '[/B][/COLOR]  [COLOR orange][B][Coleccion][/B][/COLOR]'
            li = xbmcgui.ListItem(
                titulo, iconImage=poster, thumbnailImage=poster)
            li.setInfo("video", {"Title": titulo, "Plot": sinopsis})
            li.setArt({'fanart': fanart, 'poster': poster})
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, True)
        endMenu()


def reproductor(url, tmdbid='', season='', episode=''):
    if tmdbid != '':
        ids = json.dumps({'tmdb': tmdbid})
        xbmcgui.Window(10000).setProperty('script.trakt.ids', ids)
    if 'drive.google.com' in url:
        from base.servers import gvideo
        final_link = gvideo.google_final_link(url)
        play_video(final_link, tmdbid, season, episode)
    elif 'gamovideo' in url:
        final_link = urlgamovideo(url)
        if 'File was locked by administrator' in final_link:
            duration = 5500  # in milliseconds
            message = 'Contenido Bloqueado'
            dialog = xbmcgui.Dialog()
            dialog.notification("Fusion", message,
                                xbmcgui.NOTIFICATION_INFO, duration, False)
            return
        play_video(final_link, tmdbid, season, episode)
    elif 'clipwatching.com' in url:
        echo, final_link = urlclipwatching(url)
        if echo:
            play_video(final_link, tmdbid, season, episode)
        else:
            duration = 5500  # in milliseconds
            message = 'Clipwatching Fallo al obtener Link'
            dialog = xbmcgui.Dialog()
            dialog.notification("Fusion", message,
                                xbmcgui.NOTIFICATION_INFO, duration, False)
            xbmc.executebuiltin("XBMC.Container.Refresh")
    elif 'uptobox' in url:
        echo, final_link = uptobox(url, tmdbid + 'S' + season + 'E' + episode)
        if echo:
            play_video(final_link, tmdbid, season, episode)
        else:
            duration = 5500  # in milliseconds
            if final_link == '':
                message = 'UPTOBOX Fallo al obtener Link'
            else:
                message = final_link
            dialog = xbmcgui.Dialog()
            dialog.notification("Fusion", message,
                                xbmcgui.NOTIFICATION_INFO, duration, False)
            xbmc.executebuiltin("XBMC.Container.Refresh")

    elif 'uptostream' in url:
        echo, final_link = uptostream(url)
        if echo:
            play_video(final_link, tmdbid, season, episode)
        else:
            if final_link == '':
                message = 'UPTOSTREAM Fallo al obtener Link'
            else:
                message = final_link
            duration = 5500  # in milliseconds
            dialog = xbmcgui.Dialog()
            dialog.notification("Fusion", message,
                                xbmcgui.NOTIFICATION_INFO, duration, False)
            xbmc.executebuiltin("XBMC.Container.Refresh")

    elif 'tune.pk' in url:
        echo, final_link = tunepk(url)
        if echo:
            play_video(final_link, tmdbid, season, episode)
        else:
            if final_link != '':
                message = final_link
            else:
                message = 'Tune.pk Fallo al obtener link!!!'
            duration = 5500  # in milliseconds
            dialog = xbmcgui.Dialog()
            dialog.notification("Fusion", message,
                                xbmcgui.NOTIFICATION_INFO, duration, False)
            xbmc.executebuiltin("XBMC.Container.Refresh")

    elif 'gounlimited' in url or 'tazmovies' in url:
        echo, final_link = gounlimited(url)
        if echo:
            play_video(final_link, tmdbid, season, episode)
        else:
            if final_link != '':
                message = final_link
            else:
                message = 'Tune.pk Fallo al obtener link!!!'
            duration = 5500  # in milliseconds
            dialog = xbmcgui.Dialog()
            dialog.notification("Fusion", message,
                                xbmcgui.NOTIFICATION_INFO, duration, False)
            xbmc.executebuiltin("XBMC.Container.Refresh")

    elif 'fembed.com' in url or 'feurl.com' in url:
        echo, final_link = urlfembed(url)
        if echo:
            play_video(final_link, tmdbid, season, episode)
        else:
            duration = 5500  # in milliseconds
            message = 'Fembed Fallo al obtener Link'
            dialog = xbmcgui.Dialog()
            dialog.notification("Fusion", message,
                                xbmcgui.NOTIFICATION_INFO, duration, False)
            xbmc.executebuiltin("XBMC.Container.Refresh")

    elif 'uqload.com' in url:
        echo, final_link = urluqload(url)
        if echo:
            play_video(final_link, tmdbid, season, episode)
        else:
            duration = 5500  # in milliseconds
            message = 'UQload Fallo al obtener Link'
            dialog = xbmcgui.Dialog()
            dialog.notification("Fusion", message,
                                xbmcgui.NOTIFICATION_INFO, duration, False)
            xbmc.executebuiltin("XBMC.Container.Refresh")

    elif 'ok.ru' in url or 'odnoklassniki.ru' in url:
        echo, final_link = urlokru(url)
        if echo:
            play_video(final_link, tmdbid, season, episode)
        else:
            duration = 5500  # in milliseconds
            message = 'Ok.ru Fallo al obtener Link'
            dialog = xbmcgui.Dialog()
            dialog.notification("Fusion", message,
                                xbmcgui.NOTIFICATION_INFO, duration, False)
            xbmc.executebuiltin("XBMC.Container.Refresh")

    elif 'upstream.to' in url:
        echo, final_link = urlupstream(url)
        if echo:
            play_video(final_link, tmdbid, season, episode)
        else:
            duration = 5500  # in milliseconds
            message = 'UpStream Fallo al obtener Link'
            dialog = xbmcgui.Dialog()
            dialog.notification("Fusion", message,
                                xbmcgui.NOTIFICATION_INFO, duration, False)
            xbmc.executebuiltin("XBMC.Container.Refresh")

    elif 'mixdrop' in url:
        echo, final_link = urlmixdrop(url)
        if echo:
            play_video(final_link, tmdbid, season, episode)
        else:
            duration = 5500  # in milliseconds
            message = 'MIXdrop Fallo al obtener Link'
            dialog = xbmcgui.Dialog()
            dialog.notification("Fusion", message,
                                xbmcgui.NOTIFICATION_INFO, duration, False)
            xbmc.executebuiltin("XBMC.Container.Refresh")

    elif 'vup.to' in url:
        echo, final_link = urlvup(url)
        if echo:
            play_video(final_link, tmdbid, season, episode)
        else:
            duration = 5500  # in milliseconds
            message = 'Vup.to Fallo al obtener Link'
            dialog = xbmcgui.Dialog()
            dialog.notification("Fusion", message,
                                xbmcgui.NOTIFICATION_INFO, duration, False)
            xbmc.executebuiltin("XBMC.Container.Refresh")

    elif 'thevideobee' in url:
        echo, final_link = urlthevideobee(url)
        if echo:
            play_video(final_link, tmdbid, season, episode)
        else:
            duration = 5500  # in milliseconds
            message = 'The Video Bee Fallo al obtener Link'
            dialog = xbmcgui.Dialog()
            dialog.notification("Fusion", message,
                                xbmcgui.NOTIFICATION_INFO, duration, False)
            xbmc.executebuiltin("XBMC.Container.Refresh")
    elif 'youtube' in url:
        play_video(url, tmdbid, season, episode)
    else:
        play_video(url, tmdbid, season, episode)


def play_video(path, tmdbid='', season='', episode=''):
    subtitles = []
    play_item = xbmcgui.ListItem(path=path)
    if addon.getSetting('subtitles') == 'Si':
        subs_file_path = os.path.join(
            addon_data_dir, 'subtitles.json').encode('utf-8')
        subs_file = {}
        subs_file['counter'] = 0
        subs_file['subtitulos'] = []
        subs_file['tmdbid'] = str(tmdbid) + 'S' + season + 'E' + episode
        if os.path.isfile(subs_file_path):
            try:
                subs_content = open(subs_file_path, 'rb').read()
                subs_content = json.loads(subs_content)
                if subs_content.get('tmdbid', '') == subs_file['tmdbid'] and subs_content.get('counter', '0') != '0' and len(subs_content.get('subtitulos', [])) > 0:
                    subs_file = subs_content
            except:
                pass
        if len(subs_file['subtitulos']) > 0:
            subs_path = os.path.join(addon_data_dir, 'subtitles')
            try:
                if not os.path.isdir(subs_path):
                    os.makedirs(subs_path)
                counter_subs = 1
                for subtitle in subs_file['subtitulos']:
                    if subtitle[1].lower().startswith('s') or subtitle[1].lower().startswith('e') or subtitle[1].lower().startswith('l'):
                        sub_path = os.path.join(
                            subs_path, 'subtitle' + str(counter_subs) + '.' + subtitle[1] + '.srt').encode('utf-8', 'ignore')
                        sub_url = subtitle[0]
                        try:
                            r = conect.get_url(sub_url)
                            if r != '' and r != 'Imposible conectar con el server':
                                if r.status_code == 200 and r.content != '':
                                    strData = ""
                                    if '.vtt' in sub_url:
                                        strData = strData + \
                                            vtt2srt.convertContent(r.content)
                                    elif '.srt' in sub_url:
                                        try:
                                            strData = strData + \
                                                vtt2srt.convertContent(
                                                    r.content)
                                        except:
                                            strData = r.content
                                    if strData != "":
                                        open(sub_path, 'wb').write(strData)
                                        subtitles.append(sub_path)
                                    try:
                                        filename, file_extension = os.path.splitext(
                                            sub_url)
                                        if file_extension != '.srt':
                                            open(sub_path.replace('.srt', file_extension), 'wb').write(
                                                r.content)
                                            subtitles.append(
                                                sub_path.replace('.srt', file_extension))
                                    except:
                                        pass
                        except:
                            pass
                        counter_subs += 1
            except:
                pass
    if len(subtitles) > 0:
        play_item.setSubtitles(subtitles)
    play_item.setProperty("IsPlayable", "true")
    if 'm3u8' in path:
        xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
        version=float(xbmc_version[:4])
        if version <= 18.6:
            play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
        else:
            play_item.setProperty('inputstream', 'inputstream.adaptive')
        play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
        play_item.setMimeType('application/vnd.apple.mpegstream_url')
        play_item.setContentLookup(False)
        if '|' in path:
            headers_play = path.split('|')[1]
            play_item.setProperty(
                'inputstream.adaptive.stream_headers', headers_play)
    else:
        play_item.setMimeType('video/mp4')
    duration = 5500  # in milliseconds
    if ('uptostream' in path or 'uptobox' in path or 'clipwatching' in path or 'playercdn' in path or 'google.com' in path or 'gamovideo' in path or 'tunefiles.com' in path or '/v.mp4' in path or 'redirector?' in path or 'mycdn.me' in path or '.mp4' in path or 'megaupload.to' in path or '.m3u8' in path):
        message = 'En Breve empezara la Reproduccion'
        dialog = xbmcgui.Dialog()
        dialog.notification("Fusion", message,
                            xbmcgui.NOTIFICATION_INFO, duration, False)
        xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
    else:
        message = 'Intentando Repruducir Medio'
        try:
            stream_url = resolve_url(path)
            if stream_url:
                play_item.setPath(stream_url)
        # Pass the item to the Kodi player.
        except:
            pass

        dialog = xbmcgui.Dialog()
        dialog.notification("Fusion", message,
                            xbmcgui.NOTIFICATION_INFO, duration, False)
        xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)


def resolve_url(url):
    stream_url = urlresolver.HostedMediaFile(url=url).resolve()
    # If urlresolver returns false then the video url was not resolved.
    if not stream_url:
        try:
            import resolveurl
            stream_url = resolveurl.HostedMediaFile(url=url).resolve()
        except:
            pass
        if not stream_url:
            return False
    return stream_url


def get_dir_addon():
    return xbmc.translatePath(addon.getAddonInfo('Path'))


def collections_list(categorias, urls, posters, fanarts, infos, modes):
    xbmcplugin.setContent(addon_handle, 'albums')
    xbmcplugin.setPluginCategory(addon_handle, 'Colleciones')
    add_search_item()
    for categoria, info, fanart, mode, poster, url in zip(categorias, infos, fanarts, modes, posters, urls):
        url = build_url(
            {'mode': mode, 'direccion': url, 'categoria': categoria})
        li = xbmcgui.ListItem('[COLOR white][B]' + categoria + '[/B][/COLOR]')
        li.setInfo("video", {"Plot": info})
        li.setArt({'fanart': fanart, 'poster': poster})
        addMenuitem(url, li, True)
    endMenu()


def collection_list(web, categoria, mode='movies'):
    xbmcplugin.setContent(addon_handle, 'albums')
    xbmcplugin.setPluginCategory(addon_handle, categoria.title())
    data = conect.get_url_d(web)
    matches = re.findall('<ppal(.*?)<\/ppal', data, re.MULTILINE)
    add_search_item()
    for match in matches:
        id = re.findall('id.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        id = base64.b64decode(id)
        sinopsis = re.findall('info.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        sinopsis = base64.b64decode(sinopsis)
        titulo = re.findall('titulo.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        titulo = base64.b64decode(titulo)
        link = re.findall('link.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        link = base64.b64decode(link)
        poster = re.findall('thumb.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        poster = base64.b64decode(poster)
        fanart = re.findall('fanart.*?lue=(.*?)\/>', match, re.MULTILINE)[0]
        fanart = base64.b64decode(fanart)
        post_img_qy = addon.getSetting('pos_qy').replace(' px', '')
        if post_img_qy != 'Mejor':
            poster = poster.replace('/original/', '/w' + post_img_qy + '/')
        fan_img_qy = addon.getSetting('fan_qy').replace(' px', '')
        if fan_img_qy != 'Mejor':
            fanart = fanart.replace('/original/', '/w' + fan_img_qy + '/')
        url = build_url({'mode': mode, 'foldername': titulo, 'direccion': link,
                         'thumbnail': poster, 'fanart': fanart, 'info': sinopsis, 'categoria': titulo})
        titulo = '[COLOR white][B]' + titulo + '[/B][/COLOR]'
        li = xbmcgui.ListItem(titulo, iconImage=poster, thumbnailImage=poster)
        li.setInfo("video", {"Title": titulo, "Plot": sinopsis})
        li.setArt({'fanart': fanart, 'poster': poster})
        li.setProperty('fanart_image', fanart)
        addMenuitem(url, li, True)
    endMenu()


def solve_request(urls):
    identifier = 'R' + str(int(time.time()))
    options = []
    urls_actives = []
    num_links = len(urls)
    headerpD = 'FusionOrg Resolver'
    line1pD = 'Links Validos: {}, Links Faltantes: {}'.format('0', num_links)
    line2pD = ''
    line3pD = 'Iniciando resolver'
    pDialog = xbmcgui.DialogProgress()
    porcentpD = 0
    pDialog.create(headerpD, line1pD, line2pD, line3pD)
    if num_links > 0:
        inc_pD = 100 / num_links
    else:
        inc_pD = 100
    for url in urls:
        media_subtitles = []
        server = url.replace(
            'https://', '').replace('http://', '').replace('www.', '').replace('//', '').split('/')
        server[0] = server[0].title()
        line1pD = 'Links Validos: {}, Links Faltantes: {}'.format(
            str(len(options)), num_links)
        line2pD = line3pD
        line3pD = 'Comprobando {} '.format(server[0])
        pDialog.update(porcentpD, line1pD, line2pD, line3pD)
        if pDialog.iscanceled():
            pDialog.close()
            dialog.notification("FusionOrg", "Reproduccion cancelada!!!",
                                xbmcgui.NOTIFICATION_INFO, 5000, False)
            exit()
        if 'drive.google.com' in url:
            from base.servers import gvideo
            try:
                calidades = gvideo.google_calidades(url)
                for calidad in calidades:
                    urls_actives += [url + '&q=' + calidad]
                    options += ['[COLOR orange][B]Gvideo=' +
                                calidad + '[/B][/COLOR]']
                    line3pD += '[COLOR green] Valido[/COLOR]'
            except:
                pass
        elif 'clipwatching.com' in url:
            calidades = calidadesclipwatching(url)
            for calidad in calidades:
                urls_actives += [url + '&calidad=' + calidad]
                options += ['[COLOR orange][B]Clipwatching=' +
                            calidad + '[/B][/COLOR]']
                line3pD += '[COLOR green] Valido[/COLOR]'
        elif 'gamovideo.com' in url:
            calidades = urlgamovideo(url)
            if 'http' in calidades:
                urls_actives += [calidades]
                options += ['[COLOR orange][B]Gamovideo[/B][/COLOR]']
                line3pD += '[COLOR green] Valido[/COLOR]'
        elif ('uptobox.com' in url or 'uptostream.com' in url):
            servers, media_subtitles = uptoboxtest(url, identifier)
            if len(servers) > 0:
                for server in servers:
                    if server == 'uptostream':
                        for calidad in servers['uptostream']:
                            urls_actives += [servers['uptostream'][calidad][1]]
                            options += ['[COLOR orange][B]' +
                                        servers['uptostream'][calidad][0].replace('[', ' ').replace(']', ' ').replace('  ', ' ') + '[/B][/COLOR]']
                            line3pD += '[COLOR green] Valido[/COLOR]'
                    elif server == 'uptobox':
                        for calidad in servers['uptobox']:
                            urls_actives += [servers['uptobox'][calidad][1]]
                            options += ['[COLOR orange][B]' +
                                        servers['uptobox'][calidad][0].replace('[', ' ').replace(']', ' ').replace('  ', ' ') + '[/B][/COLOR]']
                            line3pD += '[COLOR green] Valido[/COLOR]'
        elif 'tune.pk' in url:
            echo, calidades = tunepk(url)
            if echo and len(calidades) > 0:
                for calidad in calidades:
                    urls_actives += [url + '&calidad=' + calidad]
                    options += ['[COLOR orange][B]Tune.pk=' +
                                calidad + 'p[/B][/COLOR]']
                    line3pD += '[COLOR green] Valido[/COLOR]'
        elif 'gounlimited' in url or 'tazmovies' in url:
            echo, calidades, media_subtitles = gounlimited(url)
            if echo and len(calidades) > 0:
                for calidad in calidades:
                    urls_actives += [url + '&calidad=' + calidad]
                    options += ['[COLOR orange][B]Gounlimited=' +
                                calidad + 'p[/B][/COLOR]']
                    line3pD += '[COLOR green] Valido[/COLOR]'
        elif 'fembed.com' in url or 'feurl.com' in url:
            calidades = calidadesfembed(url)
            for calidad in calidades:
                urls_actives += [url + '&calidad=' + calidad]
                options += ['[COLOR orange][B]Fembed=' +
                            calidad + '[/B][/COLOR]']
                line3pD += '[COLOR green] Valido[/COLOR]'

        elif 'uqload' in url:
            calidades = calidadesuqload(url)
            if calidades:
                urls_actives += [url]
                options += ['[COLOR orange][B]Uqload[/B][/COLOR]']
                line3pD += '[COLOR green] Valido[/COLOR]'

        elif 'ok.ru' in url or 'odnoklassniki.ru' in url:
            echo, calidades = calidadesokru(url)
            if echo:
                for calidad in calidades:
                    urls_actives += [url + '&calidad=' + calidad]
                    options += ['[COLOR orange][B]Ok.ru=' +
                                calidad + '[/B][/COLOR]']
                    line3pD += '[COLOR green] Valido[/COLOR]'

        elif 'upstream' in url:
            valid = calidadesupstream(url)
            if valid:
                urls_actives += [url]
                options += ['[COLOR orange][B]UpStream[/B][/COLOR]']
                line3pD += '[COLOR green] Valido[/COLOR]'

        elif 'mixdrop' in url:
            calidades = calidadesmixdrop(url)
            for calidad in calidades:
                urls_actives += [url]
                options += ['[COLOR orange][B]' + calidad + '[/B][/COLOR]']
                line3pD += '[COLOR green] Valido[/COLOR]'

        elif 'vup.to' in url:
            calidades = calidadesvup(url)
            for calidad in calidades:
                urls_actives += [url]
                options += ['[COLOR orange][B]' + calidad + '[/B][/COLOR]']
                line3pD += '[COLOR green] Valido[/COLOR]'

        elif 'thevideobee' in url:
            calidades = calidadesthevideobee(url)
            for calidad in calidades:
                urls_actives += [url + '&calidad=' + calidad]
                options += ['[COLOR orange][B]The Video Bee=' +
                            calidad + '[/B][/COLOR]']
                line3pD += '[COLOR green] Valido[/COLOR]'

        else:
            try:
                hmf = urlresolver.HostedMediaFile(url)
                if hmf:
                    stream_url = urlresolver.resolve(url)
                    if stream_url:
                        if isinstance(stream_url, list):
                            for k in stream_url:
                                line3pD += '[COLOR green] Valido[/COLOR]'
                                if k['quality'] == 'HD':
                                    urls_actives += [k['url']]
                                    options += ['[COLOR orange][B]' +
                                                server[0] + '=HD[/B][/COLOR]']
                                elif k['quality'] == 'SD':
                                    urls_actives += [k['url']]
                                    options += ['[COLOR orange][B]' +
                                                server[0] + '=SD[/B][/COLOR]']
                                elif k['quality'] == '1080p':
                                    urls_actives += [k['url']]
                                    options += ['[COLOR orange][B]' +
                                                server[0] + '=1080p[/B][/COLOR]']
                                else:
                                    urls_actives += [k['url']]
                                    options += ['[COLOR orange][B]' +
                                                server[0] + '[/B][/COLOR]']
                        elif stream_url:
                            urls_actives += [stream_url]
                            options += ['[COLOR orange][B]' +
                                        server[0] + '[/B][/COLOR]']
                            line3pD += '[COLOR green] Valido[/COLOR]'
            except:
                try:
                    import resolveurl
                    hmf = resolveurl.HostedMediaFile(url)
                    if hmf:
                        stream_url = resolveurl.resolve(url)
                        if stream_url:
                            if isinstance(stream_url, list):
                                for k in stream_url:
                                    line3pD += '[COLOR green] Valido[/COLOR]'
                                    if k['quality'] == 'HD':
                                        urls_actives += [k['url']]
                                        options += ['[COLOR orange][B]' +
                                                    server[0] + '=HD[/B][/COLOR]']
                                    elif k['quality'] == 'SD':
                                        urls_actives += [k['url']]
                                        options += ['[COLOR orange][B]' +
                                                    server[0] + '=SD[/B][/COLOR]']
                                    elif k['quality'] == '1080p':
                                        urls_actives += [k['url']]
                                        options += ['[COLOR orange][B]' +
                                                    server[0] + '=1080p[/B][/COLOR]']
                                    else:
                                        urls_actives += [k['url']]
                                        options += ['[COLOR orange][B]' +
                                                    server[0] + '[/B][/COLOR]']
                            elif stream_url:
                                urls_actives += [stream_url]
                                options += ['[COLOR orange][B]' +
                                            server[0] + '[/B][/COLOR]']
                                line3pD += '[COLOR green] Valido[/COLOR]'
                except:
                    pass
        if not 'Valido' in line3pD:
            line3pD += ' [COLOR red]Fallo[/COLOR]'
        num_links -= 1
        porcentpD += inc_pD
        line1pD = 'Links Validos: {}, Links Faltantes: {}'.format(
            str(len(options)), num_links)
        line2pD = line2pD
        line3pD = line3pD
        pDialog.update(porcentpD, line1pD, line2pD, line3pD)
        if pDialog.iscanceled():
            pDialog.close()
            dialog = xbmcgui.Dialog()
            dialog.notification("FusionOrg", "Reproduccion cancelada!!!",
                                xbmcgui.NOTIFICATION_INFO, 5000, False)
            exit()

        subs_file = os.path.join(addon_data_dir, 'subtitles.json')
        new_subs_file = {}
        new_subs_file['counter'] = 0
        new_subs_file['subtitulos'] = []
        new_subs_file['tmdbid'] = identifier + 'SE'
        if os.path.isfile(subs_file):
            try:
                subs_content = open(subs_file, 'rb').read()
                subs_content = json.loads(subs_content)
                if subs_content.get('tmdbid', '') == new_subs_file['tmdbid'] and subs_content.get('counter', '0') != '0' and len(subs_content.get('subtitulos', [])) > 0:
                    new_subs_file = subs_content
            except:
                pass
        if len(media_subtitles) > 0:
            for media_subtitle in media_subtitles:
                new_subs_file['subtitulos'].append(media_subtitle)
                new_subs_file['counter'] += 1
        open(subs_file, 'wb').write(json.dumps(new_subs_file))
    pDialog.close()
    if len(urls_actives) > 0:
        option = 0
        if len(urls_actives) > 1:
            option = xbmcgui.Dialog().select('Selecciona el link de tu preferencia', options)
            if (option < 0):
                dialog = xbmcgui.Dialog()
                dialog.notification("FusionOrg", "Reproduccion cancelada!!!",
                                    xbmcgui.NOTIFICATION_INFO, 5000, False)
                exit()
        url = urls_actives[option]
        if 'drive.google.com' in url:
            from base.servers import gvideo
            final_link = gvideo.google_final_link(url)
        elif 'gamovideo' in url:
            final_link = url
            if 'File was locked by administrator' in final_link:
                final_link = ''
                url = ''
        elif 'clipwatching.com' in url:
            echo, final_link = urlclipwatching(url)
            if not echo:
                final_link = ''
                url = ''
        elif 'uptobox' in url:
            echo, final_link = uptobox(url, identifier)
            if not echo:
                final_link = ''
                url = ''
        elif 'uptostream' in url:
            echo, final_link = uptostream(url)
            if not echo:
                final_link = ''
                url = ''
        elif 'tune.pk' in url:
            echo, final_link = tunepk(url)
            if not echo:
                final_link = ''
                url = ''
        elif 'gounlimited' in url or 'tazmovies' in url:
            echo, final_link = gounlimited(url)
            if not echo:
                final_link = ''
                url = ''
        elif 'fembed.com' in url or 'feurl.com' in url:
            echo, final_link = urlfembed(url)
            if not echo:
                final_link = ''
                url = ''
        elif 'uqload' in url:
            echo, final_link = urluqload(url)
            if not echo:
                final_link = ''
                url = ''
        elif 'ok.ru' in url or 'odnoklassniki.ru' in url:
            echo, final_link = urlokru(url)
            if not echo:
                final_link = ''
                url = ''
        elif 'upstream.to' in url:
            echo, final_link = urlupstream(url)
            if not echo:
                final_link = ''
                url = ''
        elif 'mixdrop' in url:
            echo, final_link = urlmixdrop(url)
            if not echo:
                final_link = ''
                url = ''
        elif 'vup.to' in url:
            echo, final_link = urlvup(url)
            if not echo:
                final_link = ''
                url = ''

        elif 'thevideobee' in url:
            echo, final_link = urlthevideobee(url)
            if not echo:
                final_link = ''
                url = ''

        else:
            final_link = url

        if final_link != '':
            play_video(final_link, identifier)
            return True

    dialog = xbmcgui.Dialog()
    dialog.notification("FusionOrg", "Fallo al resolver el link!!![CR]O los links no son validos.",
                        xbmcgui.NOTIFICATION_INFO, 5000, True)
    return False


def add_search_item():
    categoria = 'Buscador'
    fanart = 'https://i.imgur.com/S07Dlve.jpg'
    poster = 'https://i.imgur.com/OiQWdpa.png'
    info = 'Buscar en la biblioteca de Fusion.'
    mode = 'mode04'
    url = build_url({'mode': mode})
    li = xbmcgui.ListItem('[COLOR white][B]' + categoria + '[/B][/COLOR]')
    li.setInfo("video", {"Plot": info})
    li.setArt({'fanart': fanart, 'poster': poster})
    addMenuitem(url, li, True)
