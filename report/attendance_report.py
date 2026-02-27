from odoo import models, api
from datetime import timedelta

class ReportAttendancePDF(models.AbstractModel):
    _name = 'report.nursery_management.report_attendance_pdf'
    _description = 'Attendance PDF Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        form = data['form']
        date_from = fields.Date.from_string(form['date_from'])
        date_to = fields.Date.from_string(form['date_to'])
        
        # If no classes selected, take all classes
        class_ids = form.get('class_ids')
        if class_ids:
            classes = self.env['nursery.class'].browse(class_ids)
        else:
            classes = self.env['nursery.class'].search([])

        # Generate list of dates
        date_list = []
        current_date = date_from
        while current_date <= date_to:
            date_list.append(current_date)
            current_date += timedelta(days=1)

        attendance_data = {}
        for nursery_class in classes:
            students = self.env['nursery.student'].search([('class_id', '=', nursery_class.id)])
            if not students:
                continue
                
            class_data = []
            for student in students:
                student_attendance = []
                for dt in date_list:
                    attendance = self.env['nursery.attendance'].search([
                        ('student_id', '=', student.id),
                        ('date', '=', dt)
                    ], limit=1)
                    
                    if attendance:
                        status_char = 'P' if attendance.status == 'present' else ('A' if attendance.status == 'absent' else 'L')
                    else:
                        status_char = '-'
                    student_attendance.append(status_char)
                    
                class_data.append({
                    'student': student.name,
                    'attendance': student_attendance
                })
            
            attendance_data[nursery_class.name] = class_data

        return {
            'doc_ids': docids,
            'doc_model': 'nursery.attendance.report.wizard',
            'data': form,
            'date_from': date_from,
            'date_to': date_to,
            'date_list': date_list,
            'attendance_data': attendance_data,
        }
