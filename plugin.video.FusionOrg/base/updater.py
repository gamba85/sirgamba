# -*- coding: utf-8 -*-
import base64
import hashlib
import json
import os
import time
from xml.dom import minidom
from xml.etree import ElementTree as ET

import control
from resources.lib.conector import conect
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs


is_fusion_request = control.addon_details('plugin.video.FusionTv.Request', fields=[
                                          'enabled', 'installed', 'fanart', 'thumbnail'])
is_repo = control.addon_details('repository.Fusion.org', fields=[
                                'enabled', 'installed', 'fanart', 'thumbnail'])


addon = xbmcaddon.Addon()
addon_dir = xbmc.translatePath(xbmc.translatePath(
    addon.getAddonInfo('Path')).decode('utf-8'))
addon_data_dir = xbmc.translatePath(xbmc.translatePath(
    addon.getAddonInfo('profile')).decode('utf-8'))


def add_fusion_source():
    exist_source = False
    successful = False
    path_sources = xbmc.translatePath('special://userdata')
    path_sources = os.path.join(path_sources, 'sources.xml')

    #=========================================================================
    # try:
    #=========================================================================
    if os.path.exists(path_sources):
        xmldoc = minidom.parse(path_sources)
    else:
        xmldoc = minidom.Document()
        nodo_sources = xmldoc.createElement("sources")
        for type in ['programs', 'video', 'music', 'pictures', 'files', 'games']:
            nodo_type = xmldoc.createElement(type)
            element_default = xmldoc.createElement("default")
            element_default.setAttribute("pathversion", "1")
            nodo_type.appendChild(element_default)
            nodo_sources.appendChild(nodo_type)
            xmldoc.appendChild(nodo_sources)

    nodo_video = xmldoc.childNodes[0].getElementsByTagName("files")[0]
    nodos_paths = nodo_video.getElementsByTagName("path")
    list_path = []
    for path in nodos_paths:
        list_path += [path.firstChild.data]
    subfolder = 'https://repositorio.fusionorg.net/'
    if not subfolder in list_path:
        name = 'Repo FusionOrg'
        nodo_source = xmldoc.createElement("source")
        nodo_name = xmldoc.createElement("name")
        nodo_name.appendChild(xmldoc.createTextNode(name))
        nodo_source.appendChild(nodo_name)
        nodo_path = xmldoc.createElement("path")
        nodo_path.setAttribute("pathversion", "1")
        nodo_path.appendChild(xmldoc.createTextNode(subfolder))
        nodo_source.appendChild(nodo_path)
        nodo_allowsharing = xmldoc.createElement("allowsharing")
        nodo_allowsharing.appendChild(xmldoc.createTextNode('true'))
        nodo_source.appendChild(nodo_allowsharing)
        nodo_video.appendChild(nodo_source)
        successful = True
        exist_source = True
    else:
        exist_source = True

    content = '\n'.join(
        [x for x in xmldoc.toprettyxml().encode("utf-8").splitlines() if x.strip()])
    write_file(path_sources, content)

    #=========================================================================
    # except:
    #     pass
    #=========================================================================

    if successful:
        control.infoDialog(
            'Se Agrego correctamente El Repo de FusionOrg a Sources.xml')
    elif not successful and exist_source:
        control.infoDialog('El Repo de FusionOrg ya esta en las fuentes')
    elif not successful and not exist_source:
        control.infoDialog(
            'Fallo al agregar la fuente de FusionOrg a Sources.xml')


def install_FOR():
    exist_repo = False
    enable_repo = False
    if ('enabled' or 'installed') in is_repo:
        exist_repo = True
        if is_repo['enabled']:
            xbmc.executebuiltin('InstallAddon(plugin.video.FusionTv.Request)')
            return
    add_fusion_source()
    xbmc.executebuiltin('InstallFromZip')


def force_update():
    add_fusion_source()
    update = build_conectors_data_system()
    update = build_conectors_data_remote()
    xbmc.executebuiltin('UpdateAddonRepos')
    xbmc.executebuiltin('UpdateLocalAddons')
    control.infoDialog('Repositorios actualizados!!!')


def write_file(file, buffer):
    handler = xbmcvfs.File(file, 'w')
    result = handler.write(buffer)
    handler.close()
    return result


def build_conectors_data_remote():
    connectors_path = os.path.join(addon_dir, 'base', 'servers')
    data_connectors_path = os.path.join(
        connectors_path, 'connectors_remote.json')
    data = 'Failed'
    response = conect.get_url(
        'https://fusionorg.net/connectors/index.php', m='post', p={'connectors': 'hola'})
    if response != 'Imposible conectar con el server':
        if response.status_code == 200:
            data = json.loads(response.content)
            data['conectores'] = len(data)
            data['actualizar'] = True
            data['time'] = time.time()
            write_file(data_connectors_path, json.dumps(data, indent=1))
    return data


