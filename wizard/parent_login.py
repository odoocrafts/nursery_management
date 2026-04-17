import random
import string
from odoo import models, fields, api
from odoo.exceptions import UserError

class NurseryParentLoginWizard(models.TransientModel):
    _name = 'nursery.parent.login.wizard'
    _description = 'Parent Login Wizard'

    student_id = fields.Many2one('nursery.student', string='Student', required=True)
    parent_id = fields.Many2one('res.partner', string='Parent', related='student_id.parent_id')
    email = fields.Char(string='Login Email', related='parent_id.email', readonly=False)
    password = fields.Char(string='Generated Password', required=True)
    login_info_text = fields.Char(string='Login Info', compute='_compute_login_info_text')
    
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get('active_model') == 'nursery.student' and self.env.context.get('active_id'):
            student = self.env['nursery.student'].browse(self.env.context.get('active_id'))
            if not student.parent_id:
                raise UserError("Please assign a Parent/Guardian to the student before creating a login.")
            res['student_id'] = student.id
            
            # Generate random 5 char password (letters + numbers)
            chars = string.ascii_letters + string.digits
            res['password'] = ''.join(random.choice(chars) for i in range(5))
        return res

    @api.depends('email', 'password')
    def _compute_login_info_text(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for wizard in self:
            if wizard.email and wizard.password:
                wizard.login_info_text = f"Portal URL: {base_url}/my \nLogin: {wizard.email} \nPassword: {wizard.password}"
            else:
                wizard.login_info_text = ""

    def action_create_login(self):
        self.ensure_one()
        if not self.email:
            raise UserError("An email address is required for the parent to log in.")
            
        # Ensure parent has email set permanently
        self.parent_id.email = self.email
            
        # Check if user already exists for this partner
        user = self.env['res.users'].sudo().search([('partner_id', '=', self.parent_id.id)], limit=1)
        portal_group = self.env.ref('base.group_portal')
        
        if user:
            # Update existing user
            user.sudo().write({
                'password': self.password,
                'groups_id': [(4, portal_group.id)]
            })
        else:
            # Check if login (email) is already taken
            existing_login = self.env['res.users'].sudo().search([('login', '=', self.email)])
            if existing_login:
                raise UserError(f"A user with the login/email '{self.email}' already exists. Please use a different email.")
                
            # Create new user
            user = self.env['res.users'].sudo().create({
                'name': self.parent_id.name,
                'login': self.email,
                'partner_id': self.parent_id.id,
                'groups_id': [(6, 0, [portal_group.id])],
                'password': self.password,
            })
            
        return {'type': 'ir.actions.act_window_close'}
