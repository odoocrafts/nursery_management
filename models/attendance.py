from odoo import models, fields, api

class NurseryAttendance(models.Model):
    _name = 'nursery.attendance'
    _description = 'Nursery Daily Attendance'
    _order = 'date desc, id desc'
    _rec_name = 'student_id'

    student_id = fields.Many2one('nursery.student', string='Student', required=True)
    class_id = fields.Many2one('nursery.class', string='Class', related='student_id.class_id', store=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave')
    ], string='Status', required=True, default='present')
    notes = fields.Char(string='Notes')

    _sql_constraints = [
        ('unique_attendance_per_day', 'unique(student_id, date)', 
         'Attendance for this student on this date already exists!')
    ]
