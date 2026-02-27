from odoo import models, fields, api

class NurseryClass(models.Model):
    _name = 'nursery.class'
    _description = 'Nursery Class'

    name = fields.Char(string='Class Name', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    monthly_fee = fields.Float(string='Monthly Fee', required=True, default=0.0)

    student_ids = fields.One2many('nursery.student', 'class_id', string='Students')
    student_count = fields.Integer(string='Total Students', compute='_compute_statistics')
    total_due = fields.Float(string='Total Due', compute='_compute_statistics')
    total_paid = fields.Float(string='Total Paid', compute='_compute_statistics')
    avg_mood_class = fields.Char(string='Avg Mood (Class)', compute='_compute_statistics')
    avg_mood_play = fields.Char(string='Avg Mood (Play)', compute='_compute_statistics')

    @api.depends('student_ids', 'student_ids.total_due', 'student_ids.total_paid')
    def _compute_statistics(self):
        for record in self:
            record.student_count = len(record.student_ids)
            record.total_due = sum(record.student_ids.mapped('total_due'))
            record.total_paid = sum(record.student_ids.mapped('total_paid'))
            
            # Simple logic for "Average" mood - finding the most frequent one from recent reports of students in this class
            # This is a bit resource intensive if many reports, so optimization might be needed for large data.
            # For now, let's fetch reports linked to these students.
            reports = self.env['nursery.daily.report'].search([('class_id', '=', record.id)], limit=100, order='date desc')
            
            if reports:
                # Mood in Class
                moods_class = reports.mapped('mood_class')
                if moods_class:
                    record.avg_mood_class = max(set(moods_class), key=moods_class.count)
                else:
                    record.avg_mood_class = 'N/A'
                
                # Mood in Play Area
                moods_play = reports.mapped('mood_play')
                if moods_play:
                    record.avg_mood_play = max(set(moods_play), key=moods_play.count)
                else:
                    record.avg_mood_play = 'N/A'
            else:
                record.avg_mood_class = 'N/A'
                record.avg_mood_play = 'N/A'
