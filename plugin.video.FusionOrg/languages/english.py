# coding=utf-8
import base64

""" Main Menu"""


def categoriasprincipales():
    categorias = ['TV [COLOR red] Building[/COLOR]',
                  'Movies', 'TV Shows', 'Search', "Fusion's Handbook"]
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


""" Subcat Movies"""


def subcategoriasmovies():
    subcategorias = ['Last added', 'Premieres', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
                     'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western']
    return subcategorias


def archivosmovies():
    archivos = ['last', 'premieres', 'adventure', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'family',
                'fantasy', 'history', 'horror', 'music', 'mystery', 'romance', 'fiction', 'tvmovie', 'thriller', 'war', 'western']
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
    subcategoriastvshows = ['All TV Shows']
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
    subcategoriastv = ['My Lists', 'Shared Lists']
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
