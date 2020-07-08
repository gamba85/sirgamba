# coding=utf-8
import base64

""" Menu Ppal de Fusion"""


def categoriasprincipales():
    categorias = ['Television [COLOR red] En Constriccion[/COLOR]',
                  'Peliculas', 'TV Shows', 'Buscador', 'Manual de Fusion']
    return categorias


def thumbnailsprincipales():
    thumbnails = ['', '', '', '', '']
    return thumbnails


def fanartsprincipales():
    fanarts = ['https://fusionorg.net/images/fanart.jpg', 'https://fusionorg.net/images/fanart.jpg',
               'https://fusionorg.net/images/fanart.jpg', 'https://fusionorg.net/images/fanart.jpg', 'https://fusionorg.net/images/fanart.jpg']
    return fanarts


def infosprincipales():
    infos = ['', '', '', '', '']
    return infos


def modesprincipales():
    modes = ['mode01', 'mode02', 'mode03', 'mode04', 'mode05']
    return modes


""" Subcategorias de Peliculas"""


def subcategoriasmovies():
    subcategorias = ['Ultimas Agregadas', 'Estrenos', 'Accion', 'Aventura', 'Comedia', 'Documental', 'Familia', 'Guerra', 'Misterio',
                     'Romance', 'Terror', 'Animacion', 'Ciencia Ficcion', 'Crimen', 'Drama', 'Fantasia', 'Historia', 'Musica', 'Suspenso', 'Western']
    return subcategorias


def archivosmovies():
    archivos = ['ultimas', 'estrenos', 'accion', 'aventura', 'comedia', 'documental', 'familia', 'guerra', 'misterio',
                'romance', 'terror', 'animacion', 'ficcion', 'crimen', 'drama', 'fantasia', 'historia', 'musica', 'suspense', 'western']
    return archivos


def subthumbnailsmovies():
    subthumbnails = ['', '', '', '', '', '', '', '',
                     '', '', '', '', '', '', '', '', '', '', '', '']
    return subthumbnails


def subfanartsmovies():
    subfanarts = ['', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', '', '', '', '', '', '']
    return subfanarts


def subinfosmovies():
    subinfos = ['', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '']
    return subinfos


def submodesmovies():
    submodes = ['movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies',
                'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies', 'movies']
    return submodes


# Subcategorias de Series

def subcategoriastvshows():
    subcategoriastvshows = ['Todos los TV Shows']
    return subcategoriastvshows


def subthumbnailstvshows():
    subthumbnailstvshows = ['']
    return subthumbnailstvshows


def subfanartstvshows():
    subfanartstvshows = ['']
    return subfanartstvshows


def subinfostvshows():
    subinfostvshows = ['']
    return subinfostvshows


def submodestvshows():
    submodestvshows = ['tvshows']
    return submodestvshows


# Subcategorias de Television

def subcategoriastv():
    subcategoriastv = ['Mis Listas', 'Listas Compartidas']
    return subcategoriastv


def subthumbnailstv():
    subthumbnailstv = ['', '']
    return subthumbnailstv


def subfanartstv():
    subfanartstv = ['', '']
    return subfanartstv


def subinfostv():
    subinfostv = ['', '']
    return subinfostv


def submodestv():
    submodestv = ['list', 'listshared']
    return submodestv
