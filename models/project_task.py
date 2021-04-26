# -*- coding: utf-8 -*-

import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessError

HTTPS_INVALID_MESSAGE = r'Git/SonarQube/Testing site link ' \
                        r'are not valid, e.g https://www.example.com.'

link_pattern = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}'
    r'[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def check_https(link):
    if not link:
        return True

    elif re.match(link_pattern, link) is not None:
        return True

    else:
        return False


def error_https(link):
    if check_https(link) is False:
        raise ValidationError(
            HTTPS_INVALID_MESSAGE
        )


class ProjectTask(models.Model):
    _inherit = "project.task"

    average_rating = fields.Float(
        string="Average Rating",
        default=0,
        compute="_average_rating",
        required=True)

    additional_notes = fields.Text(
        string="Additional Notes",
        help="Add additional Notes",
        required=False)

    git_link = fields.Char(
        string="GitHub/GitLab Link",
        required=False)

    sonarqube_link = fields.Char(
        string="SonarQube Link",
        required=False)

    test_site = fields.Char(
        string="Testing Site",
        help="Website where i can test the module.",
        required=False)

    functionality_specification = fields.Many2many(
        'ir.attachment',
        'class_ir_attachments_rel',
        'class_id',
        'attachment_id',
        string="Functionality Specification",
        required=False)

    rating_questions = fields.Many2many(
        "project.task_rating",
        string="Rating Questions",
        required=False)

    @api.model
    def create(self, values):
        res = super(ProjectTask, self).create(values)
        def_rate_quest = self.env["project.task_rating"].search([
            ('default_question', '=', True)
        ])
        res.rating_questions = def_rate_quest
        return res

    @api.constrains('git_link', 'sonarqube_link', 'test_site')
    def _check_git_link(self):
        for record in self:
            error_https(record.git_link)
            error_https(record.sonarqube_link)
            error_https(record.test_site)

    @api.depends('rating_questions')
    def _average_rating(self):
        for record in self:

            rating, rated_questions = 0, 0

            for question in record.rating_questions:
                if question.rating != "0":
                    rating += float(question.rating)
                    rated_questions += 1

            if rated_questions != 0:
                record.average_rating = rating / rated_questions

            else:
                record.average_rating = 0

    def rating_questions_form(self):
        for record in self:

            if record.env.user.has_group('base.group_no_one'):

                view_id = \
                    record.env.ref('simplify_task_rating_v12c_1.rating_questions_form').id
                context = record._context.copy()

                return {
                    'name': 'Rating Questions',
                    'view_type': 'form',
                    'view_mode': 'tree',
                    'views': [(view_id, 'form')],
                    'res_model': 'project.task',
                    'view_id': view_id,
                    'type': 'ir.actions.act_window',
                    'res_id': record.id,
                    'target': 'new',
                    'context': context,
                }

            else:
                raise AccessError(
                    "Only users who have "
                    "dev mode access can "
                    "access this view."
                )
