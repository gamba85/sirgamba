# coding=utf-8
import base64
import os

from base import control
from base import tools


is_fusion_request = control.addon_details('plugin.video.FusionTv.Request', fields=[
                                          'enabled', 'installed', 'fanart', 'thumbnail'])

""" Menu Ppal de Fusion"""


def categoriasprincipales():
    categorias = ['Instala Fusion Org [COLOR green]Request[/COLOR]', 'Películas',
                  'TV Shows', 'Colecciones', 'Buscador', 'Herramientas']
    if ('enabled' or 'installed') in is_fusion_request:
        if is_fusion_request['enabled']:
            categorias[0] = 'Television en Fusion Org [COLOR green]Request[/COLOR]'
    return categorias


def fanartsprincipales():
    #=========================================================================
    # dir_fan_pri = os.path.join(
    #     tools.get_dir_addon(), 'resources', 'media', 'principal', 'fanart')
    #=========================================================================
    dir_fan_pri = 'https://i.imgur.com/'
    fanarts = ['1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg',
               'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg']
    fanartss = []
    for fanart in fanarts:
        fanartss.append(os.path.join(dir_fan_pri, fanart))
    return fanartss


def postersprincipales():
    posterss = ['https://i.imgur.com/v2WxUCv.png', 'https://i.imgur.com/93blal1.png', 'https://i.imgur.com/GOlzcSY.png',
                'https://i.imgur.com/6lIrijE.png', 'https://i.imgur.com/OiQWdpa.png', 'https://i.imgur.com/3SzWau5.png']
    return posterss


def infosprincipales():
    infos = ['Recomendamos instalar Fusion Org [COLOR green]Request[/COLOR][CR]En Fusion Org [COLOR green]Request[/COLOR] hay contenido de IPTV',
             'Disfruta de las películas agregadas por todos los usuarios,',
             'Disfruta de tus series favoritas.',
             'Colecciones de películas',
             'Buscar en la biblioteca de Fusion.',
             'Tools.']
    if ('enabled' or 'installed') in is_fusion_request:
        if is_fusion_request['enabled']:
            infos[0] = 'Television en Fusion Org Request'
    return infos


def modesprincipales():
    modes = ['install_request', 'mode02', 'mode03',
             'collections', 'mode04', 'mode05', 'mode06']
    if ('enabled' or 'installed') in is_fusion_request:
        if is_fusion_request['enabled']:
            modes[0] = 'request'
    return modes


""" Subcategorias de Películas"""


def subcategoriasmovies():
    subcategorias = ['Ultimas Agregadas', 'Mas Populares', 'Mejor Valoradas', 'Por Año', 'Estrenos', 'Accion', 'Animacion', 'Aventura', 'Ciencia Ficcion', 'Comedia',
                     'Crimen', 'Documental', 'Drama', 'Familia', 'Fantasia', 'Guerra', 'Historia', 'Misterio', 'Musica', 'Romance', 'Suspenso', 'Terror', 'Western', 'Otros']
    return subcategorias


def archivosmovies():
    archivos = ['ultimas', 'populares', 'mejores', 'year', 'estrenos', 'accion', 'animacion', 'aventura', 'ficcion', 'comedia', 'crimen',
                'documental', 'drama', 'familia', 'fantasia', 'guerra', 'historia', 'misterio', 'musica', 'romance', 'suspense', 'terror', 'western', 'otros']
    return archivos


def subpostersmovies():
    subposterss = ['https://i.imgur.com/U2CeOYD.png', 'https://i.imgur.com/gEbomhW.png', 'https://i.imgur.com/ALl0o0S.png', 'https://i.imgur.com/7ozqFmI.png', 'https://i.imgur.com/QkEJFnU.png', 'https://i.imgur.com/N5a3Qzi.png', 'https://i.imgur.com/i2gP1ng.png', 'https://i.imgur.com/bT6Jakd.png', 'https://i.imgur.com/3DcDpev.png', 'https://i.imgur.com/ZzryErK.png', 'https://i.imgur.com/6ej0VeD.png', 'https://i.imgur.com/9o8olXv.png',
                   'https://i.imgur.com/v61Mh9i.png', 'https://i.imgur.com/I2J72S5.png', 'https://i.imgur.com/zo1sZdS.png', 'https://i.imgur.com/paqWLjQ.png', 'https://i.imgur.com/jOQ9MhD.png', 'https://i.imgur.com/zeI4O6o.png', 'https://i.imgur.com/uCd3wMv.png', 'https://i.imgur.com/dV7Cftq.png', 'https://i.imgur.com/ZhqOsbN.png', 'https://i.imgur.com/3znjcDi.png', 'https://i.imgur.com/spY1uKH.png', 'https://i.imgur.com/Lvoclxh.png']
    return subposterss


