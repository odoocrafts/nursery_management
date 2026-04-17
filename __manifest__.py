{
    'name': 'Nursery Management',
    'version': '18.0.1.0.0',
    'summary': 'Manage Nursery Students, Classes, and Daily Reports',
    'description': """
        Nursery Management System
        =========================
        - Manage Student Profiles
        - Manage Classes/Sections
        - Generate Daily Parent Communication Reports
    """,
    'category': 'Education',
    'author': 'Your Name',
    'website': 'https://www.example.com',
    'depends': ['base', 'mail', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'security/nursery_security.xml',
        'views/nursery_menus.xml',
        'views/nursery_class_views.xml',
        'views/student_views.xml',
        'views/daily_report_views.xml',
        'views/fee_views.xml',
        'views/attendance_views.xml',
        'views/checkin_views.xml',
        'views/event_views.xml',
        'views/suggestion_views.xml',
        'views/portal_templates.xml',
        'wizard/attendance_wizard_views.xml',
        'wizard/attendance_report_wizard_views.xml',
        'report/nursery_reports.xml',
        'report/attendance_report_template.xml',
        'report/daily_report_template.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
