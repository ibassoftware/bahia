#!/usr/bin/python

import sys, os
import base64

# import xmlrpclib
from xmlrpc import client

from datetime import datetime
import time

# ODOO SERVER CONNECTION
# SOURCE - PROD
src_URL = 'http://backoffice.bahiashipping.ph'
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


# UPDATE employee licenses
def update_employee_licenses():
	print("MIGRATION OF employee licenses ON GOING...")
	start = time.time()

	count = 0
	count_update = 0

	# args = [('id', '=', 502358)]
	args = [('file_upload', '!=', False)]
	get_employee_doc = src_models.execute(src_DB, src_uid, src_PASS, 'hr.employeelicenses', 'search', args)
	
	for employee_doc in get_employee_doc:
		employee_doc_fields = [
			'id',
			'employee_licenses_id',
			'licensetype',
			'file_upload',
		]
		employee_doc_data = src_models.execute(src_DB, src_uid, src_PASS, 'hr.employeelicenses', 'read', employee_doc, employee_doc_fields)

		print(employee_doc_data['employee_licenses_id'])
		print(employee_doc_data['licensetype'])

		check_args = [('id', '=', employee_doc)]
		check_dest_employee_doc = dest_models.execute(dest_DB, dest_uid, dest_PASS, 'hr.employeelicenses', 'search', check_args)
		if check_dest_employee_doc:
			employee_update_doc = dest_models.execute_kw(dest_DB, dest_uid, dest_PASS, 'hr.employeelicenses', 'write', [employee_doc, {
				'file_upload': employee_doc_data['file_upload'],
			}])

			if employee_update_doc:
				count += 1
				print("[" + str(count) + "]" + "UPDATED employee: " + str(employee_doc_data['employee_licenses_id']))

update_employee_licenses()