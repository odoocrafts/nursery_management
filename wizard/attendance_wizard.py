from odoo import models, fields, api
from odoo.exceptions import UserError

class AttendanceWizard(models.TransientModel):
    _name = 'nursery.attendance.wizard'
    _description = 'Batch Attendance Wizard'

    class_id = fields.Many2one('nursery.class', string='Class', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    line_ids = fields.One2many('nursery.attendance.wizard.line', 'wizard_id', string='Students')

    @api.onchange('class_id', 'date')
    def _onchange_class_id(self):
        if self.class_id and self.date:
            # Check if attendance already exists
            existing = self.env['nursery.attendance'].search([
                ('class_id', '=', self.class_id.id),
                ('date', '=', self.date)
            ], limit=1)
            
            if existing:
                self.line_ids = [(5, 0, 0)]
                return {
                    'warning': {
                        'title': 'Attendance Exists',
                        'message': 'Attendance for this class on this date has already been recorded.'
                    }
                }

            # Fetch students in the class
            students = self.env['nursery.student'].search([('class_id', '=', self.class_id.id)])
            
            # Prepare lines (default is_present=True)
            lines = [(5, 0, 0)] # Clear existing lines
            for student in students:
                lines.append((0, 0, {
                    'student_id': student.id,
                    'is_present': True
                }))
            self.line_ids = lines
        else:
            self.line_ids = [(5, 0, 0)]

    def action_submit_attendance(self):
        self.ensure_one()
        
        # Prevent submission if attendance already exists for this class and date
        existing = self.env['nursery.attendance'].search([
            ('class_id', '=', self.class_id.id),
            ('date', '=', self.date)
        ], limit=1)
        
        if existing:
            raise UserError('Attendance for this class on this date has already been recorded. You cannot submit it again.')

        Attendance = self.env['nursery.attendance']
        
        for line in self.line_ids:
            status = 'present' if line.is_present else 'absent'
            
            Attendance.create({
                'student_id': line.student_id.id,
                'date': self.date,
                'status': status,
                'notes': line.notes
            })
        
        return {'type': 'ir.actions.act_window_close'}


class AttendanceWizardLine(models.TransientModel):
    _name = 'nursery.attendance.wizard.line'
    _description = 'Batch Attendance Wizard Line'

    wizard_id = fields.Many2one('nursery.attendance.wizard', required=True, ondelete='cascade')
    student_id = fields.Many2one('nursery.student', string='Student', required=True)
    is_present = fields.Boolean(string='Present', default=True)
    notes = fields.Char(string='Notes')
