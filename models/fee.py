from odoo import models, fields, api

class NurseryFee(models.Model):
    _name = 'nursery.fee'
    _description = 'Nursery Fee Payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    student_id = fields.Many2one('nursery.student', string='Student', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    amount = fields.Float(string='Amount', required=True)
    description = fields.Char(string='Description')
    fee_type_id = fields.Many2one('nursery.fee.type', string='Fee Type', required=True, default=lambda self: self.env['nursery.fee.type'].search([('name', '=', 'Tuition Fee')], limit=1))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted')
    ], string='Status', default='draft', tracking=True)

    @api.onchange('fee_type_id')
    def _onchange_fee_type_id(self):
        if self.fee_type_id:
            self.amount = self.fee_type_id.amount

    def action_post(self):
        self.write({'state': 'posted'})

    def action_draft(self):
        self.write({'state': 'draft'})
