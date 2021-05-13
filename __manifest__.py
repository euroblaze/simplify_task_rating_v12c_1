# -*- coding: utf-8 -*-
{
    'name': "Project Task Rating",

    'summary': """
        Rate a Task
    """,

    'description': """
    - User who has project manager or system admin access is allowed to asign rating questions for a specific task with a click of the button Rating Questions available in the header of the Task Form View.
    - The admin or project manager can contact the customer by clicking the button Rating to Customer available in the header of the Task Form View, giving the customer a notification in his mail box that the task has been finished and in the context of the mail the rating questions are mentioned.
    - Customer can give a rating from 0 to 5 for every single rating question and add aditional notes. This feature is available only for portal users.
    - Average Rating is shown on the Kanban View.
    - In Project --> Configuration a menu item (Rating Questions) is available for adding, editing and deleting rating questions.
    - Task Links page exists on every single task. Fields such as Git, SonarQube and Testing website links are available.
    """,

    'author': "Simplify ERP®",
    'website': "https://simplify-erp.com/",
    'category': 'Project Task',
    'version': '1.0',
    'depends': ['base', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/project_task_rate_template.xml',
        'data/project_task_rate_customer_template.xml',
        'views/project_task_question_views.xml',
        'views/project_task_views.xml',
        'views/portal_project_task_views.xml',
        'views/project_task_rate_views.xml',
        'views/views.xml',
        'views/assets.xml',
    ],
    'installable': True,
    'auto_install': False,
}
