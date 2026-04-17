from odoo import models, fields

class NurseryNotice(models.Model):
    _name = 'nursery.notice'
    _description = 'Nursery Notice'
    _order = 'date desc, id desc'

    name = fields.Char(string='Title', required=True)
    content = fields.Html(string='Content', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today)
    active = fields.Boolean(default=True)
