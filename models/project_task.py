# -*- coding: utf-8 -*-

import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessError

HTTPS_INVALID_MESSAGE = r'Git/SonarQube/Testing links ' \
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
        default="",
        required=False)

    git_link = fields.Char(
        string="Git Link",
        required=False)

    sonarqube_link = fields.Char(
        string="SonarQube Link",
        required=False)

    test_site = fields.Char(
        string="Testing Link",
        help="Website where i can test the module.",
        required=False)

    rating_questions = fields.Many2many(
        "project.task_question",
        "project_task_question_rel",
        "task_questions",
        "rating_questions",
        string="Rating Questions",
        required=False)

    task_question_rating = fields.Many2many(
        "project.task_rate",
        string="Task Rating")

    def copy(self, default=None):
        default = dict(default or {})
        copy = super(ProjectTask, self).copy(default)

        for rating in copy.task_question_rating:
            if copy.id != rating.task_id:
                copy.write({"task_question_rating": [(3, rating.id)]})

        return copy

    def unlink(self):
        for record in self:
            remove_rating = ((2, x.id) for x in record.task_question_rating)
            record.write({'task_question_rating': remove_rating})
            return super(ProjectTask, self).unlink()

    @api.constrains("rating_questions")
    def check_rating(self):
        for record in self:
            questions = record.rating_questions
            ratings = record.env["project.task_rate"] \
                .search([('task_id', '=', record.id)])

            for rating in ratings:
                appear = False
                for question in questions:
                    if rating.question == question.question:
                        appear = True
                        break

                if not appear:
                    record.write({"task_question_rating": [(2, rating.id)]})

            for question in questions:
                stored_question = record.env["project.task_rate"] \
                    .search([('task_id', '=', record.id),
                             ('question', '=', question.question)])

                if not stored_question:
                    record.write({"task_question_rating": [(0, 0, {
                        'task_id': record.id,
                        'question': question.question,
                    })]})

    @api.constrains('git_link', 'sonarqube_link', 'test_site')
    def _check_git_link(self):
        for record in self:
            error_https(record.git_link)
            error_https(record.sonarqube_link)
            error_https(record.test_site)

    @api.depends('task_question_rating')
    def _average_rating(self):
        for record in self:

            rating, rated_questions = 0, 0

            for question in record.task_question_rating:
                if question.rating != "0":
                    rating += float(question.rating)
                    rated_questions += 1

            if rated_questions != 0:
                record.average_rating = rating / rated_questions

            else:
                record.average_rating = 0

    def rating_questions_form(self):
        for record in self:

            if record.env.user.has_group('project.group_project_manager'):

                view_id = record.env \
                    .ref('simplify_task_rating_v12c_1'
                         '.rating_questions_form').id
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
                    "Only users with a "
                    "system admin role can "
                    "access this view."
                )

    def rating_questions_mail(self):
        for record in self:
            if record.rating_questions \
                    and record.partner_id \
                    and record.user_id:
                record.ensure_one()
                ir_model_data = record.env['ir.model.data']
                try:
                    template_id = ir_model_data.get_object_reference(
                        'simplify_task_rating_v12c_1',
                        'rate_questions_email_template')[1]
                except ValueError:
                    template_id = False
                try:
                    compose_form_id = \
                        ir_model_data.get_object_reference(
                            'mail',
                            'email_compose_message_wizard_form')[1]
                except ValueError:
                    compose_form_id = False
                ctx = {
                    'default_model': 'project.task',
                    'default_res_id': record.ids[0],
                    'default_use_template': bool(template_id),
                    'default_template_id': template_id,
                    'default_composition_mode': 'comment',
                }
                return {
                    'name': 'Customer Rating',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'mail.compose.message',
                    'views': [(compose_form_id, 'form')],
                    'view_id': compose_form_id,
                    'target': 'new',
                    'context': ctx,
                }

            else:
                raise ValidationError(
                    "Please assign a developer, "
                    "customer and rating questions to this task "
                    "before contacting the "
                    "customer."
                )
