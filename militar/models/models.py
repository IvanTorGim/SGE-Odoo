# -*- coding: utf-8 -*-

from datetime import date, datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class player(models.Model):
    _name = 'militar.player'
    _description = 'Jugador'

    name = fields.Char()
    birth_date = fields.Date(string='Fecha de nacimiento')
    age = fields.Integer(string='Edad', compute='_get_age')

    # Campo default con una función, la función antes de ser llamada
    # def _get_enrolment_date(self):
    #     return date.today()
    # enrollment_date = fields.Date(default=_get_enrolment_date, readonly=True)

    enrollment_date = fields.Datetime(default=lambda p: datetime.now())
    last_login = fields.Datetime()
    level = fields.Integer(string='Nivel')

    weapons = fields.Many2many(string='Armas', comodel_name='militar.weapon',
                               domain="[('level', '<=', level)]")

    @api.depends('birth_date')
    def _get_age(self):
        for player in self:
            today = date.today()
            if player.birth_date:
                player.age = today.year - player.birth_date.year
            else:
                player.age = 1

    @api.constrains('weapons')
    def _max_weapon(self):
        for player in self:
            if len(player.weapons) > 2:
                raise ValidationError('Solo puedes seleccionar 2 armas')


class weapon(models.Model):
    _name = 'militar.weapon'
    _description = 'Arma'

    name = fields.Char(string='Nombre')
    description = fields.Text(string="Descripción")
    type = fields.Selection(string='tipo', selection=[('Assault Rifle', 'Fusil de asalto'),
                                                      ('Semi-Automatic Pistol', 'Pistola semiautomática'),
                                                      ('Submachine Gun', 'Subfusil'),
                                                      ('Snipe Rifle', 'Francotirador')])
    caliber = fields.Char(string='Calibre')
    country = fields.Char(string='País')
    charger = fields.Integer(string='Cargador')
    level = fields.Integer(string='Nivel')
