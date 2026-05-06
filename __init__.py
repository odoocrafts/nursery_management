from . import controllers
from . import models
from . import wizard
from . import report

def post_init_hook(env):
    dashboard_action = env.ref('nursery_management.action_nursery_dashboard', raise_if_not_found=False)
    if dashboard_action:
        # Update all internal users (share=False) except OdooBot/Public
        users = env['res.users'].search([('share', '=', False), ('id', '>', 2)])
        for user in users:
            if not user.action_id:
                user.write({'action_id': dashboard_action.id})
