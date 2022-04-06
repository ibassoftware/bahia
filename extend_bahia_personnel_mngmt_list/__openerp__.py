{
    'name': 'Bahia Personnel Management Customization',
    'category': 'Human Resources',
    'sequence': 25,
    'summary': 'Bahia Customization',
    'description': 'Bahia Customization for Tracking and Allowing the Seafarers his/her Information',
    'author': 'XCode Innovation Solutions',
    'depends': ['hr',
                'mail', 
                'resource', 
                'bahia_personnel_management',
                'extend_bahia_pm_consent_form', 
                'extend_bahia_personnel_management',
                'bahia_personnel_data_migration'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_personnel_management.xml',
        ],
    'application': True,
}
#'data': ['hr_recruitment_view.xml','views/hr_recruitment_personnel_view.xml'],
#'security/ir.model.access.csv'

