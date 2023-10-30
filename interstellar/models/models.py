# -*- coding: utf-8 -*-

from odoo import models, fields, api


class player(models.Model):
    _name = 'interstellar.player'
    _description = 'Jugador de Interstellar'

    name = fields.Char(string='Nombre')
    birthdate = fields.Date(string='Fecha de nacimiento')

    planets = fields.One2many(
        string='Planetas',
        comodel_name='interstellar.planet',
        inverse_name='player'
    )


class planet(models.Model):
    _name = 'interstellar.planet'
    _description = 'Planeta'

    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')
    dimension = fields.Integer(string='Dimension', help='Dimension del planeta en kilómetros')
    race = fields.Char(string='Raza')
    age = fields.Integer(string='Edad', )

    minerals = fields.Integer(default=100, string='Minerales')
    energy = fields.Integer(default=500, string='Energía')
    construction_materials = fields.Integer(default=500, string='Materiales de construcción')

    player = fields.Many2one(
        string='Jugador',
        comodel_name='interstellar.player'
    )

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
    description = fields.Text(string='Descripción')
    attack = fields.Integer(string='Ataque')
    health = fields.Integer(string='salud')
    mineral_cost = fields.Integer(string='Coste en minerales')
    material_cost = fields.Integer(string='Coste en materiales')
    mineral_collection = fields.Integer(string='Recolección de minerales')
    material_collection = fields.Integer(string='Recolección de materiales')

    planets = fields.Many2many(
        string='Planetas',
        comodel_name='interstellar.planet',
        relation='planet_spaceship_rel',
        column1='spaceship_id',
        column2='planet_id'
    )
    weapons = fields.Many2many(
        string='Armas',
        comodel_name='interstellar.weapon',
        relation='spaceship_weapon_rel',
        column1='spaceship_id',
        column2='weapon_id'
    )


class weapon(models.Model):
    _name = 'interstellar.weapon'
    _description = 'Arma'

    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')
    attack = fields.Integer(string='Ataque')
    reload = fields.Integer(string='Recarga')

    spaceships = fields.Many2many(
        string='Naves',
        comodel_name='interstellar.spaceship',
        relation='spaceship_weapon_rel',
        column1='weapon_id',
        column2='spaceship_id'
    )
