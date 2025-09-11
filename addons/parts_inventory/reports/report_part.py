# addons/parts_inventory/reports/report_part.py
from odoo import models

class ReportPartPDF(models.AbstractModel):
    _name = "report.parts_inventory.report_part_pdf"
    _description = "Part PDF Report"

    def _get_report_values(self, docids, data=None):
        docs = self.env["parts.inventory.part"].browse(docids)
        return {"docs": docs}
