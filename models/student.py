from odoo import models, fields, api
from datetime import date

class NurseryStudent(models.Model):
    _name = 'nursery.student'
    _description = 'Nursery Student'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    def _compute_access_url(self):
        super()._compute_access_url()
        for student in self:
            student.access_url = f'/my/students/{student.id}'

    name = fields.Char(string='Student Name', required=True, tracking=True)
    dob = fields.Date(string='Date of Birth', required=True)
    age = fields.Char(string='Age', compute='_compute_age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    class_id = fields.Many2one('nursery.class', string='Class', tracking=True)
    shift = fields.Selection([
        ('full_day', 'Full Day'),
        ('half_day', 'Half Day')
    ], string='Shift', default='full_day')
    image = fields.Image(string='Image')
    parent_id = fields.Many2one('res.partner', string='Parent/Guardian')
    report_count = fields.Integer(string='Report Count', compute='_compute_report_count')

    # Fee Details
    admission_date = fields.Date(string='Admission Date', default=fields.Date.context_today)
    fee_ids = fields.One2many('nursery.fee', 'student_id', string='Fee Payments')
    total_paid = fields.Float(string='Total Paid', compute='_compute_dues')
    total_due = fields.Float(string='Total Due', compute='_compute_dues')

    @api.depends('fee_ids.amount', 'fee_ids.state', 'admission_date', 'class_id.monthly_fee')
    def _compute_dues(self):
        # Fetch Admission Fee from Fee Type
        admission_fee_type = self.env['nursery.fee.type'].search([('is_admission', '=', True)], limit=1)
        admission_fee = admission_fee_type.amount if admission_fee_type else 0.0
        
        for student in self:
            # Calculate Total Paid
            student.total_paid = sum(student.fee_ids.filtered(lambda f: f.state == 'posted').mapped('amount'))
            
            # Calculate Total Payable
            total_payable = admission_fee
            if student.admission_date and student.class_id:
                today = date.today()
                # Simple month difference calculation
                months = (today.year - student.admission_date.year) * 12 + (today.month - student.admission_date.month)
                # If admitted this month, count as 1 month (or 0 if you want to charge next month, but usually charge current)
                # Let's assume charge for current month if joined.
                months += 1 
                if months > 0:
                    total_payable += months * student.class_id.monthly_fee
            
            student.total_due = total_payable - student.total_paid

    def _compute_report_count(self):
        for student in self:
            student.report_count = self.env['nursery.daily.report'].search_count([('student_id', '=', student.id)])

    # --- Smart Button Actions ---
    def action_view_reports(self):
        self.ensure_one()
        return {
            'name': 'Daily Reports',
            'type': 'ir.actions.act_window',
            'res_model': 'nursery.daily.report',
            'view_mode': 'list,form,graph',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }
        
    def action_view_fees(self):
        self.ensure_one()
        return {
            'name': 'Fee Payments',
            'type': 'ir.actions.act_window',
            'res_model': 'nursery.fee',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    # --- Attendance ---
    attendance_count = fields.Integer(string="Attendance Records", compute='_compute_attendance_count')

    def _compute_attendance_count(self):
        for student in self:
            student.attendance_count = self.env['nursery.attendance'].search_count([('student_id', '=', student.id)])

    def action_view_attendance(self):
        self.ensure_one()
        return {
            'name': 'Attendance',
            'type': 'ir.actions.act_window',
            'res_model': 'nursery.attendance',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    @api.depends('dob')
    def _compute_age(self):
        for student in self:
            if student.dob:
                today = date.today()
                years = today.year - student.dob.year - ((today.month, today.day) < (student.dob.month, student.dob.day))
                student.age = f"{years} Years"
            else:
                student.age = "N/A"
