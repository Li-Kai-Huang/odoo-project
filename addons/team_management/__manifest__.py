# addons/team_management/__manifest__.py
{
    "name": "Team Management",
    "version": "17.0.1.0.0",
    "summary": "Basic team and member management for competition",
    "author": "Your Name",
    "website": "https://example.com",
    "license": "LGPL-3",
    "category": "Tools",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/team_views.xml",
        "views/member_views.xml",
    ],
    "installable": True,
    "application": True,
}