def subfanartsmovies():
    #=========================================================================
    # dir_fan_pel = os.path.join(
    #     tools.get_dir_addon(), 'resources', 'media', 'peliculas', 'fanart')
    # subfanarts = ['fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png',
    #               'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png']
    #=========================================================================
    dir_fan_pel = 'https://i.imgur.com/'

    subfanarts = ['1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg',
                  'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg']
    subfanartss = []
    for subfanart in subfanarts:
        subfanartss.append(os.path.join(dir_fan_pel, subfanart))
    return subfanartss


def subinfosmovies():
    subinfos = ['Ultimas Agregadas', 'Las Más Populares (Trending)', 'Las Méjor valoradas', 'Por Año', 'Estrenos', 'Acción', 'Animación', 'Aventura', 'Ciencia Ficción', 'Comedia',
                'Crimen', 'Documentales', 'Drama', 'Familia', 'Fantasia', 'Bélicas', 'Historicas', 'Misterio', 'Músicales', 'Romance', 'Suspenso', 'Terror', 'Occidentales', 'Aún no catalogados']
    return subinfos


def submodesmovies():
    submodes = ['movies', 'movies', 'movies', 'for_year', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies',
                'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies']
    return submodes


"""Subcategorias de Series"""


def subcategoriastvshows():
    subcategoriastvshows = ['Todos los TV Shows', 'Mas Populares', 'Mejor Valoradas', 'Acción y Aventura', 'Animación', 'Ciencia Ficción y Fantasía', 'Comedia', 'Crimen', 'Documental',
                            'Drama', 'Familia', 'Guerra y Politica', 'Historia', 'Kids', 'Misterio', 'Occidental', 'Reality', 'Romance', 'Terror', 'Otros']
    return subcategoriastvshows


def subposterstvshows():
    dir_pos_tvs = os.path.join(
        tools.get_dir_addon(), 'resources', 'media', 'tv show', 'poster')
    subposterstvshows = ['todos los tv shows.png', 'mas populares.png', 'mejor valoradas.png', 'accion y aventura.png', 'animacion.png', 'ciencia ficcion y fantasia.png', 'Comedia.png',
                         'Crimen.png', 'documental.png', 'drama.png', 'Familia.png', 'guerra y politica.png', 'Historia.png', 'kids.png', 'misterio.png', 'occidental.png', 'Reality.png',
                         'romance.png', 'terror.png', 'otros.png']
    subposterstvshowss = []
    for subposterstvshow in subposterstvshows:
        subposterstvshowss.append(os.path.join(dir_pos_tvs, subposterstvshow))
    return subposterstvshowss


def subfanartstvshows():
    #=========================================================================
    # dir_fan_tvs = os.path.join(
    #     tools.get_dir_addon(), 'resources', 'media', 'tv show', 'fanart')
    # subfanartstvshows = ['fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png',
    #                      'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png', 'fanart.png']
    #=========================================================================
    dir_fan_tvs = 'https://i.imgur.com/'

    subfanartstvshows = ['1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg',
                         '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg', '1aiVCPY.jpg', 'S07Dlve.jpg']
    subfanartstvshowss = []
    for subfanartstvshow in subfanartstvshows:
        subfanartstvshowss.append(os.path.join(dir_fan_tvs, subfanartstvshow))
    return subfanartstvshowss


