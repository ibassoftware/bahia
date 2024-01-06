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


# UPDATE employee documents
def update_employee_medical_records():
	print("MIGRATION OF employee documents ON GOING...")
	start = time.time()

	count = 0
	count_update = 0

	args = [('id', '=', 53025)]
	# args = [('document_id', '!=', False)]
	get_employee_doc = src_models.execute(src_DB, src_uid, src_PASS, 'hr.employee_medical_records', 'search', args)
	
	for employee_doc in get_employee_doc:
		employee_doc_fields = [
			'id',
			'employee_med_rec_id',
			'medical_type',
			'document_id',
		]
		employee_doc_data = src_models.execute(src_DB, src_uid, src_PASS, 'hr.employee_medical_records', 'read', employee_doc, employee_doc_fields)

		print(employee_doc_data['employee_med_rec_id'])
		print(employee_doc_data['medical_type'])

		check_args = [('id', '=', employee_doc)]
		check_dest_employee_doc = dest_models.execute(dest_DB, dest_uid, dest_PASS, 'hr.employee_medical_records', 'search', check_args)
		if check_dest_employee_doc:
			employee_update_doc = dest_models.execute_kw(dest_DB, dest_uid, dest_PASS, 'hr.employee_medical_records', 'write', [employee_doc, {
				'document_id': employee_doc_data['document_id'],
			}])

			if employee_update_doc:
				count += 1
				print("[" + str(count) + "]" + "UPDATED employee: " + str(employee_doc_data['employee_med_rec_id']))

update_employee_medical_records()