# -*- coding: utf-8 -*-

from odoo import models, fields
import secrets
import logging

_logger = logging.getLogger(__name__)


class student(models.Model):
    _name = 'school.student'
    _description = 'school.student'

    name = fields.Char(string='nombre', required=True, help='Esto es el nombre')
    birth_year = fields.Integer(string='cumpleaños', readonly=False)
    password = fields.Char(compute='_get_password')
    description = fields.Text()
    enrollment_date = fields.Date()
    last_login = fields.Datetime()
    is_student = fields.Boolean()
    photo = fields.Image(max_width=200, max_height=200)
    classroom = fields.Many2one(comodel_name='school.classroom')
    teachers = fields.Many2many('school.teacher', related='classroom.teachers', readonly=True)

    def _get_password(self):
        _logger.info('\033[94m' + str(self) + '\033[0m')
        for student in self:
            _logger.info('\033[94m' + str(student) + '\033[0m')
            student.password = secrets.token_urlsafe(12)


class classroom(models.Model):
    _name = 'school.classroom'
    _description = "school.classroom"

    name = fields.Char()
    students = fields.One2many(comodel_name='school.student', inverse_name='classroom')
    teachers = fields.Many2many(comodel_name='school.teacher',
                                relation='teacher_classroom',
                                column1='teacher_id',
                                column2='classroom_id')

    teachers_ly = fields.Many2many(comodel_name='school.teacher',
                                   relation='teacher_classroom_ly',
                                   column1='teacher_id',
                                   column2='classroom_id')

    delegate = fields.Many2one('school.student', compute='_get_delegate')
    all_teachers = fields.Many2many('school.teacher', compute='_get_teachers')

    def _get_delegate(self):
        for s in self:
            s.delegate = s.students[0].id

    def _get_teachers(self):
        for t in self:
            t.all_teachers = t.teachers + t.teachers_ly

class teacher(models.Model):
    _name = "school.teacher"
    _description = "school.teacher"

    name = fields.Char()
    classrooms = fields.Many2many(comodel_name='school.classroom',
                                  relation='teacher_classroom',
                                  column2='teacher_id',
                                  column1='classroom_id')

    classrooms_ly = fields.Many2many(comodel_name='school.classroom',
                                     relation='teacher_classroom_ly',
                                     column2='teacher_id',
                                     column1='classroom_id')
