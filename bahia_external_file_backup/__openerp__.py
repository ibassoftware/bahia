{
    'name': 'Bahia Seafarer Document Backup',
    'category': 'Tools',
    'sequence': 25,
    'summary': 'Automated/Manual Backup of External Documents for Bahia',
    'description': 'This will allow an Automation or Manual Backup of the Documents that Bahia is needed for their Seafarer.',
    'author': 'Excode Innovation Solutions. Inc.',
    'depends': ['base', 'bahia_personnel_management', 'db_backup_ept'],
    'data': [
             #'security/ir.model.access.csv',
             #'security/sys.model.audit.config.csv',
             'data/external_file_backup.xml',
             'views/external_backup_file.xml',],             
    'application': False,
}