# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class movie(models.Model):
    _name = "movie"
    _description = "list of movies"

    name = fields.Char(string="Название фильма", required=True)
    year = fields.Char(string="Год выпуска")
    country = fields.Char(string="Страна")
    fieldtoupload = fields.Text()
    poster = fields.Binary(string="Постер", store=True, attachment=False)
    rating_kp = fields.Float(string="Рейтинг KP", digits=(2,1))
    rating_imdb = fields.Float(string="Рейтинг IMDB", digits=(2,1))

    @api.onchange('fieldtoupload')
    def onchange_fieldtoupload(self):
        self.poster = self.fieldtoupload
        self.fieldtoupload = None

    _sql_constraints = [
        ('name_year_country_uniq', 'unique (name,year,country)', 'Данный фильм уже существует в базе.')
    ]


class muvie_view(models.Model):
    _name = "movie.view"
    _description = "list of movie views"

    def name_get(self):
        result = []
        for record in self:
            name = record.movie_id.name + ', ' + record.company_id.name + ', ' + record.partner_id.name
            result.append((record.id, name))
        return result

    movie_id = fields.Many2one('movie', string="Фильм", required=True)
    partner_id = fields.Many2one('res.partner', string="Зритель", required=True, domain=[('is_company', '=', False)])
    company_id = fields.Many2one('res.company', string="Кинотеатр", required=True)
    date = fields.Date(string="Дата просмотра" , required=True)
    priority = fields.Selection([
        ('0', 0),
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
        ('6', 6),
        ('7', 7),
        ('8', 8),
        ('9', 9),
        ('10', 10),
    ], default='0', string="Рейтинг")

    _sql_constraints = [
        ('movie_partner_company_date_uniq', 'unique (movie,partner_id,company_id,date)',
         'На выбранную дату уже есть запись о просмтре данного фильма.')
    ]

    @api.model
    def create(self, vals):
        seance = self.env['cinema.movie.view'].search([('company_id', '=', vals['company_id']),
                                                       ('movie_id', '=', vals['movie_id']),
                                                       ('date', '=', vals['date'])])
        if not seance:
            self.env['cinema.movie.view'].create({'company_id': vals['company_id'], 'movie_id': vals['movie_id'],
                                                  'date': vals['date'], 'viewer_ids': [vals['partner_id']]})
        else:
            partner_list = []
            for partner in seance.viewer_ids:
                partner_list.append(partner.id)
            partner_list.append(vals['partner_id'])
            seance.write({'viewer_ids': partner_list})
        return super(muvie_view, self).create(vals)

    def unlink(self):
        for record in self:
            seance = self.env['cinema.movie.view'].search([('company_id', '=', record.company_id.id),
                                                           ('movie_id', '=', record.movie_id.id),
                                                           ('date', '=', record.date)])
            if seance:
                partner_list = []
                for partner in seance.viewer_ids:
                    partner_list.append(partner.id)
                if record.partner_id.id in partner_list:
                    partner_list.remove(record.partner_id.id)
                    if len(partner_list) > 0:
                        seance.write({'viewer_ids': partner_list})
                    else:
                        seance.unlink()
        return super(muvie_view, self).unlink()
