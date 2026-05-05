from odoo import models, api, fields
from datetime import date

class NurseryDashboard(models.AbstractModel):
    _name = 'nursery.dashboard'
    _description = 'Nursery Dashboard Backend'

    @api.model
    def get_dashboard_stats(self):
        today = fields.Date.context_today(self)
        
        # 1. Total Students
        total_students = self.env['nursery.student'].search_count([])
        
        # 2. Total Present Today (from Check-ins)
        total_present = self.env['nursery.checkin'].search_count([
            ('checkin_time', '>=', today)
        ])
        
        # 3. Average Mood Today
        reports = self.env['nursery.daily.report'].search([('date', '=', today)])
        moods = [m for m in reports.mapped('mood_class') if m]
        average_mood = max(set(moods), key=moods.count) if moods else 'N/A'
        
        # 4. Total Fees Received (Posted)
        posted_fees = self.env['nursery.fee'].search([('state', '=', 'posted')])
        fee_received = sum(posted_fees.mapped('amount'))
        
        # 5. Upcoming Events
        events = self.env['nursery.event'].search(
            [('date_start', '>=', fields.Datetime.now())],
            order='date_start asc',
            limit=5
        )
        upcoming_events = [{
            'id': e.id,
            'name': e.name,
            'date': e.date_start.strftime("%b %d, %Y - %H:%M") if e.date_start else '',
            'venue': e.venue or 'TBA'
        } for e in events]
        
        return {
            'total_students': total_students,
            'total_present': total_present,
            'average_mood': average_mood.capitalize() if average_mood != 'N/A' else average_mood,
            'fee_received': fee_received,
            'upcoming_events': upcoming_events
        }
