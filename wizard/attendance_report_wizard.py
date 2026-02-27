from odoo import models, fields, api
from datetime import timedelta

class AttendanceReportWizard(models.TransientModel):
    _name = 'nursery.attendance.report.wizard'
    _description = 'Attendance Report Wizard'

    date_from = fields.Date(string='From Date', required=True, default=fields.Date.context_today)
    date_to = fields.Date(string='To Date', required=True, default=fields.Date.context_today)
    class_ids = fields.Many2many('nursery.class', string='Classes', help="Leave empty to include all classes.")

    def action_print_report(self):
        self.ensure_one()
        # Cap the date range to 31 days to avoid massive horizontal tables
        if (self.date_to - self.date_from).days > 31:
            self.date_from = self.date_to - timedelta(days=31)

        data = {
            'form': self.read()[0],
        }
        return self.env.ref('nursery_management.action_report_nursery_attendance').report_action(self, data=data)
