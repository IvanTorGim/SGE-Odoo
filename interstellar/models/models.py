# -*- coding: utf-8 -*-
import random
from datetime import date, datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class player(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    # _description = 'Jugador de Interstellar'

    # Datos del jugador
    # photo = fields.Image(string='Foto', max_width=200, max_height=200)
    photo_mini = fields.Image(related='image_128', string='Foto mini', max_width=50, max_height=50)
    # name = fields.Char(string='Nombre')
    last_name = fields.Char(string='Apellidos')
    birth_date = fields.Date(string='Fecha de nacimiento')
    age = fields.Integer(string='Edad', compute='_get_age', store='True')
    gender = fields.Selection([('male', 'Hombre'), ('female', 'Mujer'), ('other', 'Otro')])

    # Datos del juego
    total_planets = fields.Integer(string='Total de planetas', compute='_get_player_planets')
    planet_names = fields.Char(string="Nombre de los planetas", compute='_get_planet_names')
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
            player.total_planets = len(player.planets)

    # Función que calcula el nombre de los planetas
    @api.depends('planets')
    def _get_planet_names(self):
        self.planet_names = str.join(', ', self.planets.mapped(lambda p: str(p.name)))

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
        comodel_name='res.partner'
    )

    spaceships = fields.One2many(
        string='Naves',
        comodel_name='interstellar.planet_spaceship',
        inverse_name='planet'
    )

    # Función CRON actualiza los minerales y materiales
    @api.model
    def update_resources(self):
        planets = self.env['interstellar.planet'].search([])
        for planet in planets:
            if len(planet.spaceships) > 0:
                for planet_spaceship in planet.spaceships:
                    planet.materials += planet_spaceship.spaceship.material_collection
                    planet.minerals += planet_spaceship.spaceship.mineral_collection

    # Función que reinicie las estadísticas y la flota de los planet
    @api.onchange('player')
    def _on_change_player(self):
        self.write({'minerals': 1000, 'materials': 1000})
        for spaceship in self.spaceships:
            self.write({'spaceships': [(2, spaceship.id, 0)]})

    # Función que calcula la salud total del planeta
    @api.depends('spaceships', 'player')
    def _get_planet_health(self):
        for planet in self:
            health = planet.health
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

    # Campos de la batalla
    name = fields.Char(string='Nombre', default=lambda b: "Batalla " + str(datetime.now()), readonly=True)
    battle_state = fields.Selection(string='Estado de la batalla',
                                    selection=[('preparation', 'Preparación'), ('active', 'Activa'),
                                               ('finished', 'Finalizada')], default='preparation', readonly=True)
    winner = fields.Char(string='Ganador', default="", readonly=True)
    battle_record = fields.One2many(comodel_name='interstellar.battle_record', inverse_name='battle')

    # Campos del jugador 1
    player_one = fields.Many2one(string='Player1', comodel_name='res.partner',
                                 domain=[('is_active', '=', True)])
    planet_one = fields.Many2one(string='Planeta', comodel_name='interstellar.planet')
    attack_one = fields.Integer(string='Ataque')
    defense_one = fields.Integer(string='Defensa')
    health_one = fields.Integer(string='Salud')
    planets_one = fields.One2many(related='player_one.planets')

    # Campos del planeta elegido

    # Campos del jugador 1
    player_two = fields.Many2one(string='Player2', comodel_name='res.partner',
                                 domain=[('is_active', '=', True)])
    planet_two = fields.Many2one(string='Planeta', comodel_name='interstellar.planet')
    attack_two = fields.Integer(string='Ataque')
    defense_two = fields.Integer(string='Defensa')
    health_two = fields.Integer(string='Salud')

    # Función que me muestra los planetas del jugador uno
    @api.onchange('player_one')
    def _onchange_player_one(self):
        for battle in self:
            return {'domain': {'planet_one': [('player.id', '=', battle.player_one.id)]}}

    # Función que me muestra los planetas del jugador dos
    @api.onchange('player_two')
    def _onchange_player_two(self):
        for battle in self:
            return {'domain': {'planet_two': [('player.id', '=', battle.player_two.id)]}}

    # Función que muestra el ataque, defensa y salud
    @api.onchange('planet_one', 'planet_two')
    def _onchange(self):
        self.attack_one = self.planet_one.attack
        self.defense_one = self.planet_one.defense
        self.health_one = self.planet_one.health
        self.attack_two = self.planet_two.attack
        self.defense_two = self.planet_two.defense
        self.health_two = self.planet_two.health

    # Restricción para no elegir el mismo jugador
    @api.constrains('player_one', 'player_two')
    def _check_distinct_player(self):
        for battle in self:
            if battle.player_one.id == battle.player_two.id:
                raise ValidationError('Tienes que elegir diferentes jugadores')

    # Restricción para no elegir el mismo jugador
    @api.constrains('planet_one', 'planet_two')
    def _check_spaceships(self):
        if len(self.planet_one.spaceships) < 1 or len(self.planet_two.spaceships) < 1:
            raise ValidationError('Tienes que elegir planetas con una flota de naves')

    # Restricción para no elijan un jugador sin naves
    # @api.constrains('health_one', 'health_two')
    # def _check_spaceships(self):
    #    if self.health_one <= 0 or self.health_two <= 0:
    #       raise ValidationError('No pueden pelear sin naves')

    # todo crear las funciones

    # Función que pone nombre a la batalla
    def _get_name_battle(self):
        for battle in self:
            battle.name = battle.player_one.name + battle.player_two.name + str(date.today())

    # Función que calcula la batalla
    def start_battle(self):
        self.battle_state = 'active'
        turn = 0
        health_planet_one = self.health_one
        health_planet_two = self.health_two
        while health_planet_one > 0 and health_planet_two > 0:
            randomTurn = random.randint(0, 1)
            turn += 1
            if randomTurn == 0:
                damage = self.calculate_damage(self.attack_one, self.defense_two)
                health_planet_two -= damage
                self.env['interstellar.battle_record'].create({
                    'battle': self.id,
                    'turn': turn,
                    'attacker_name': self.player_one.name,
                    'attacker_health': health_planet_one,
                    'attacker_damage': damage,
                    'defensor_name': self.player_two.name,
                    'defensor_health': health_planet_two
                })
            else:
                damage = self.calculate_damage(self.attack_two, self.defense_one)
                health_planet_one -= damage
                self.env['interstellar.battle_record'].create({
                    'battle': self.id,
                    'turn': turn,
                    'attacker_name': self.player_two.name,
                    'attacker_health': health_planet_two,
                    'attacker_damage': damage,
                    'defensor_name': self.player_one.name,
                    'defensor_health': health_planet_one
                })
        self.battle_state = 'finished'
        if health_planet_one < 0:
            self.winner = "Ha ganado el jugador 2, conquista el planeta " + self.planet_one.name
            self.planet_one.write({'minerals': 500, 'materials': 500, 'spaceships': [6, 0, 0]})
            self.player_two.write({'planets': [(4, self.planet_one.id)]})
        else:
            self.winner = "Ha ganado el jugador 1, conquista el planeta " + self.planet_two.name
            self.planet_two.write({'minerals': 500, 'materials': 500, 'spaceships': [6, 0, 0]})
            self.player_one.write({'planets': [(4, self.planet_two.id)]})

    # Calcula el daño pasandole el ataque y la defensa
    def calculate_damage(self, attacker_attack, defensor_defense):
        damage = (attacker_attack * 5 * random.randint(50, 100)) / defensor_defense
        return 0 if damage < 0 else damage

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


class battle_record(models.Model):
    _name = 'interstellar.battle_record'
    _description = 'Registros de la batalla'

    # Relación con batalla
    battle = fields.Many2one(comodel_name='interstellar.battle')
    turn = fields.Integer(string="Turno")

    # Campos del jugador que ataca
    attacker_name = fields.Char(string='Atacante')
    attacker_health = fields.Integer(string='Salud atacante')
    attacker_damage = fields.Integer(string='Daño atacante')

    # Campos del jugador que defiende
    defensor_name = fields.Char(string='Defensor')
    defensor_health = fields.Integer(string='Salud defensor')
