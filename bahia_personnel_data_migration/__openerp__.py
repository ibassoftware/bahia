{
    'name': 'Bahia Personnel Management Data Migration',
    'category': 'Human Resources',
    'sequence': 25,
    'summary': 'Personnel Management Data Migration',
    'description': 'After All the Primary Information of the Employees and its Configuration\n this will be the data migration for Files'\
		'Pictures and One2Many Relationship in Personnel Management',
    'author': 'Datagenesis',
    'depends': ['bahia_personnel_management'],
    'data': [
	     'views/employee_link_tables.xml',
         'views/employee_image_and_file_data_migration.xml',
         ],
    'application': False,
}
