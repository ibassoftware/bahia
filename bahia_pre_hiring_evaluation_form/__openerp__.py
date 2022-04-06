{
    'name': 'Bahia Pre-Hiring Evaluation Form',
    'category': 'Form',
    'sequence': 25,
    'summary': 'Pre-Hiring Evaluation Form',
    'description': 'Evaluation form form for Applicant',
    'author': 'Excode Innovation Solutions. Inc.',
    'depends': ['base', 
                'bahia_personnel_management', 
                'hr_recruitment_extend_application'],
    'data': [
             'security/ir.model.access.csv',
             #'security/sys.model.audit.config.csv',
             
             'report/hr_applicant_evaluation.xml',
             'views/hr_applicant_evaluation.xml',
             'views/hr_applicant.xml',
             'data/report_paper_format.xml',],             
    'application': False,
}