# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TaskQuestion(models.Model):
    _name = 'project.task_question'
    _description = 'Task Question'
    _rec_name = 'question'

    _sql_constraints = [
        ('unique_question',
         'unique(question)',
         'The rating question you are'
         ' trying to create already exists.')
    ]

    question = fields.Char(
        string='Question',
        help='Description of the asked question',
        required=True)

    default_question = fields.Boolean(
        string='Default Question',
        help='Questions that will be added to every newly created task.',
        default=False,
        required=True)

    task_questions = fields.Many2many(
        "project.task",
        "project_task_question_rel",
        "rating_questions",
        "task_questions",
        string="Task",
        readonly=True,
        required=False)

    @api.constrains('question')
    def _check_question(self):
        for record in self:
            if len(record.question) < 5:
                raise ValidationError(
                    "Question field should "
                    "have at least 5 characters."
                )

    def unlink(self):
        for record in self:
            if not record.task_questions:
                return super(TaskQuestion, self).unlink()
            else:
                raise ValidationError("The question is "
                                      "assigned to a task.")
