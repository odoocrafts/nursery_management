from odoo import models, fields, api

class NurseryDailyReport(models.Model):
    _name = 'nursery.daily.report'
    _description = 'Daily Parent Communication Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_id = fields.Many2one('nursery.student', string='Student', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
    class_id = fields.Many2one('nursery.class', related='student_id.class_id', string='Class', store=True)

    # Routine & Engagement
    handwashing = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Handwashing')
    settled_down = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Settling Down')
    engagement = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Engagement in Class')
    
    mood_class = fields.Selection([
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('neutral', 'Neutral'),
        ('active', 'Active'),
        ('tired', 'Tired')
    ], string='Mood in Class')
    
    mood_play = fields.Selection([
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('neutral', 'Neutral'),
        ('active', 'Active'),
        ('tired', 'Tired')
    ], string='Mood in Play Area')
    
    sleep_duration = fields.Float(string='Sleep Duration (Hours)')
    water_consumed = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Water Consumed')
    urine_count = fields.Integer(string='Urine Count')

    # Food Status
    breakfast_status = fields.Selection([
        ('finished', 'Finished'),
        ('almost_finished', 'Almost Finished'),
        ('half', 'Half Eaten'),
        ('no', 'Not Eaten')
    ], string='Breakfast Status')
    
    lunch_status = fields.Selection([
        ('finished', 'Finished'),
        ('almost_finished', 'Almost Finished'),
        ('half', 'Half Eaten'),
        ('no', 'Not Eaten')
    ], string='Lunch Status')
    
    snack_status = fields.Selection([
        ('finished', 'Finished'),
        ('almost_finished', 'Almost Finished'),
        ('half', 'Half Eaten'),
        ('no', 'Not Eaten')
    ], string='Snack Status')

    # Narrative
    remarks = fields.Html(string='Learning/Activity Remarks')
    
    # Media
    activity_image = fields.Image(string='Activity Photo')
