# -*- coding: utf-8 -*-

import logging
import re
import secrets

from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class student(models.Model):
    _name = 'school.student'
    _description = 'school.student'

    name = fields.Char(string='nombre', required=True, help='Esto es el nombre')
    birth_year = fields.Integer(string='cumpleaños', readonly=False)
    gender = fields.Selection([('male', 'Hombre'), ('female', 'Mujer'), ('other', 'Otro')],string='genero', default='male')
    password = fields.Char(default=lambda s: secrets.token_urlsafe(12))
    dni = fields.Char(string='DNI')
    description = fields.Text()
    enrollment_date = fields.Datetime(default=lambda self: fields.Datetime.now())
    last_login = fields.Datetime()
    level = fields.Selection([('1', '1'), ('2', '2')])
    is_student = fields.Boolean()
    photo = fields.Image(max_width=200, max_height=200)
    classroom = fields.Many2one(comodel_name='school.classroom', domain='[("level", "=", level)]', ondelete='set null',
                                help='La clase a la que va')
    teachers = fields.Many2many('school.teacher', related='classroom.teachers', readonly=True)

    @api.constrains('dni')
    def _check_dni(self):
        regex = re.compile('[0-9]{8}[a-z]\Z', re.IGNORECASE)
        for s in self:
            if regex.match(s.dni):
                _logger.warning('El dni hace match')
            else:
                raise ValidationError('El DNI no vale')

    _sql_constraints = [('dni_uniq', 'unique(dni)', 'El DNI no se puede repetir')]

    def regenerate_password(self):
        for s in self:
            password = secrets.token_urlsafe(12)
            s.write({'password': password})


class classroom(models.Model):
    _name = 'school.classroom'
    _description = "school.classroom"

    name = fields.Char()
    level = fields.Selection([('1', '1'), ('2', '2')])
    students = fields.One2many(comodel_name='school.student', inverse_name='classroom')
    teachers = fields.Many2many(comodel_name='school.teacher',
                                relation='teacher_classroom',
                                column1='teacher_id',
                                column2='classroom_id')

    teachers_ly = fields.Many2many(comodel_name='school.teacher',
                                   relation='teacher_classroom_ly',
                                   column1='teacher_id',
                                   column2='classroom_id')

    all_teachers = fields.Many2many('school.teacher', compute='_get_teachers')

    def _get_teachers(self):
        for t in self:
            t.all_teachers = t.teachers + t.teachers_ly


class teacher(models.Model):
    _name = "school.teacher"
    _description = "school.teacher"

    name = fields.Char()
    topic = fields.Char()
    phone = fields.Char()
    classrooms = fields.Many2many(comodel_name='school.classroom',
                                  relation='teacher_classroom',
                                  column2='teacher_id',
                                  column1='classroom_id')

    classrooms_ly = fields.Many2many(comodel_name='school.classroom',
                                     relation='teacher_classroom_ly',
                                     column2='teacher_id',
                                     column1='classroom_id')
