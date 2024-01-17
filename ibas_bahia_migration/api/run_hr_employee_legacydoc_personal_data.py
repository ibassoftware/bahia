#!/usr/bin/python

import sys, os
import base64

# import xmlrpclib
from xmlrpc import client

from datetime import datetime
import time

# ODOO SERVER CONNECTION
# SOURCE - PROD
# src_URL = 'http://bahiashipping.ph'
src_URL = 'http://192.168.88.253:8069'
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


# UPDATE employee legacy documents: personal_data
def update_employee_legacydoc_personal_data():
	print("MIGRATION OF employee legacy doc ON GOING...")
	start = time.time()

	count = 0
	count_update = 0

	args = [('id', '=', 50462)]
	# args = [('name', 'ilike', '')]
	get_employee = src_models.execute(src_DB, src_uid, src_PASS, 'hr.employee', 'search', args)

	if get_employee:
		for employee in get_employee:
			employee_fields = [
				'id',
				'name',
				'legacy_doc_2',
			]
			employee_data = src_models.execute(src_DB, src_uid, src_PASS, 'hr.employee', 'read', employee, employee_fields)

			print(employee)
			print(employee_data['id'])
			print(employee_data['name'])
			check_args = [('id', '=', employee	)]
			check_dest_employee = dest_models.execute(dest_DB, dest_uid, dest_PASS, 'hr.employee', 'search', check_args)
			if check_dest_employee:
				# Get binary data
				filecontent = base64.b64decode(employee_data['legacy_doc_2'] or '')

				if filecontent:
					FILENAME_DIR = "/opt/DataFiles/"
					FILENAME = False

					try:
						FILENAME = filecontent.decode('utf-8')
					except:
						print("Cannot decode")

					if FILENAME:
						file_path = FILENAME_DIR+str(FILENAME)
						print(file_path)

						content = False
						with open(file_path, 'rb') as f:
							content = base64.b64encode(f.read())

						if content:
							employee_insert = dest_models.execute_kw(dest_DB, dest_uid, dest_PASS, 'hr.employee', 'write', [employee, {
								'legacy_doc_2': content.decode(),
							}])

							if employee_insert:
								count += 1
								print("[" + str(count) + "]" + "UPDATED employee: " + str(employee))
					else:
						employee_insert = dest_models.execute_kw(dest_DB, dest_uid, dest_PASS, 'hr.employee', 'write', [employee, {
							'legacy_doc_2': employee_data['legacy_doc_2'],
						}])

						if employee_insert:
							count += 1
							print("[" + str(count) + "]" + "UPDATED employee: " + str(employee))

update_employee_legacydoc_personal_data()