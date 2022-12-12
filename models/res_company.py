# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class res_company(models.Model):
    _inherit = "res.company"
    _name = "res.company"

    movie_view_ids = fields.One2many('cinema.movie.view', 'company_id', string="Сеансы",)


class cinema_movie_view(models.Model):
    _name = 'cinema.movie.view'

    company_id = fields.Many2one('res.company', string="Кинотеатр", required=True)
    date = fields.Date(string="Дата сеанса", required=True)
    movie_id = fields.Many2one('movie', string="Фильм", required=True)
    viewer_ids = fields.Many2many('res.partner', 'cinema_movie_view_partner_rel', 'cmv_id', 'p_id', string="Зрители",
                                  domain=[('is_company', '=', False)])

    _sql_constraints = [
        ('company_date_movie_uniq', 'unique (company_id,date,movie_id)',
         'На выбранную дату уже был показ данного фильма.')
    ]
