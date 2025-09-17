# addons/parts_inventory/__manifest__.py
{
    "name": "Parts Inventory",
    "version": "0.1",
'depends': ['base', 'product', 'team_management'],  # 要有 product
"data": [
    "security/security.xml",
    "security/ir.model.access.csv",
    # 報表（讓表單按鈕能找到 action）
    "reports/templates.xml",
    "reports/report.xml",

    # 其他 action / view
    "views/stock_move_views.xml",
    "views/wizard_views.xml",
    "views/part_views.xml",
    "views/product_views.xml",
    "views/task_views.xml",
    "views/stock_request_views.xml",
    'data/sequence.xml',
    "views/menu.xml",
],

    "application": True,
}
