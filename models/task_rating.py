# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

AVAILABLE_RATINGS = [
    ('0', "Can't decide"),
    ('1', 'Very Dissatisfied'),
    ('2', 'Dissatisfied'),
    ('3', 'Fair'),
    ('4', 'Satisfied'),
    ('5', 'Very Satisfied'),
]


class TaskRating(models.Model):
    _name = 'project.task_rating'
    _description = 'Task Rating'

    _sql_constraints = [
        ('unique_question',
         'unique(question)',
         'The ratings question you are'
         ' trying to create already exists.')
    ]

    question = fields.Char(
        string='Question',
        help='Description of the asked question',
        required=True)

    rating = fields.Selection(
        AVAILABLE_RATINGS,
        string='Rating',
        index=True,
        default=AVAILABLE_RATINGS[0][0])

    default_question = fields.Boolean(
        string='Default Question',
        help='Questions that will be added to every newly created task.',
        default=False,
        required=True)

    def name_get(self):
        name = []
        for record in self:
            name.append((
                record.id,
                record.question))
        return name

    @api.constrains('question')
    def _check_field_of_study(self):
        for record in self:
            if len(record.question) < 10:
                raise ValidationError(
                    "Question field of study should "
                    "have at least 10 characters."
                )
