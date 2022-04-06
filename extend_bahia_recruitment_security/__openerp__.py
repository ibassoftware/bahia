{
    'name': 'Extend Bahia Recruitment Security',
    'category': 'Human Resource',
    'sequence': 25,
    'summary': 'Add Recruiter Group',
    'description': 'Add Recruiter Group.',
    'author': 'Excode Innovation Solutions. Inc.',
    'depends': ['hr', 'hr_recruitment'],
    'data': [
             'security/hr_recruitment.xml',
             'security/ir.model.access.csv',
             'views/hr_recruitment.xml',],             
    'application': False,
}