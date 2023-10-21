# -*- coding: utf-8 -*-

from odoo import models, fields, api


class player(models.Model):
    _name = 'interstellar.player'
    _description = 'Jugador de Interstellar'

    name = fields.Char(string='Nombre')
    spaceships = fields.One2many(comodel_name='interstellar.spaceship', inverse_name='player')


class planet(models.Model):
    _name = 'interstellar.planet'
    _description = 'Planeta'

    name = fields.Char(string='Planeta')

    precious_minerals = fields.Integer(default=100)
    food = fields.Integer(default=500)
    construction_materials = fields.Integer(default=500)


class spaceship(models.Model):
    _name = 'interstellar.spaceship'
    _description = 'Nave'

    name = fields.Char(string='Nombre')
    player = fields.Many2one(comodel_name='interstellar.player', required=True)
    weapons = fields.Many2many('interstellar.weapon')


class weapon(models.Model):
    _name = 'interstellar.weapon'
    _description = 'Arma'

    name = fields.Char(string='Nombre')
    spaceships = fields.Many2many('interstellar.spaceship')
