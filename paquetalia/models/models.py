from odoo import models, fields, api
from odoo.exceptions import ValidationError


class furgoneta(models.Model):
    _name = 'paquetalia.furgoneta'
    _description = 'Furgoneta'

    name = fields.Char(string='Nombre')
    matricula = fields.Char(string='Matricula')
    capacidad = fields.Integer(string='Capacidad', help='Volumen en m3', default=200)
    foto = fields.Image(string='Foto', max_width=200, max_height=200)
    paquetes = fields.Many2many(string='Paquetes', comodel_name='paquetalia.paquete')


class viaje(models.Model):
    _name = 'paquetalia.viaje'
    _description = 'Viaje'

    name = fields.Char(string='Nombre')
    identificador = fields.Integer(string='Identificador')
    volumen_ocupado = fields.Integer(string='Volumen ocupado', compute='_get_volumen_ocupado')
    conductor = fields.Many2one(string='Conductor', comodel_name='res.partner')
    furgoneta = fields.Many2one(string='Furgoneta', comodel_name='paquetalia.furgoneta')
    paquetes = fields.Many2many(string='Paquetes', comodel_name='paquetalia.paquete')

    # Calcular el volumen ocupado
    @api.depends('furgoneta')
    def _get_volumen_ocupado(self):
        for viaje in self:
            volumen_total = 0
            for paquete in viaje.paquetes:
                volumen_total += paquete.volumen
            viaje.volumen_ocupado = volumen_total

    # Restriccion de paquetes
    @api.constrains('paquetes')
    def _check_volumen_ocupado(self):
        for viaje in self:
            volumen_total = 0
            for paquete in viaje.paquetes:
                volumen_total += paquete.volumen
            if volumen_total > viaje.furgoneta.capacidad:
                raise ValidationError("Has superado el limite de carga")


class paquete(models.Model):
    _name = 'paquetalia.paquete'
    _description = 'Paquete'

    name = fields.Char(string='Nombre')
    identificador = fields.Char(string='Identificador')
    volumen = fields.Integer(string='Volumen', help='Volumen en m3')
