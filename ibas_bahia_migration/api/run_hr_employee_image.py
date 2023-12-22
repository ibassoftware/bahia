#!/usr/bin/python

import sys, os
import base64

# import xmlrpclib
from xmlrpc import client

from datetime import datetime
import time

# ODOO SERVER CONNECTION
# SOURCE - PROD
src_URL = 'http://bahiashipping.ph'
src_DB = 'bck_apr_2020'
src_USER = 'admin'
src_PASS = 'P@5word'

src_common = client.ServerProxy('{}/xmlrpc/2/common'.format(src_URL))
src_uid = src_common.authenticate(src_DB, src_USER, src_PASS, {})
src_models = client.ServerProxy('{}/xmlrpc/2/object'.format(src_URL))

# DESTINATION - TEST
dest_URL = 'http://158.220.98.233:8069'
dest_DB = 'BAHIA'
dest_USER = 'admin'
dest_PASS = 'admin'

dest_common = client.ServerProxy('{}/xmlrpc/2/common'.format(dest_URL))
dest_uid = dest_common.authenticate(dest_DB, dest_USER, dest_PASS, {})
dest_models = client.ServerProxy('{}/xmlrpc/2/object'.format(dest_URL))


# UPDATE employee image
def update_employee_image():
	print("MIGRATION OF employee ON GOING...")
	start = time.time()

	count = 0
	count_update = 0

	args = [('id', '=', 50382)]
	get_employee = src_models.execute(src_DB, src_uid, src_PASS, 'hr.employee', 'search', args)

	if get_employee:
		for employee in get_employee:
			employee_fields = [
				'id',
				'name',
				'image_1920',
			]
			employee_data = dest_models.execute(dest_DB, dest_uid, dest_PASS, 'hr.employee', 'read', employee, employee_fields)

			print(employee_data)
			employee_insert = dest_models.execute_kw(dest_DB, dest_uid, dest_PASS, 'hr.employee', 'write', [{
				'id': employee_data[0]['id'],
				'image': employee_data[0]['image_1920'],
			}])

			if employee_insert:
				count += 1
				print("[" + str(count) + "]" + "UPDATED employee: " + str(product))

update_employee_image()