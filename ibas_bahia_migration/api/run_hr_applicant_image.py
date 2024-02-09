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


# UPDATE applicant image
def update_applicant_image():
	print("MIGRATION OF applicant ON GOING...")
	start = time.time()

	count = 0
	count_update = 0

	args = [('name', 'ilike', '')]
	get_applicant = src_models.execute(src_DB, src_uid, src_PASS, 'hr.applicant', 'search', args)

	if get_applicant:
		for applicant in get_applicant:
			applicant_fields = [
				'id',
				'name',
				'image',
			]
			applicant_data = src_models.execute(src_DB, src_uid, src_PASS, 'hr.applicant', 'read', applicant, applicant_fields)

			print(applicant)
			print(applicant_data['id'])
			print(applicant_data['name'])
			check_args = [('id', '=', applicant	)]
			check_dest_applicant = dest_models.execute(dest_DB, dest_uid, dest_PASS, 'hr.applicant', 'search', check_args)
			if check_dest_applicant:
				applicant_update = dest_models.execute_kw(dest_DB, dest_uid, dest_PASS, 'hr.applicant', 'write', [applicant, {
					'image_1920': applicant_data['image'],
				}])

				if applicant_update:
					count += 1
					print("[" + str(count) + "]" + "UPDATED applicant: " + str(applicant))

update_applicant_image()