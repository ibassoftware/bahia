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


# DELETE employee user
def delete_employee_user():
	print("UPDATING ...")
	start = time.time()

	count = 0
	count_update = 0

	
	# args = [('create_date', '<', '12/15/2023')]
	args = [('name', 'ilike', '')]
	get_user = dest_models.execute(dest_DB, dest_uid, dest_PASS, 'res.users', 'search', args)

	print(get_user)
	print(len(get_user))
	
	# if get_user:
	# 	for user in get_user:
	# 		count += 1
	# 		# UPDATE employee user
	# 		print("CREATING employee user: " + str(user))
	# 		# try:
	# 		create_employee_user = dest_models.execute(dest_DB, dest_uid, dest_PASS, 'res.users', 'createEmployeeUser', user)
	# 		if create_employee_user:
	# 			print("employee user CREATED: " + str(user))
	# 			count_update += 1
	# 		# except:
	# 		# 	print("Cannot create")

	print("DONE! PROCESSED # OF RECORDS: " + str(count_update))
	end = time.time()
	execution_time = end - start
	log = "[DONE] Total number of records updated: " + str(count_update) + " OVER: " + str(count) + ". EXECUTION TIME (seconds): " + str(execution_time)
	print(log)

delete_employee_user()