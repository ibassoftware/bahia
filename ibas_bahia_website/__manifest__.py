{
    'name': 'Bahia Personnel Management Website',
    'category': 'Content Management',
    'sequence': 25,
    'summary': 'Bahia Website Content Management',
    'description': 'Personnel Management Information for Bahia Website Management odoo v15',
    'author': 'IBAS and Samuel Salvador',
    'depends': ['ibas_bahia','website','website_hr_recruitment','website_partner'],
    'data': [
             'security/ir.model.access.csv',
             'views/privacy_policy.xml',
             'views/hr_recruitment.xml',
             'views/application_form_temp.xml',
             # 'views/templates.xml',
             'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'ibas_bahia_website/static/src/js/BAHIA_MAIN.js',
            'ibas_bahia_website/static/src/js/bahia_application_form.js',
        ],
    },
    'license': 'LGPL-3',
    'application': True,
}


