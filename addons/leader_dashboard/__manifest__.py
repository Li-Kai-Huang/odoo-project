
# addons/leader_dashboard/__manifest__.py
{
    'name': 'Leader Dashboard',
    'version': '1.0',
    'summary': 'A custom dashboard for leaders, integrating data from multiple modules.',
    'author': 'Your Name',
    'website': 'https://www.odoo.com',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'depends': [
        'base',
        'team_management',
        'parts_inventory',
        'project_team_integration',
        'web',
    ],
    'data': [
        'views/dashboard_view.xml',
        'views/dashboard_menu.xml',
        'security/ir.model.access.csv', # 如果有需要新增權限規則
    ],
    'assets': {
        # 這裡將來可以放您用 JavaScript 寫的客製化 UI
    },
    'installable': True,
    'application': True,
}