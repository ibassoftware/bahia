{
    'name': 'Bahia Application functions',
    'category': 'Human Resources',
    'sequence': 26,
    'summary': 'A part of Bahia Personnel Management',
    'description': 'Part of Bahia Personnel Management in the Recruitment',
    'author': 'Datagenesis',
    'depends': ['hr_recruitment'],
    'data': ['views/hr_recruitment_view.xml',
             'views/socialmedia.xml',
             'data/ir_sequence.xml',
             'data/hr.socialmedia.config.csv',
             'reports/application_form_report.xml'],
    'application': True,
}

#f