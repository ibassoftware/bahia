#!/usr/bin/python

import sys, os
import base64

# import xmlrpc
# import xmlrpclib
from xmlrpc import client


from datetime import datetime
import time

import pandas as pd

# from random import randint

# ODOO SERVER CONNECTION
# PROD
# dest_URL = 'https://indigotest.odoo.com'
# dest_DB = 'indigo-prodnewrrd2-1833891'

# TEST
dest_URL = 'http://45.77.38.247:8069'
dest_DB = 'BAHIA2'

dest_USER = 'admin'
dest_PASS = 'admin'

# STAGING CONNECTION
dest_common = client.ServerProxy('{}/xmlrpc/2/common'.format(dest_URL))
dest_uid = dest_common.authenticate(dest_DB, dest_USER, dest_PASS, {})
dest_models = client.ServerProxy('{}/xmlrpc/2/object'.format(dest_URL))


# UPDATE EMPLOYEE FULL NAME
def computeEmployeeName():
	print("UPDATING ...")
	start = time.time()

	count = 0
	count_update = 0

	
	args = [('name', 'ilike', '')]
	get_employee = dest_models.execute(dest_DB, dest_uid, dest_PASS, 'hr.employee', 'search', args)

	# print len(get_sale)

	if get_employee:
		for employee in get_employee:
			count += 1
			# UPDATE employee
			print("UPDATING employee: " + str(employee))
			# update_employee = dest_models.execute_kw(dest_DB, dest_uid, dest_PASS, 'stock.employee.layer', 'write', [employee, {
			# 	'value': 0,
			# }])
			update_employee = dest_models.execute(dest_DB, dest_uid, dest_PASS, 'hr.employee', 'computeEmployeeName', employee)
			if update_employee:
				print("employee UPDATED: " + str(employee))
				count_update += 1

	print("DONE! PROCESSED # OF RECORDS: " + str(count_update))
	end = time.time()
	execution_time = end - start
	log = "[DONE] Total number of records updated: " + str(count_update) + " OVER: " + str(count) + ". EXECUTION TIME (seconds): " + str(execution_time)
	print(log)

computeEmployeeName()