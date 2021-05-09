# -*- coding: utf-8 -*-

from odoo import models, fields, api

AVAILABLE_RATINGS = [
    ('0', "Can't decide"),
    ('1', 'Very Dissatisfied'),
    ('2', 'Dissatisfied'),
    ('3', 'Fair'),
    ('4', 'Satisfied'),
    ('5', 'Very Satisfied'),
]


class TaskRating(models.Model):
    _name = 'project.task_rate'
    _description = 'Task Rating'

    task_id = fields.Integer(
        string="Task Id",
        required=True)

    question = fields.Char(
        string="Question",
        required=True)

    rating = fields.Selection(
        AVAILABLE_RATINGS,
        string='Rating',
        index=True,
        default=AVAILABLE_RATINGS[0][0],
        required=True)
