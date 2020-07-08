# -*- coding: utf-8 -*-

'''
    Author Bugatsinho

        License summary below, for more details please read license.txt file

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 2 of the License, or
        (at your option) any later version.
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import datetime
import json
import re
import time
import urllib
import urlparse

from base import client


def google_calidades(url):
    calidades = []
    try:
        calidades = [x['quality'] for x in google(url)]
    except:
        pass
    calidad_d = google_calidad_d(url)
    if calidad_d != '':
        calidades += [calidad_d]
    return calidades


def google_calidad_d(url):
    return google_d(url)[0]


def google_d(url):
    calidad = ('', '')
    try:
        google_id = re.findall(
            '[\/|=]([0-9a-zA-Z-_]{20,})[\&|\/|\s*]', url, re.I)
        if len(google_id) < 0:
            google_id = re.findall('[\/|=]([0-9a-zA-Z-_]{20,})', url, re.I)
        if len(google_id) > 0:
            google_id = google_id[0]
        else:
            return ('', '')
        url = 'https://drive.google.com/uc?id={}&export=download'.format(
            google_id)
        headers = {'User-Agent': client.agent()}
        result = client.request(url, output='extended', headers=headers)
        try:
            headers['user-agent'] = headers['User-Agent']
            headers.pop('User-Agent')
            headers.pop('Referer')
            headers.pop('Accept-Language')
        except:
            pass
        try:
            headers['cookie'] = result[3].replace(' ','')
        except:
            pass
        try:
            size = re.findall('>\s*\((.*?)\)\s*<', result[0], re.I)
            size = size[0]
            calidad = re.findall(
                '(\d{3,4}\s*[p|P]).*?\(%s\)' % (size), result[0], re.I)
            if len(calidad) == 0:
                calidad = re.findall('(4[k|K]).*?\(%s\)' %
                                     (size), result[0], re.I)
            if len(calidad) == 0:
                calidad = re.findall('(2[k|K]).*?\(%s\)' %
                                     (size), result[0], re.I)
            if len(calidad) > 0:
                size = 'Original ' + size + ' ' + calidad[0]
            else:
                size = 'Original ' + size

        except:
            size = ''
        if ('Download anyway' in result[0] or 'Descargar de todos modos' in result[0]) and size != '':
            confirm = re.findall(
                'download_warning_\d*_{}=(.*?);'.format(google_id), headers['cookie'], re.I)
            if (len(confirm) > 0):
                now_timestamp = datetime.datetime.utcnow()
                headers['cookie'] = headers['cookie'] + '; 1P_JAR=' + \
                    now_timestamp.strftime('%Y-%m-%d-%H')
                calidad = (size, 'https://drive.google.com/uc?export=download&confirm={}&id={}'.format(
                    confirm[0], google_id) + '|' + urllib.urlencode(headers))
        else:
            return ('', '')
    except:
        return ('', '')
    return calidad


def google_final_link(url):
    calidad = urlparse.parse_qs(url)['q'][0]
    url = url.split('&')[0]
    if 'Original' in calidad:
        links = google_d(url)
        return links[1]
    else:
        links = google(url)
    for link in links:
        if link['quality'] == calidad:
            header_test = {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'}
            header_test = '|' + urllib.urlencode(header_test)
            return link['url'] + header_test


def google(url, ref=None):
    try:
        if 'lh3.googleusercontent' in url or 'bp.blogspot' in url:
            newheaders = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
                'Accept': '*/*',
                'Host': 'lh3.googleusercontent.com',
                'Accept-Language': 'en-US,en;q=0.8,de;q=0.6,es;q=0.4',
                'Accept-Encoding': 'identity;q=1, *;q=0',
                'Referer': ref,
                'Connection': 'Keep-Alive',
                'X-Client-Data': 'CJK2yQEIo7bJAQjEtskBCPqcygEIqZ3KAQjSncoBCKijygE=',
                'Range': 'bytes=0-'
            }
            resp = client.request(
                url, headers=newheaders, redirect=False, output='extended', timeout='10')
            loc = resp[2]['Location']
            c = resp[2]['Set-Cookie'].split(';')[0]
            url = '%s|Cookie=%s' % (loc, c)
            return url

        if any(x in url for x in ['youtube.', 'docid=']):
            url = 'https://drive.google.com/file/d/%s/view' % \
                re.compile('docid=([\w-]+)').findall(url)[0]

        netloc = urlparse.urlparse(url.strip().lower()).netloc
        netloc = netloc.split('.google')[0]

        if netloc == 'docs' or netloc == 'drive':
            url = url.split('/preview', 1)[0]
            url = url.replace('drive.google.com', 'docs.google.com')

        headers = {'User-Agent': client.agent()}

        result = client.request(url, output='extended', headers=headers)

        try:
            headers['Cookie'] = result[2]['Set-Cookie']
        except:
            pass

        result = result[0]

        if netloc == 'docs' or netloc == 'drive':
            result = re.compile('"fmt_stream_map",(".+?")').findall(result)[0]
            result = json.loads(result)
            result = [i.split('|')[-1] for i in result.split(',')]
            result = sum([googletag(i, append_height=True)
                          for i in result], [])

        elif netloc == 'photos':
            result = result.replace('\r', '').replace(
                '\n', '').replace('\t', '')
            result = re.compile('"\d*/\d*x\d*.+?","(.+?)"').findall(result)[0]

            result = result.replace('\\u003d', '=').replace('\\u0026', '&')
            result = re.compile('url=(.+?)&').findall(result)
            result = [urllib.unquote(i) for i in result]

            result = sum([googletag(i, append_height=True)
                          for i in result], [])

        elif netloc == 'picasaweb':
            id = re.compile('#(\d*)').findall(url)[0]

            result = re.search('feedPreload:\s*(.*}]}})},',
                               result, re.DOTALL).group(1)
            result = json.loads(result)['feed']['entry']

            if len(result) > 1:
                result = [i for i in result if str(
                    id) in i['link'][0]['href']][0]
            elif len(result) == 1:
                result = result[0]

            result = result['media']['content']
            result = [i['url'] for i in result if 'video' in i['type']]
            result = sum([googletag(i, append_height=True)
                          for i in result], [])

        elif netloc == 'plus':
            id = (urlparse.urlparse(url).path).split('/')[-1]

            result = result.replace('\r', '').replace(
                '\n', '').replace('\t', '')
            result = result.split('"%s"' % id)[-1].split(']]')[0]

            result = result.replace('\\u003d', '=').replace('\\u0026', '&')
            result = re.compile('url=(.+?)&').findall(result)
            result = [urllib.unquote(i) for i in result]

            result = sum([googletag(i, append_height=True)
                          for i in result], [])

        result = sorted(result, key=lambda i: i.get('height', 0), reverse=True)

        url = []
        for q in ['4K', '1440p', '1080p', '720p', '480p', '360p']:
            try:
                url += [[i for i in result if i.get('quality') == q][0]]
            except:
                pass

        for i in url:
            i.pop('height', None)
            i.update({'url': i['url'] + '|%s' % urllib.urlencode(headers)})

        if not url:
            return
        return url
    except:
        return


def googletag(url, append_height=False):
    quality = re.compile('itag=(\d*)').findall(url)
    quality += re.compile('=m(\d*)$').findall(url)
    try:
        quality = quality[0]
    except:
        return []

    itag_map = {'151': {'quality': 'SD', 'height': 72}, '212': {'quality': 'SD', 'height': 480},
                '313': {'quality': '4K', 'height': 2160},
                '242': {'quality': 'SD', 'height': 240}, '315': {'quality': '4K', 'height': 2160},
                '219': {'quality': 'SD', 'height': 480},
                '133': {'quality': 'SD', 'height': 240}, '271': {'quality': '1440p', 'height': 1440},
                '272': {'quality': '4K', 'height': 2160},
                '137': {'quality': '1080p', 'height': 1080}, '136': {'quality': '720p', 'height': 720},
                '135': {'quality': 'SD', 'height': 480},
                '134': {'quality': 'SD', 'height': 360}, '82': {'quality': 'SD', 'height': 360},
                '83': {'quality': 'SD', 'height': 480},
                '218': {'quality': 'SD', 'height': 480}, '93': {'quality': 'SD', 'height': 360},
                '84': {'quality': '720p', 'height': 720},
                '170': {'quality': '1080p', 'height': 1080}, '167': {'quality': 'SD', 'height': 360},
                '22': {'quality': '720p', 'height': 720},
                '46': {'quality': '1080p', 'height': 1080}, '160': {'quality': 'SD', 'height': 144},
                '44': {'quality': 'SD', 'height': 480},
                '45': {'quality': '720p', 'height': 720}, '43': {'quality': 'SD', 'height': 360},
                '94': {'quality': 'SD', 'height': 480},
                '5': {'quality': 'SD', 'height': 240}, '6': {'quality': 'SD', 'height': 270},
                '92': {'quality': 'SD', 'height': 240},
                '85': {'quality': '1080p', 'height': 1080}, '308': {'quality': '1440p', 'height': 1440},
                '278': {'quality': 'SD', 'height': 144},
                '78': {'quality': 'SD', 'height': 480}, '302': {'quality': '720p', 'height': 720},
                '303': {'quality': '1080p', 'height': 1080},
                '245': {'quality': 'SD', 'height': 480}, '244': {'quality': 'SD', 'height': 480},
                '247': {'quality': '720p', 'height': 720},
                '246': {'quality': 'SD', 'height': 480}, '168': {'quality': 'SD', 'height': 480},
                '266': {'quality': '4K', 'height': 2160},
                '243': {'quality': 'SD', 'height': 360}, '264': {'quality': '1440p', 'height': 1440},
                '102': {'quality': '720p', 'height': 720},
                '100': {'quality': 'SD', 'height': 360}, '101': {'quality': 'SD', 'height': 480},
                '95': {'quality': '720p', 'height': 720},
                '248': {'quality': '1080p', 'height': 1080}, '96': {'quality': '1080p', 'height': 1080},
                '91': {'quality': 'SD', 'height': 144},
                '38': {'quality': '4K', 'height': 3072}, '59': {'quality': '480p', 'height': 480},
                '17': {'quality': 'SD', 'height': 144},
                '132': {'quality': 'SD', 'height': 240}, '18': {'quality': '360p', 'height': 360},
                '37': {'quality': '1080p', 'height': 1080},
                '35': {'quality': 'SD', 'height': 480}, '34': {'quality': 'SD', 'height': 360},
                '298': {'quality': '720p', 'height': 720},
                '299': {'quality': '1080p', 'height': 1080}, '169': {'quality': '720p', 'height': 720}}

    if quality in itag_map:
        quality = itag_map[quality]
        if append_height:
            return [{'quality': quality['quality'], 'height': quality['height'], 'url': url}]
        else:
            return [{'quality': quality['quality'], 'url': url}]
    else:
        return []


def googlepass(url):
    try:
        try:
            headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
        except:
            headers = None
        url = url.split('|')[0].replace('\\', '')
        url = client.request(url, headers=headers, output='geturl')
        if 'requiressl=yes' in url:
            url = url.replace('http://', 'https://')
        else:
            url = url.replace('https://', 'http://')
        if headers:
            url += '|%s' % urllib.urlencode(headers)
        return url
    except:
        return


##########TEST########################
#
#glink = 'https://drive.google.com/file/d/1D86ZMsRFbVA0Cvv59lKoP5NZM1u_kwRf1w/edit'
#
# for x in google(glink):
#    quality = x['quality']
#    url = x['url']
#
#    print quality, url
