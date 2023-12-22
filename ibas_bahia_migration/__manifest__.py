{
    'name': 'Bahia Migration',
    'category': 'Human Resources',
    'sequence': 25,
    'summary': 'Bahia Tool To Migrate Images and Files',
    'description': 'After All the Primary Information of the Employees and its Configuration\n this will be the data migration for Files'\
        'Pictures and One2Many Relationship in Personnel Management',
    'author': 'IBAS',
    'depends': ['hr', 'ibas_bahia'],
    'data': [
    	     'security/ir.model.access.csv',             
             'views/hr_employee_data_tables.xml',
             'views/hr_data_migration.xml',
             ],
    'application': False,
}


