from odoo import models, fields

class NurseryEvent(models.Model):
    _name = 'nursery.event'
    _description = 'Nursery Event'
    _order = 'date_start desc'

    name = fields.Char(string='Event Name', required=True)
    date_start = fields.Datetime(string='Start Date/Time', required=True)
    date_end = fields.Datetime(string='End Date/Time', required=True)
    venue = fields.Char(string='Venue')
    attendee_ids = fields.Many2many('res.partner', string='Attendees')
    description = fields.Text(string='Event Details')
