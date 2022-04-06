{
    'name': 'Jobs Bahia',
    'category': 'Website',
    'version': '1.0',
    'summary': 'Job Descriptions And Application Forms for Bahia',
    'description': """
OpenERP Contact Form
====================

        """,
    'author': 'Excode Innovation',
    'depends': ['website','website_partner', 'hr_recruitment', 'website_mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/website_hr_recruitment_security.xml',
        'data/config_data.xml',
        'views/hr_job_views.xml',
        'views/templates.xml',
        'views/templates_application.xml',
    ],
    'installable': True,
}
