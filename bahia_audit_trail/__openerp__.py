{
    'name': 'Bahia Audit Log',
    'category': 'Tools',
    'sequence': 25,
    'summary': 'Tracking of Changes in detail in a Model',
    'description': 'To Track the changes of record on the Given Model.',
    'author': 'Excode Innovation Solutions. Inc.',
    'depends': ['base','hr', 'hr_recruitment', 'bahia_personnel_management'],
    'data': [
             'security/ir.model.access.csv',
             'security/sys.model.audit.config.csv',
             'views/sys_model_audit.xml',],             
    'application': False,
}