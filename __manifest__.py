# -*- coding: utf-8 -*-
{
    'name' : 'Movies',
    'version' : '0.1',
    'summary': '',
    'sequence': 0,
    'description': """
Test task.
    """,
    'category': '',
    'website': '',
    'images' : [],
    'depends' : ['contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/movie_view.xml',
        'views/cinema_view.xml',
        'views/menu_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'movie/static/src/css/movie.css',
            'movie/static/src/js/movie.js',
         ],
    }
}
