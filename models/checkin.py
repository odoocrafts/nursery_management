from odoo import models, fields, api

class NurseryCheckin(models.Model):
    _name = 'nursery.checkin'
    _description = 'Student Check-In/Check-Out'
    _order = 'checkin_time desc, id desc'

    name = fields.Char(string='Reference', compute='_compute_name', store=True)
    student_id = fields.Many2one('nursery.student', string='Student', required=True)
    checkin_time = fields.Datetime(string='Arrival Time', default=fields.Datetime.now, required=True)
    checkout_time = fields.Datetime(string='Dispersal Time')
    checkin_snapshot = fields.Image(string='Arrival Snapshot', max_width=1024, max_height=1024)
    checkout_snapshot = fields.Image(string='Dispersal Snapshot', max_width=1024, max_height=1024)
    
    @api.depends('student_id', 'checkin_time')
    def _compute_name(self):
        for record in self:
            if record.student_id and record.checkin_time:
                record.name = f"{record.student_id.name} - {record.checkin_time.strftime('%Y-%m-%d')}"
            else:
                record.name = "New Check-In"