def subinfostvshows():
    subinfostvshows = ['Todos los TV Shows', 'Mas Populares', 'Mejor Valoradas', 'Acción y Aventura', 'Animación', 'Ciencia Ficción y Fantasía', 'Comedia', 'Crimen',
                       'Documental', 'Drama', 'Familia', 'Guerra y Politica', 'Historia', 'Kids', 'Misterio', 'Occidental', 'Reality', 'Romance', 'Terror', 'Aún no catalogados']
    return subinfostvshows


def submodestvshows():
    submodestvshows = ['tvshows', 'tvshows', 'tvshows', 'tvshows', 'tvshows', 'tvshows', 'tvshows', 'tvshows', 'tvshows',
                       'tvshows', 'tvshows', 'tvshows', 'tvshows', 'tvshows', 'tvshows', 'tvshows', 'tvshows', 'tvshows', 'tvshows', 'tvshows']
    return submodestvshows


def subtagstvshows():
    submodestvshows = ['all', 'populares', 'mejor', 'accion', 'animacion', 'ciencia', 'comedia', 'crimen', 'documental',
                       'drama', 'familia', 'guerra', 'historia', 'kids', 'misterio', 'occidental', 'reality', 'romance', 'terror', 'otros']
    return submodestvshows


"""Subcategorias de Herramientas"""


def subtools():
    subtools = ['Abrir ajustes', 'Actualizar Repositorios', 'Compartir Log']
    return subtools


def subtoolsinfos():
    subtoolsinfos = ['Abre los ajistes', 'Forza que los addon tipo repositorio se actualicen',
                     '(Requiere tener instalado loguploader)Si tienes un problema como un fallo o error, comparte el log y mandanos el link para revisarlo en el grupo de telegram o en el grupo de facebook.']
    return subtoolsinfos


def subtoolsposters():
    subtoolsfanarts = ['https://i.imgur.com/1aiVCPY.jpg',
                       'https://i.imgur.com/S07Dlve.jpg', 'https://i.imgur.com/1aiVCPY.jpg']
    return subtoolsfanarts


def subtoolsfanarts():
    #=========================================================================
    # subtoolsfanarts = ['https://fusionorg.net/images/fanart.jpg', 'https://fusionorg.net/images/fanart.jpg', 'https://fusionorg.net/images/fanart.jpg',
    #                    'https://fusionorg.net/images/fanart.jpg', 'https://fusionorg.net/images/fanart.jpg', 'https://fusionorg.net/images/fanart.jpg']
    #=========================================================================
    subtoolsfanarts = ['https://i.imgur.com/3SzWau5.png',
                       'https://i.imgur.com/3SzWau5.png', 'https://i.imgur.com/3SzWau5.png']
    return subtoolsfanarts


def subtoolsmodes():
    subtoolsmodes = ['open_settings', 'force_update', 'loguploader']
    return subtoolsmodes


""" Subcategorias de Colecciones"""


def subcategoriascollections():
    subcategoriascollections = [
        'Coleciones de Actores', 'Colecciones de Películas']
    return subcategoriascollections


def suburlcollections():
    urlcollections = ['https://fusionorg.net/colecciones/index.php?type=persons',
                      'https://fusionorg.net/colecciones/index.php?type=movies']
    return urlcollections


def subposterscollections():
    dir_pos_col = os.path.join(
        tools.get_dir_addon(), 'resources', 'media', 'collections')
    subposters = ['persons.png', 'movies.png']
    subposterss = []
    for subposter in subposters:
        subposterss.append(os.path.join(dir_pos_col, subposter))
    return subposterss


def subfanartscollections():
    #=========================================================================
    # dir_fan_pel = os.path.join(
    #     tools.get_dir_addon(), 'resources', 'media', 'peliculas', 'fanart')
    # subfanarts = ['fanart.png', 'fanart.png']
    #=========================================================================
    dir_fan_pel = 'https://i.imgur.com/'

    subfanarts = ['1aiVCPY.jpg', 'S07Dlve.jpg']
    subfanartss = []
    for subfanart in subfanarts:
        subfanartss.append(os.path.join(dir_fan_pel, subfanart))
    return subfanartss


def subinfoscollections():
    subinfos = ['Coleccion de películas por Actores o Directores',
                'Coleccion de películas por Secuela']
    return subinfos


def submodescollections():
    submodes = ['collection', 'collection']
    return submodes
