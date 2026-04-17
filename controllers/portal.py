from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class NurseryPortal(CustomerPortal):

    @http.route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        partner = request.env.user.partner_id
        students = request.env['nursery.student'].search([('parent_id', '=', partner.id)])
        
        # If the user is a parent (has students), render the custom dashboard
        if students:
            values = self._prepare_portal_layout_values()
            
            # Fetch relevant data
            reports = request.env['nursery.daily.report'].search([('student_id', 'in', students.ids)], limit=5, order="date desc, id desc")
            events = request.env['nursery.event'].search([], limit=5, order="date_start asc")
            notices = request.env['nursery.notice'].search([('active', '=', True)], limit=5, order="date desc")
            suggestions = request.env['nursery.suggestion'].search([('partner_id', '=', partner.id)], limit=3, order="create_date desc")
            
            values.update({
                'students': students,
                'reports': reports,
                'events': events,
                'notices': notices,
                'suggestions': suggestions,
                'page_name': 'home',
            })
            return request.render("nursery_management.nursery_portal_dashboard", values)
            
        # Fallback to standard Odoo portal if not a parent
        return super(NurseryPortal, self).home(**kw)

    @http.route(['/my/students/<int:student_id>'], type='http', auth="user", website=True)
    def portal_my_student_detail(self, student_id, **kw):
        student = request.env['nursery.student'].browse(student_id)
        if student.parent_id != request.env.user.partner_id:
            return request.redirect('/my')
            
        values = {
            'student': student,
            'page_name': 'student_detail',
        }
        return request.render("nursery_management.portal_student_detail", values)

    @http.route(['/my/reports/<int:report_id>'], type='http', auth="user", website=True)
    def portal_my_report_detail(self, report_id, **kw):
        report = request.env['nursery.daily.report'].browse(report_id)
        if report.student_id.parent_id != request.env.user.partner_id:
            return request.redirect('/my')
            
        values = {
            'report': report,
            'page_name': 'report_detail',
        }
        return request.render("nursery_management.portal_daily_report_detail", values)

    @http.route(['/my/suggestion/submit'], type='http', auth="user", website=True, methods=['POST'])
    def portal_submit_suggestion(self, **post):
        request.env['nursery.suggestion'].create({
            'name': post.get('subject'),
            'suggestion': post.get('suggestion'),
            'partner_id': request.env.user.partner_id.id,
        })
        return request.redirect('/my')
