#!/usr/bin/python

import sys, os
import base64

# import xmlrpclib
from xmlrpc import client

from datetime import datetime
import time

# ODOO SERVER CONNECTION
# PROD
# dest_URL = 'https://indigotest.odoo.com'
# dest_DB = 'indigo-prodnewrrd2-1833891'

# PROD TRIAL MIG 2023
dest_URL = 'http://154.26.132.80:8069'
dest_DB = 'BAHIA'

dest_USER = 'admin'
dest_PASS = 'P@5word'

# STAGING CONNECTION
dest_common = client.ServerProxy('{}/xmlrpc/2/common'.format(dest_URL))
dest_uid = dest_common.authenticate(dest_DB, dest_USER, dest_PASS, {})
dest_models = client.ServerProxy('{}/xmlrpc/2/object'.format(dest_URL))


# CREATE employee user
def create_employee_user():
	print("UPDATING ...")
	start = time.time()

	count = 0
	count_update = 0

	
	args = [('user_id', '=', 'False')]
	# args = [('id', '=', 53931)]
	get_employee_name = dest_models.execute(dest_DB, dest_uid, dest_PASS, 'hr.employee', 'search', args)

	print(get_employee_name)
	
	if get_employee_name:
		for employee_name in get_employee_name:
			count += 1
			# UPDATE employee user
			print("CREATING employee user: " + str(employee_name))
			create_employee_user = dest_models.execute(dest_DB, dest_uid, dest_PASS, 'hr.employee', 'createEmployeeUser', employee_name)
			if create_employee_user:
				print("employee user CREATED: " + str(employee_name))
				count_update += 1

	print("DONE! PROCESSED # OF RECORDS: " + str(count_update))
	end = time.time()
	execution_time = end - start
	log = "[DONE] Total number of records updated: " + str(count_update) + " OVER: " + str(count) + ". EXECUTION TIME (seconds): " + str(execution_time)
	print(log)

create_employee_user()