def get_connectors_data_remote():
    connectors_path = os.path.join(addon_dir, 'base', 'servers')
    data_connectors_path = os.path.join(
        connectors_path, 'connectors_remote.json')
    if os.path.isfile(data_connectors_path):
        try:
            data = open(data_connectors_path, 'r').read()
            data = json.loads(data)
            data_time = data['time']
            time_diff = time.time() - data_time
            time_diff = abs(time_diff)
            if time_diff > 3600:
                data = build_conectors_data_remote()
        except:
            data = build_conectors_data_remote()
    else:
        data = build_conectors_data_remote()
    return data


def get_connectors_data_system():
    connectors_path = os.path.join(addon_dir, 'base', 'servers')
    data_connectors_path = os.path.join(
        connectors_path, 'connectors_system.json')
    if os.path.isfile(data_connectors_path):
        try:
            data = open(data_connectors_path, 'r').read()
            data = json.loads(data)
            data_time = data['time']
            time_diff = time.time() - data_time
            time_diff = abs(time_diff)
            if time_diff > 3600:
                data = build_conectors_data_system()
        except:
            data = build_conectors_data_system()
    else:
        data = build_conectors_data_system()
    return data


def build_conectors_data_system():
    connectors_path = os.path.join(addon_dir, 'base', 'servers')
    data_connectors_path = os.path.join(
        connectors_path, 'connectors_system.json')
    files = os.listdir(connectors_path)
    response = {}
    for file in files:
        path_file = os.path.join(connectors_path, file)
        if os.path.isfile(path_file) and not file.startswith('__') and file.endswith('.py'):
            hash = hashlib.md5()
            hash.update(open(path_file).read())
            md5 = hash.hexdigest()
            response[file] = md5
    response['time'] = time.time()
    write_file(data_connectors_path, json.dumps(response, indent=1))
    return response

def test_connectors():
    local_connectors = get_connectors_data_system()
    remote_connectors = get_connectors_data_remote()
    if remote_connectors != 'Failed' and remote_connectors.get('actualizar', False):
        num_conectores = remote_connectors.get('conectores', 0)
        headerpD = 'FusionOrg AutoUpdater'
        line1pD = 'Conectores Actualizados: {}, Conectores Faltantes: {}'.format(
            '0', str(num_conectores))
        line2pD = ''
        line3pD = 'Iniciando AutoUpdater...'
        pDialog = xbmcgui.DialogProgress()
        counter = 0
        porcentpD = 0
        if num_conectores > 0:
            inc_pD = 100 / num_conectores
        else:
            inc_pD = 100
        pDialog.create(headerpD, line1pD, line2pD, line3pD)
        
        for remote_connector in remote_connectors:
            if remote_connector != 'time' and remote_connector != 'conectores' and remote_connector != 'actualizar':
                line2pD = line3pD
                line3pD = 'Comprobando {} '.format(remote_connector)
                pDialog.update(porcentpD, line1pD, line2pD, line3pD)
                md5_local_connector = local_connectors.get(
                    remote_connector, 'Fail')
                md5_remote_connector = remote_connectors.get(
                    remote_connector, 'Fail')
                if md5_remote_connector != 'Fail':
                    md5_remote_connector = md5_remote_connector.get(
                        'md5', 'Fail')
                    if md5_remote_connector != 'Fail':
                        if md5_local_connector != md5_remote_connector:
                            line2pD = line3pD
                            line3pD = 'Descargando {} '.format(remote_connector)
                            pDialog.update(porcentpD, line1pD, line2pD, line3pD)
                            download_connector(
                                remote_connector, local_connectors, remote_connectors)
                            local_connectors = build_conectors_data_system()
                            md5_local_connector = local_connectors.get(remote_connector, 'Fail')
                            if md5_local_connector != md5_remote_connector:
                                line2pD = line3pD
                                line3pD = 'Fallo al Actualizar {} '.format(remote_connector)
                                pDialog.update(counter * inc_pD, line1pD, line2pD, line3pD)
                            else:
                                line2pD = line3pD
                                line3pD = '{} Actualizado'.format(remote_connector)
                                pDialog.update(counter * inc_pD, line1pD, line2pD, line3pD)
                        else:
                            line2pD = line3pD
                            line3pD = '{} Actualizado'.format(remote_connector)
                            pDialog.update(counter * inc_pD, line1pD, line2pD, line3pD)
                counter += 1
                line1pD = 'Conectores Actualizados: {}, Conectores Faltantes: {}'.format(
                    str(counter), str(num_conectores - counter))
                pDialog.update(counter * inc_pD, line1pD, line2pD, line3pD)
        pDialog.update(100, line1pD, line2pD, line3pD)
        pDialog.close()


def download_connector(local_connector, local_connectors, remote_connectors):
    response = conect.get_url(
        'https://fusionorg.net/connectors/index.php', m='post', p={'connector': local_connector})
    if response != 'Imposible conectar con el server':
        if response.status_code == 200:
            data = response.content
            hash = hashlib.md5()
            hash.update(data)
            md5 = hash.hexdigest()
            if md5 == remote_connectors.get(local_connector, {'md5': ''}).get('md5', ''):
                connectors_path = os.path.join(addon_dir, 'base', 'servers')
                path_file = os.path.join(connectors_path, local_connector)
                if not local_connector.startswith('__') and local_connector.endswith('.py'):
                    open(path_file, 'w').write(data)
