# -*- coding: utf-8 -*-

from datetime import date

from odoo import models, fields, api


class player(models.Model):
    _name = 'interstellar.player'
    _description = 'Jugador de Interstellar'

    # Datos del jugador
    photo = fields.Image(string='Foto', max_width=200, max_height=200)
    photo_mini = fields.Image(related='photo', string='Foto mini', max_width=50, max_height=50)
    name = fields.Char(string='Nombre')
    last_name = fields.Char(string='Apellidos')
    birth_date = fields.Date(string='Fecha de nacimiento')
    age = fields.Integer(string='Edad', compute='_get_age')
    gender = fields.Selection([('male', 'Hombre'), ('female', 'Mujer'), ('other', 'Otro')])

    # Datos del juego
    total_planets = fields.Integer(string='Total de planetas', compute='_get_player_planets')
    attack = fields.Integer(string='Ataque', compute='_get_player_attack')
    defense = fields.Integer(string='Defensa', compute='_get_player_defense')
    health = fields.Integer(string='Salud', compute='_get_player_health')

    # Relaciones
    planets = fields.One2many(
        string='Planetas',
        comodel_name='interstellar.planet',
        inverse_name='player',
        readonly=True
    )

    # Función que calcula la edad a partir de la fecha de nacimiento
    @api.depends('birth_date')
    def _get_age(self):
        for item in self:
            today = date.today()
            if item.birth_date:
                item.age = today.year - item.birth_date.year
            else:
                item.age = 1

    # Función que calcula el total de planetas
    @api.depends('planets')
    def _get_player_planets(self):
        for player in self:
            total = 0
            for planet in player.planets:
                total += 1
            player.total_planets = total

    # Función que calcula el ataque total del jugador
    @api.depends('planets')
    def _get_player_attack(self):
        for player in self:
            attack = 0
            for planet in player.planets:
                attack += planet.attack
            player.attack = attack

    # Función que calcula la defensa total del jugador
    @api.depends('planets')
    def _get_player_defense(self):
        for player in self:
            defense = 0
            for planet in player.planets:
                defense += planet.defense
            player.defense = defense

    # Función que calcula la salud total del jugador
    @api.depends('planets')
    def _get_player_health(self):
        for player in self:
            health = 0
            for planet in player.planets:
                health += planet.health
            player.health = health


class planet(models.Model):
    _name = 'interstellar.planet'
    _description = 'Planeta'

    # Información del planeta
    photo = fields.Image(string='Foto', max_width=250, max_height=250)
    photo_mini = fields.Image(related='photo', string='Foto mini', max_width=50, max_height=50)
    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')
    dimension = fields.Integer(string='Dimension', help='Dimension del planeta en kilómetros')
    race = fields.Char(string='Raza')
    age = fields.Integer(string='Edad', )

    # Estadísticas del planeta
    minerals = fields.Integer(default=1000, string='Minerales', readonly=True)
    materials = fields.Integer(default=1000, string='Materiales', readonly=True)
    health = fields.Integer(string='Salud', compute='_get_planet_health')
    attack = fields.Integer(string='Ataque', compute='_get_planet_attack')
    defense = fields.Integer(string='Defensa', compute='_get_planet_defense')

    # Relaciones
    player = fields.Many2one(
        string='Jugador',
        comodel_name='interstellar.player'
    )

    spaceships = fields.One2many(
        string='Naves',
        comodel_name='interstellar.planet_spaceship',
        inverse_name='planet'
    )

    # Función que calcula la salud total del planeta
    @api.depends('spaceships')
    def _get_planet_health(self):
        for planet in self:
            health = 2000
            for relation in planet.spaceships:
                health += relation.spaceship.health + relation.weapon_one.health + relation.weapon_two.health
            planet.health = health

    # Función que calcula el ataque total del planeta
    @api.depends('spaceships')
    def _get_planet_attack(self):
        for planet in self:
            attack = 0
            for relation in planet.spaceships:
                attack += relation.spaceship.attack + relation.weapon_one.attack + relation.weapon_two.attack
            planet.attack = attack

    # Función que calcula la defensa total del planeta
    @api.depends('spaceships')
    def _get_planet_defense(self):
        for planet in self:
            defense = 0
            for relation in planet.spaceships:
                defense = relation.spaceship.attack + relation.weapon_one.defense + relation.weapon_two.defense
            planet.defense = defense


class planet_spaceship(models.Model):
    _name = 'interstellar.planet_spaceship'
    _description = 'Relación de los planetas y las naves'

    # Relaciones
    planet = fields.Many2one(
        string='Planeta', comodel_name='interstellar.planet')
    spaceship = fields.Many2one(
        string='Nave', comodel_name='interstellar.spaceship')
    weapon_one = fields.Many2one(string='Arma 1', comodel_name='interstellar.weapon')
    weapon_two = fields.Many2one(string='Arma 2', comodel_name='interstellar.weapon')

    # Imagenes
    image_spaceship = fields.Image(string='Imagen nave', related='spaceship.photo_mini')
    image_weapon_one = fields.Image(string='Imagen arma uno', related='weapon_one.photo_mini')
    image_weapon_two = fields.Image(string='Imagen arma dos', related='weapon_two.photo_mini')


class spaceship(models.Model):
    _name = 'interstellar.spaceship'
    _description = 'Nave'

    # Información de la nave
    photo = fields.Image(string='Foto', max_width=250, max_height=250)
    photo_mini = fields.Image(related='photo', string='Foto mini', max_width=50, max_height=50)
    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')

    # Estadísticas de la nave
    attack = fields.Integer(string='Ataque')
    defense = fields.Integer(string='Defensa')
    health = fields.Integer(string='Salud')
    mineral_cost = fields.Integer(string='Cos. minerales', help='Coste de minerales')
    material_cost = fields.Integer(string='Cos. materiales', help='Coste de materiales')
    mineral_collection = fields.Integer(string='Rec. minerales', help='Recolección de minerales')
    material_collection = fields.Integer(string='Rec. materiales', help='Recolección de materiales')


class weapon(models.Model):
    _name = 'interstellar.weapon'
    _description = 'Arma'

    # Información del arma
    photo = fields.Image(string='Foto', max_width=200, max_height=200)
    photo_mini = fields.Image(related='photo', string='Foto mini', max_width=50, max_height=50)
    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')

    # Estadísticas del arma
    attack = fields.Integer(string='Ataque')
    defense = fields.Integer(string='Defensa')
    health = fields.Integer(string='Salud')
    reload = fields.Integer(string='Recarga')
