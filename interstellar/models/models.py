# -*- coding: utf-8 -*-

from datetime import date, datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class player(models.Model):
    _name = 'interstellar.player'
    _description = 'Jugador de Interstellar'

    # Datos del jugador
    photo = fields.Image(string='Foto', max_width=200, max_height=200)
    photo_mini = fields.Image(related='photo', string='Foto mini', max_width=50, max_height=50)
    name = fields.Char(string='Nombre')
    last_name = fields.Char(string='Apellidos')
    birth_date = fields.Date(string='Fecha de nacimiento')
    age = fields.Integer(string='Edad', compute='_get_age', store='True')
    gender = fields.Selection([('male', 'Hombre'), ('female', 'Mujer'), ('other', 'Otro')])

    # Datos del juego
    total_planets = fields.Integer(string='Total de planetas', compute='_get_player_planets')
    attack = fields.Integer(string='Ataque', compute='_get_player_attack')
    defense = fields.Integer(string='Defensa', compute='_get_player_defense')
    health = fields.Integer(string='Salud', compute='_get_player_health')
    is_active = fields.Boolean(string='Activo', compute='_get_is_active', store='True')

    # Relaciones
    planets = fields.One2many(
        string='Planetas',
        comodel_name='interstellar.planet',
        inverse_name='player'
    )

    # Función que calcula si estás activo en función de si tienes planetas o no
    @api.depends('total_planets')
    def _get_is_active(self):
        for player in self:
            if player.total_planets > 0:
                player.is_active = True
            else:
                player.is_active = False

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
    level = fields.Integer(string='Nivel')

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
                health += relation.spaceship.health
                for weapon in relation.weapons:
                    health += weapon.health
            planet.health = health

    # Función que calcula el ataque total del planeta
    @api.depends('spaceships')
    def _get_planet_attack(self):
        for planet in self:
            attack = 0
            for relation in planet.spaceships:
                attack += relation.spaceship.attack
                for weapon in relation.weapons:
                    attack += weapon.attack
            planet.attack = attack

    # Función que calcula la defensa total del planeta
    @api.depends('spaceships')
    def _get_planet_defense(self):
        for planet in self:
            defense = 0
            for relation in planet.spaceships:
                defense += relation.spaceship.defense
                for weapon in relation.weapons:
                    defense += weapon.defense
            planet.defense = defense


class planet_spaceship(models.Model):
    _name = 'interstellar.planet_spaceship'
    _description = 'Relación de los planetas y las naves'

    # Información nave
    actual_weight = fields.Integer(string='Peso actual', compute='_get_actual_weight')
    max_weight = fields.Integer(string='Peso max', related='spaceship.max_weight')
    total_weapons = fields.Integer(string='Total armas', compute='_get_total_weapons')
    spaceship_level = fields.Integer(string='Nivel nave', related='spaceship.level')

    # Relaciones
    planet = fields.Many2one(
        string='Planeta', comodel_name='interstellar.planet')
    spaceship = fields.Many2one(
        string='Nave', comodel_name='interstellar.spaceship')
    weapons = fields.Many2many(string='Armas', domain="[('level', '<=', spaceship_level)]",
                               comodel_name='interstellar.weapon', relation='spaceship_weapon',
                               column1='weapon_id', column2='spaceship_id')

    # OnChange para que me calcule el peso actual
    @api.onchange('spaceship')
    def _onchange_spaceship(self):
        self.actual_weight = self.spaceship.weight

    # Función para calcular el peso actual de la nave
    @api.depends('weapons')
    def _get_actual_weight(self):
        for planet_spaceship in self:
            total_weight = planet_spaceship.spaceship.weight
            for weapon in planet_spaceship.weapons:
                total_weight += weapon.weight
            planet_spaceship.actual_weight = total_weight

    # Función para calcular el total de armas por nave
    @api.depends('weapons')
    def _get_total_weapons(self):
        for planet_spaceship in self:
            total = 0
            for weapon in planet_spaceship.weapons:
                total += 1
            planet_spaceship.total_weapons = total

    # Restricción para que no puedan añadir armas si supera el peso máximo
    @api.constrains('weapons')
    def _check_add_weapons(self):
        for planet_spaceship in self:
            if planet_spaceship.actual_weight > planet_spaceship.max_weight:
                raise ValidationError('Has superado el límite de peso')

    # Restricción para que no puedan comprar naves si no tienen recursos
    @api.constrains('spaceship')
    def _check_minerals_materials(self):
        for planet_spaceship in self:
            mineral = planet_spaceship.spaceship.mineral_cost
            material = planet_spaceship.spaceship.material_cost
            if mineral > planet_spaceship.planet.minerals:
                raise ValidationError('No tienes suficiente mineral')
            elif material > planet_spaceship.planet.materials:
                raise ValidationError('No tienes suficiente material')
            else:
                planet_spaceship.planet.minerals -= mineral
                planet_spaceship.planet.materials -= material


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
    weight = fields.Integer(string='Peso nave')
    max_weight = fields.Integer(string='Peso Máximo')
    level = fields.Integer(string='Nivel')
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
    weight = fields.Integer(string='Peso')
    level = fields.Integer(string='Nivel')


class battle(models.Model):
    _name = 'interstellar.battle'
    _description = 'Batalla'

    name = fields.Char(string='name', default=lambda b: "Batalla " + str(datetime.now()), readonly=True)
    player_one = fields.Many2one(string='Player1', comodel_name='interstellar.player',
                                 domain=[('is_active', '=', True)])
    attack_one = fields.Integer(string='Ataque', related='player_one.attack')
    defense_one = fields.Integer(string='Defensa', related='player_one.defense')
    health_one = fields.Integer(string='Salud', related='player_one.health')
    planets_one = fields.One2many(string='Planetas', related='player_one.planets')

    player_two = fields.Many2one(string='Player2', comodel_name='interstellar.player',
                                 domain=[('is_active', '=', True)])
    attack_two = fields.Integer(string='Ataque', related='player_two.attack')
    defense_two = fields.Integer(string='Defensa', related='player_two.defense')
    health_two = fields.Integer(string='Salud', related='player_two.health')
    planets_two = fields.One2many(string='Planetas', related='player_two.planets')

    # Restricción para no elegir el mismo jugador
    @api.constrains('player_one')
    def _check_distinct_player(self):
        for battle in self:
            if battle.player_one == battle.player_two:
                raise ValidationError('Tienes que elegir diferentes jugadores')

    # Restricción para no elegir el mismo jugador
    @api.constrains('player_two')
    def _check_distinct_player(self):
        for battle in self:
            if battle.player_two == battle.player_one:
                raise ValidationError('Tienes que elegir diferentes jugadores')

    # todo crear las funciones

    # crear nombre de la batalla
    def _get_name_battle(self):
        for battle in self:
            name = battle.player_one.name + battle.player_two.name + str(date.today())

    def start_battle(self):
        for battle in self:
            damage_one = battle.player_two.attack - battle.player_one.defense
            damage_two = battle.player_one.attack - battle.player_two.defense
            if damage_one > 0:
                battle.player_one.health -= damage_one
            if damage_two > 0:
                battle.player_two.health -= damage_two

    def view_player_one(self):
        for battle in self:
            action = self.env.ref('interstellar.action_player_window_battle').read()[0]
            action['res_id'] = battle.player_one.id
            return action

    def view_player_two(self):
        for battle in self:
            action = self.env.ref('interstellar.action_player_window_battle').read()[0]
            action['res_id'] = battle.player_two.id
            return action


