from odoo import models, fields

class NurseryFeeType(models.Model):
    _name = 'nursery.fee.type'
    _description = 'Nursery Fee Type'
    _order = 'sequence, id'

    name = fields.Char(string='Fee Name', required=True)
    amount = fields.Float(string='Default Amount', default=0.0)
    sequence = fields.Integer(string='Sequence', default=10)
    description = fields.Text(string='Description')
    is_admission = fields.Boolean(string='Is Admission Fee', help="Check this if this fee is the standard Admission Fee applied to all students.")
