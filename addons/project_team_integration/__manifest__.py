# -*- coding: utf-8 -*-
{
    'name': "Project Team Integration",
    'summary': "Integrates Project and Task management with Team Management.",
    'description': """
        This module adds new fields and views to the Odoo Project and Task modules
        to support team-based task assignment and progress tracking.
    """,
    'author': "Your Name",
    'website': "http://www.yourwebsite.com",
    'category': 'Project',
    'version': '17.0.1.0.0',
    'depends': ['project', 'team_management'], # 核心：明確定義模組依賴
    'data': [
        'views/project_task_views.xml',
    ],
    'license': 'AGPL-3',
}