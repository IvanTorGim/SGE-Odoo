# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class buy_spaceship(models.TransientModel):
    _name = 'interstellar.buy_spaceship'

    actual_weight = fields.Integer(string='Peso actual', compute="_get_actual_weight")
    max_weight = fields.Integer(string='Peso max', related='spaceship.max_weight')
    spaceship_level = fields.Integer(string='Nivel nave', related='spaceship.level')

    # Relaciones
    planet = fields.Many2one(
        string='Planeta', comodel_name='interstellar.planet', readonly=True)
    spaceship = fields.Many2one(
        string='Nave', comodel_name='interstellar.spaceship')
    weapons = fields.Many2many(string='Armas',
                               comodel_name='interstellar.weapon')

    # Función que me crea la nave en el planeta donde se inicia la compra
    def buy_spaceship(self):
        self.env['interstellar.planet_spaceship'].create({
            'planet': self.planet.id,
            'spaceship': self.spaceship.id,
            'weapons': [(6, 0, self.weapons.ids)]
        })

    # OnChange para que me calcule el peso actual
    @api.depends('spaceship', 'weapons')
    def _get_actual_weight(self):
        self.actual_weight = self.spaceship.weight
        for planet_spaceship in self:
            for weapon in planet_spaceship.weapons:
                self.actual_weight += weapon.weight

    # Restricción para que elija una nave
    @api.constrains('spaceship')
    def _check_spaceship(self):
        if self.spaceship.id <= 0:
            raise ValidationError("Elige una nave")

    # Restricción para que no puedan añadir armas si supera el peso máximo
    @api.constrains('weapons')
    def _check_add_weapons(self):
        for planet_spaceship in self:
            if planet_spaceship.actual_weight > planet_spaceship.max_weight:
                raise ValidationError('Has superado el límite de peso')
