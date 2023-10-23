# -*- coding: utf-8 -*-

from odoo import models, fields, api


class player(models.Model):
    _name = 'interstellar.player'
    _description = 'Jugador de Interstellar'

    name = fields.Char(string='Nombre')


class planet(models.Model):
    _name = 'interstellar.planet'
    _description = 'Planeta'

    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')
    dimension = fields.Integer(string='Dimension', help='Dimension del planeta en kilómetros')
    race = fields.Char(string='Raza')
    age = fields.Integer(string='Edad', )

    precious_minerals = fields.Integer(default=100, string='Minerales preciosos')
    energy = fields.Integer(default=500, string='Energía')
    construction_materials = fields.Integer(default=500, string='Materiales de construcción')

    spaceships = fields.Many2many(
        string='Naves',
        comodel_name='interstellar.spaceship',
        relation='planet_spaceship_rel',
        column1='planet_id',
        column2='spaceship_id'
    )


class spaceship(models.Model):
    _name = 'interstellar.spaceship'
    _description = 'Nave'

    name = fields.Char(string='Nombre')

    planets = fields.Many2many(
        comodel_name='interstellar.planet',
        relation='planet_spaceship_rel',
        column1='spaceship_id',
        column2='planet_id'
    )
    weapons = fields.Many2many(
        comodel_name='interstellar.weapon',
        relation='spaceship_weapon_rel',
        column1='spaceship_id',
        column2='weapon_id'
    )


class weapon(models.Model):
    _name = 'interstellar.weapon'
    _description = 'Arma'

    name = fields.Char(string='Nombre')
    spaceships = fields.Many2many(
        comodel_name='interstellar.spaceship',
        relation='spaceship_weapon_rel',
        column1='weapon_id',
        column2='spaceship_id'
    )
