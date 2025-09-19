# addons/team_management/__manifest__.py
{
    "name": "Team Management",
    "version": "17.0.1.0.0",
    "summary": "Basic team and member management for competition",
    "author": "likai_huang",
    "website": "no website",
    "license": "LGPL-3",
    "category": "Tools",
    "depends": ["base", "project"],
    "data": [
        "security/ir.model.access.csv",
        "views/team_views.xml",
        "views/member_views.xml",
        #"views/menu_dashboard.xml", # 已註解，因為 Odoo 17 不再支援 'board' 視圖。
    ],
    "installable": True,
    "application": True,
}