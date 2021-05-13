# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal


class WebsiteRatingQuestion(CustomerPortal):

    @http.route(['/my/task/<int:task_id>/rate'],
                type='http', auth="public", website=True, csrf=False)
    def portal_my_task_rate(self, task_id, access_token=None, **kw):
        try:
            task_sudo = self. \
                _document_check_access('project.task', task_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        for attachment in task_sudo.attachment_ids:
            attachment.generate_access_token()

        values = self._task_get_page_view_values(task_sudo, access_token, **kw)

        num_questions = 0
        try:
            for i in range(1, len(task_sudo.task_question_rating) + 1):
                if int(kw["q_" + str(i)]) in range(0, 6):
                    num_questions += 1
        finally:
            if num_questions == len(task_sudo.task_question_rating):
                num_questions = 0
                for rating_question in task_sudo.task_question_rating:
                    rating_question.rating = kw["q_" + str(num_questions + 1)]
                    num_questions += 1

            if num_questions == len(task_sudo.task_question_rating) \
                    and task_sudo.additional_notes != kw["additional_notes"]:
                task_sudo.write({"additional_notes": kw["additional_notes"]})

        if num_questions != len(task_sudo.task_question_rating):
            values.update({'error': "Error, please try again.",
                           'error_message': "Error invalid input, "
                                            "please try again."})
        else:
            values.update({'success': "Thank you for rating the task.",
                           'success_message': "Thank you for rating "
                                              "the task."})
            task_sudo.customer_rated_mail()

        return request \
            .render("simplify_task_rating_v12c_1.portal_my_task_rq", values)
