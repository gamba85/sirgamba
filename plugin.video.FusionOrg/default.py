# coding=utf-8
import sys
import urlparse

from base import *
from base.tools import *
from languages.spanish import *
import xbmcaddon
import xbmcgui
import xbmcplugin


addon = xbmcaddon.Addon('plugin.video.FusionOrg')
addonname = addon.getAddonInfo('name')
language = addon.getSetting('language')
filenamejson = addon.getSetting('filename')
filejson = addon.getSetting('file')

filenamejsonshared = addon.getSetting('filenameshared')
filejsonshared = addon.getSetting('filejson')

args = urlparse.parse_qs(sys.argv[2][1:])
xbmcplugin.setContent(addon_handle, 'movies')
mode = args.get('mode', None)

#=========================================================================
# if language == 'Latino':
#     from languages.spanish import *
# elif language == 'Español':
#     from languages.spanish import *
# elif language == 'English':
#     from languages.english import *
# elif language == 'Portugues':
#     from languages.portuguese import *
# else:
#     from languages.spanish import *
#=========================================================================

test_connectors()

# Imprime el Menu Principal de la Aplicación

if mode is None:
    Directorios()
    menuppal(categoriasprincipales(), infosprincipales(),
             fanartsprincipales(), modesprincipales(), postersprincipales())
# Imprime Submenu de la Categoria Television
elif mode[0] == 'mode01':
    menuppal(subcategoriastv(), subinfostv(),
             subfanartstv(), submodestv(), subposterstv())

# Imprime el SubMenu de la Categoria de Películas
elif mode[0] == 'mode02':
    menucategoriasmovies(subcategoriasmovies(), subinfosmovies(), subfanartsmovies(
    ), submodesmovies(), subpostersmovies(), archivosmovies())

elif mode[0] == 'for_year':
    web = args['direccion'][0]
    movieslistyear(web, 'movies', 'Por Año')
# Imprime las Películas Dentro de las Categorias
elif mode[0] == 'movies':
    web = args['direccion'][0]
    categoria = args['categoria'][0]
    movieslist(web, 'servidores', categoria)

# Imprime el SubMenu de los TV Shows
elif mode[0] == 'mode03':
    menucategoriastvshows(subcategoriastvshows(), subinfostvshows(
    ), subfanartstvshows(), submodestvshows(), subposterstvshows(), subtagstvshows())

# imprime las colecciones activas
elif mode[0] == 'collections':
    collections_list(subcategoriascollections(), suburlcollections(), subposterscollections(
    ), subfanartscollections(), subinfoscollections(), submodescollections())

elif mode[0] == 'collection':
    web = args['direccion'][0]
    categoria = args['categoria'][0]
    collection_list(web, categoria)

# Imprime la Lista de Series
elif mode[0] == 'tvshows':
    web = args['direccion'][0]
    categoria = args['categoria'][0]
    tvshowslist(web, 'seasons', categoria)

# Imprime la Lista de Temporadas de Series
elif mode[0] == 'seasons':
    fanart = args['fanart'][0]
    sinopsis = args['info'][0]
    web = args['direccion'][0]
    tmdbid = args['tmdbid'][0]
    serie = args['serie'][0]
    seasonlist(web, fanart, sinopsis, 'episodes', tmdbid, serie)

# Imprime la Lista de Episodios de la Temporada
elif mode[0] == 'episodes':
    web = args['direccion'][0]
    tmdbid = args['tmdbid'][0]
    serie = args['serie'][0]
    episodeslist(web, 'servidores2', tmdbid, serie)

elif mode[0] == 'mode04':
    search()

# Imprime  El Menu de la Lista de Servidores para Películas
elif mode[0] == 'servidores':
    titulo = args['foldername'][0]
    thumbnail = args['thumbnail'][0]
    fanart = args['fanart'][0]
    try:
        sinopsis = args['info'][0]
    except:
        sinopsis = 'Sin info'
    url = args['direccion'][0]
    servidores(titulo, thumbnail, fanart, sinopsis, url)

# Imprime El Menu de la Lista de Servidores para Series
elif mode[0] == 'servidores2':
    web = args['direccion'][0]
    tmdbid = args['tmdbid'][0]
    season = args['season'][0]
    episode = args['episode'][0]
    serie = args['serie'][0]
    servidores2(web, tmdbid, season, episode, serie)

elif mode[0] == 'mode05':
    menuppal(subtools(), subtoolsinfos(), subtoolsposters(),
             subtoolsmodes(), subtoolsfanarts())

# Metodo de Reproduccion de Video
elif mode[0] == 'play':
    url = args['playlink'][0]
    tmdbid = args['tmdbid'][0]
    season = args.get('season', '')
    if type(season) == list and len(season) == 1:
        season = season[0]
    episode = args.get('episode', '')
    if type(episode) == list and len(episode) == 1:
        episode = episode[0]
    reproductor(url, tmdbid, season, episode)

elif mode[0] == 'playstb':
    tiempo, url = uptobox(args)
    if not tiempo:
        reproductor(url)
    else:
        mensaje("Debe esperar: " + url)
        pass

elif mode[0] == 'get_token_uptobox':
    get_token_uptobox()

elif mode[0] == 'wait':
    pass

elif mode[0] == 'open_settings':
    addon.openSettings()

elif mode[0] == 'fusion_request':
    n_links = args.get('n_link', None)
    if n_links != None:
        n_links = n_links[0]
        urls = []
        if n_links != '' and n_links != '0':
            if n_links == '1':
                if args.get('link1', None) != None:
                    urls += [args['link1'][0]]
            else:
                n_links = int(n_links)
                for x in range(1, n_links + 1):
                    if args.get('link' + str(x), None) != None:
                        urls += [args['link' + str(x)][0]]

            if len(urls) > 0:
                solve_request(urls)
            else:
                dialog = xbmcgui.Dialog()
                dialog.notification(
                    "FusionOrg", "No hay links válidos!!!", xbmcgui.NOTIFICATION_INFO, 5000, True)

elif mode[0] == 'fusion_request_tv':
    link = args.get('link', None)
    referer = args.get('referer', None)
    if link != None:
        link = link[0]
        if 'telerium' in link:
            from base.servers import telerium
            if referer != None:
                telerium.resolver(link, referer)
            else:
                telerium.resolver(link)
        elif 'wstream' in link or 'football-live.stream' in link:
            from base.servers import wstream
            if referer != None:
                wstream.resolver(link, referer)
            else:
                wstream.resolver(link)
        elif 'ok.ru' in link or 'odnoklassniki.ru' in link:
            from base.servers import okru
            okru.urlokru(link)

        else:
            dialog = xbmcgui.Dialog()
            dialog.notification(
                "FusionOrg", "No hay links válidos!!!", xbmcgui.NOTIFICATION_INFO, 5000, True)

elif mode[0] == 'install_request':
    install_FOR()

elif mode[0] == 'force_update':
    force_update()
    Directorios()
    menuppal(categoriasprincipales(), infosprincipales(),
             fanartsprincipales(), modesprincipales(), postersprincipales())

elif mode[0] == 'library':
    #=========================================================================
    # movie = args.get('movie', None)
    #=========================================================================
    from resources.lib.library_tools import main_library
