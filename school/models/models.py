# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student(models.Model):
    _name = 'school.student'
    _description = 'school.student'

    name = fields.Char(string='nombre', required=True, help='Esto es el nombre')
    birth_year = fields.Integer(string='cumpleaños', readonly=False)
    description = fields.Text()
    enrollment_date = fields.Date()
    last_login = fields.Datetime()
    is_student = fields.Boolean()
    photo = fields.Image(max_width=200, max_height=200)
    classroom = fields.Many2one(comodel_name='school.classroom')
    teachers = fields.Many2many('school.teacher', related='classroom.teachers', readonly=True)


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
