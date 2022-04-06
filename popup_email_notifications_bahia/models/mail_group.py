# -*- coding: utf-8 -*-
import importlib
from openerp import models, fields,api
from openerp.exceptions import except_orm, Warning, RedirectWarning,ValidationError

import datetime
import os
import sys
import base64

#FOR EXCEL FILE
import xlwt
from cStringIO import StringIO

YEAR = 365
MONTH = 30
DATE_NOW = datetime.datetime.now()
INT_ID_NOW = 0


class MailGroup(models.Model):
	_inherit = 'mail.group'

	data_check_selection = fields.Selection([('document', 'Documents'), 
											 ('medical', 'Medical'), 
											 ('license', 'License')], 'Document Types')

	document_ids = fields.Many2many('hr.documenttype', 
									'document_mail_group_rel', 
									'mail_group_id', 
									'document_id', 
									'Documents List')

	medical_ids = fields.Many2many('hr.medicalrecord', 
								   'medical_mail_group_rel', 
								   'mail_group_id', 
								   'medical_id', 
								   'Medical Document Type')

	license_ids = fields.Many2many('hr.license', 
								   'license_mail_group_rel', 
								   'mail_group_id', 
								   'license_id', 
								   'License Type')

	@api.model
	def getNotificationGroups(self, document_type, document_type_id):		
		mail_group_objs = self.env['mail.group'].sudo().search([('data_check_selection', '=',document_type)])
		if mail_group_objs:
			follower_ids = False
			for mail_group_obj in mail_group_objs:
				#Check if Groups has Specific Documents to Check
				get_followers = True
				if mail_group_obj[document_type + '_ids']:
					if  document_type_id not in mail_group_obj[document_type + '_ids'].ids:
						get_followers = False
				#else:
				#	get_followers = True

				if get_followers:
					if not follower_ids:
						follower_ids = mail_group_obj.message_follower_ids
					else:
						follower_ids += mail_group_obj.message_follower_ids
			#raise Warning(follower_ids)
			return follower_ids
		return False



