from odoo import models, fields

class NurserySuggestion(models.Model):
    _name = 'nursery.suggestion'
    _description = 'Parent Suggestion'
    _inherit = ['mail.thread']
    _order = 'create_date desc'

    name = fields.Char(string='Subject', required=True)
    partner_id = fields.Many2one('res.partner', string='Parent')
    suggestion = fields.Text(string='Suggestion Details', required=True)
    state = fields.Selection([
        ('draft', 'New'),
        ('reviewed', 'Reviewed')
    ], string='Status', default='draft')
