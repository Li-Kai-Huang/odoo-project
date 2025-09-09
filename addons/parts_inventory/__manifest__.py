# -*- coding: utf-8 -*-
{
    "name": "Parts Inventory",
    "summary": "Manage parts and stock moves (lightweight flow)",
    "description": "Simple parts inventory with in/out moves for Week 2 Day 09.",
    "author": "likai_huang",
    "version": "0.1",
    "website": "https://example.com",
    "category": "Inventory",
    "depends": ["base", "team_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/part_views.xml",
        "views/stock_move_views.xml",
        "views/menu.xml",
    ],
    "demo": [],
    "application": False,
    "license": "LGPL-3",
}
