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
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/nursery_menus.xml',
        'views/nursery_class_views.xml',
        'views/student_views.xml',
        'views/daily_report_views.xml',
        'views/fee_views.xml',
        'report/nursery_reports.xml',
        'report/daily_report_template.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
