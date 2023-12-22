#!/usr/bin/python

import sys, os
import base64

# import xmlrpc
import xmlrpclib

from datetime import datetime
import time

import pandas as pd

# from random import randint

# ODOO SERVER CONNECTION
# PROD
# dest_URL = 'https://indigotest.odoo.com'
# dest_DB = 'indigo-prodnewrrd2-1833891'

# PROD TRIAL MIG 2023
dest_URL = 'https://158.220.98.233:8069'
dest_DB = 'BAHIA'

dest_USER = 'admin'
dest_PASS = 'admin'

# STAGING CONNECTION
dest_common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(dest_URL))
dest_uid = dest_common.authenticate(dest_DB, dest_USER, dest_PASS, {})
dest_models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(dest_URL))


# UPDATE EMPLOYEE NAME
def update_employee_name():
	print("UPDATING ...")
	start = time.time()

	count = 0
	count_update = 0

	
	# args = [('name', 'ilike', '')]
	args = [('id', '=', 50543)]
	get_employee_name = dest_models.execute(dest_DB, dest_uid, dest_PASS, 'hr.employee', 'search', args)

	if get_employee_name:
		for employee_name in get_employee_name:
			count += 1
			# UPDATE employee name
			print("UPDATING employee name: " + str(employee_name))
			update_employee_name = dest_models.execute(dest_DB, dest_uid, dest_PASS, 'hr.employee', 'updateEmployeeName', employee_name)
			if update_employee_name:
				print("employee name UPDATED: " + str(employee_name))
				count_update += 1

	print("DONE! PROCESSED # OF RECORDS: " + str(count_update))
	end = time.time()
	execution_time = end - start
	log = "[DONE] Total number of records updated: " + str(count_update) + " OVER: " + str(count) + ". EXECUTION TIME (seconds): " + str(execution_time)
	print(log)

update_employee_name()