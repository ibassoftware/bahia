{
    'name': 'Extend Bahia Checklist Documents',
    'category': 'Human Resources',
    'sequence': 25,
    'summary': 'Extension of Bahia Checklist Document',
    'description': 'Checklist of Documents for Bahia',
    'author': 'Excode Innovation Solutions. Inc.',
    'depends': ['bahia_personnel_management'],
    'data': [
             'views/hr_employee_checklist_documents.xml',
             'reports/checklist_report.xml', #NI UPDATES
             'views/hr_checklist_templates.xml',
             'data/checklist_template_data.xml',
#             'data/hr.checklist_template.csv',
             'data/report_paper_format.xml',
             ],
    'application': False,
}

