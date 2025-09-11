# addons/parts_inventory/__manifest__.py
{
    "name": "Parts Inventory",
    "version": "0.1",
'depends': ['base', 'product', 'team_management'],  # 要有 product
'data': [
    'security/ir.model.access.csv',
    'views/part_views.xml',
    'views/stock_move_views.xml',
    'views/wizard_views.xml',
    'views/product_views.xml',
    'views/menu.xml',              # ← 放最後
],
    "application": False,
}
