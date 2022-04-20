{
    'name': 'Bahia Personnel Management Website',
    'category': 'Content Management',
    'sequence': 25,
    'summary': 'Bahia Website Content Management',
    'description': 'Personnel Management Information for Bahia Website Management odoo v15',
    'author': 'IBAS and Samuel Salvador',
    'depends': ['ibas_bahia','website','website_hr_recruitment'],
    'data': [
             #'templates/template_init.xml',
             'templates/privacy_policy.xml',
             'templates/hr_recruitment.xml',
             ],
    'assets': {
        'web.assets_frontend': [
            'ibas_bahia_website/static/src/js/BAHIA_MAIN.js',
        ],
    },
    'license': 'LGPL-3',
    'application': True,
}


