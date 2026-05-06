from odoo import models, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals_list):
        # Set default home action to Nursery Dashboard for new users
        dashboard_action = self.env.ref('nursery_management.action_nursery_dashboard', raise_if_not_found=False)
        if dashboard_action:
            for vals in vals_list:
                if 'action_id' not in vals:
                    vals['action_id'] = dashboard_action.id
        return super(ResUsers, self).create(vals_list)
