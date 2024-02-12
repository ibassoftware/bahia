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
dest_PASS = 'P@5word'

dest_common = client.ServerProxy('{}/xmlrpc/2/common'.format(dest_URL))
dest_uid = dest_common.authenticate(dest_DB, dest_USER, dest_PASS, {})
dest_models = client.ServerProxy('{}/xmlrpc/2/object'.format(dest_URL))


# UPDATE user image
def update_user_image():
	print("MIGRATION OF user ON GOING...")
	start = time.time()

	count = 0
	count_update = 0

	# args = [('id', '=', 54062)]
	args = [('name', 'ilike', '')]
	get_user = src_models.execute(src_DB, src_uid, src_PASS, 'res.users', 'search', args)

	if get_user:
		for user in get_user:
			user_fields = [
				'id',
				'name',
				'image',
			]
			user_data = src_models.execute(src_DB, src_uid, src_PASS, 'res.users', 'read', user, user_fields)

			print(user)
			print(user_data['id'])
			print(user_data['name'])
			check_args = [('id', '=', user	)]
			check_dest_user = dest_models.execute(dest_DB, dest_uid, dest_PASS, 'res.users', 'search', check_args)
			if check_dest_user:
				user_update = dest_models.execute_kw(dest_DB, dest_uid, dest_PASS, 'res.users', 'write', [user, {
					'image_1920': user_data['image'],
				}])

				if user_update:
					count += 1
					print("[" + str(count) + "]" + "UPDATED user: " + str(user))

update_user_image()