# -*- coding: utf-8 -*-
{
    'name': "Project Task Rating",

    'summary': """
        Rate a Task
    """,

    'description': """
        Rating can be triggered by any user who has access to the Task in the ERP by selecting an Action. Email is sent to customer, with the questions he must rate. Offer 5 star rating. Default questions are:
            - How did you like the communication with your developer on this task?
            - How would you assess the quality of the software written for this task?
            - Was the task delivered in satisfactory time according to your business needs?
            - Was the deployment process of the feature smooth and efficient?
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
