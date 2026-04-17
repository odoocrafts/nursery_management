from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class NurseryPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        
        if 'student_count' in counters:
            values['student_count'] = request.env['nursery.student'].search_count([('parent_id', '=', partner.id)])
        if 'event_count' in counters:
            values['event_count'] = request.env['nursery.event'].search_count([])
        if 'suggestion_count' in counters:
            values['suggestion_count'] = request.env['nursery.suggestion'].search_count([('partner_id', '=', partner.id)])
            
        return values

    @http.route(['/my/students', '/my/students/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_students(self, page=1, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        domain = [('parent_id', '=', partner.id)]
        
        pager = portal_pager(
            url="/my/students",
            total=request.env['nursery.student'].search_count(domain),
            page=page,
            step=10
        )
        
        students = request.env['nursery.student'].search(domain, limit=10, offset=pager['offset'])
        
        values.update({
            'students': students,
            'page_name': 'student',
            'pager': pager,
            'default_url': '/my/students',
        })
        return request.render("nursery_management.portal_my_students", values)

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


    @http.route(['/my/events'], type='http', auth="user", website=True)
    def portal_my_events(self, **kw):
        values = self._prepare_portal_layout_values()
        events = request.env['nursery.event'].search([])
        values.update({
            'events': events,
            'page_name': 'event',
        })
        return request.render("nursery_management.portal_my_events", values)

    @http.route(['/my/suggestions'], type='http', auth="user", website=True)
    def portal_my_suggestions(self, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        suggestions = request.env['nursery.suggestion'].search([('partner_id', '=', partner.id)])
        values.update({
            'suggestions': suggestions,
            'page_name': 'suggestion',
        })
        return request.render("nursery_management.portal_my_suggestions", values)

    @http.route(['/my/suggestion/submit'], type='http', auth="user", website=True, methods=['GET', 'POST'])
    def portal_submit_suggestion(self, **post):
        if request.httprequest.method == 'POST':
            request.env['nursery.suggestion'].create({
                'name': post.get('subject'),
                'suggestion': post.get('suggestion'),
                'partner_id': request.env.user.partner_id.id,
            })
            return request.redirect('/my/suggestions')
            
        values = self._prepare_portal_layout_values()
        values.update({'page_name': 'submit_suggestion'})
        return request.render("nursery_management.portal_submit_suggestion", values)
