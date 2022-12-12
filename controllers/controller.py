# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request

import requests
import base64

import logging
_logger = logging.getLogger(__name__)

class MovieController(http.Controller):

    @http.route('/getmovies', type='json', auth='user', methods=['POST'])
    def get_movies(self, movie):
        res = []
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        api_host = "https://kinobd.net/api/films/search/title?q="
        api_req = movie
        r = requests.get(api_host + api_req, headers=headers)
        res = r.json()
        return res

    @http.route('/getimg', type='json', auth='user', methods=['POST'])
    def get_img(self, src):
        r = requests.get(src)
        res = base64.b64encode(r.content).decode("utf-8")
        return res