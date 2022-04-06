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


class HrEmployeeExtend(models.Model):
	_inherit = 'hr.employee'


	#@api.model
	#def _combine_recordset(self, recordset, first_recordset=False):
	#	if not first_recordset:
	#		return recordset
	#	else:
	#		if recordset:
	#			return recordset

	@api.model
	def getFieldName(self, model_name, field_name):
		field_obj = self.env['ir.model.fields'].sudo().search([('name','=', field_name),
															 ('model_id','=', self.env.ref(model_name).id)])
		return field_obj.field_description or False

			

	@api.multi
	def write(self, vals):
		#raise Warning(vals)
		employee_document_obj = self.env['hr.employee_documents']
		employee_medical_obj = self.env['hr.employee_medical_records']
		employee_licence_obj = self.env['hr.employeelicenses']
		res = super(HrEmployeeExtend, self).write(vals)
		res_groups_follower_ids = False
		#raise Warning(vals)
		if res:
			description =''
			if 'employee_documents' in vals and self.env.user.share == True:
				description += 'Changes Made in Employee Document/s\n'
				for list in vals['employee_documents']:
					#Check Validation
					if list[2]:
						#raise Warning(vals)
						if 'document' not in list[2]:
							employee_document_obj_id = employee_document_obj.search([('id','=', list[1])])
							document_id = employee_document_obj_id.document.id
						else:							
							document_id = list[2]['document']
						if res_groups_follower_ids:
							res_groups_follower_ids += self.env['mail.group'].getNotificationGroups('document', document_id)
						else:
							res_groups_follower_ids = self.env['mail.group'].getNotificationGroups('document', document_id)

						for list_field_name in list[2]:
							if list_field_name == 'document':
								#raise Warning(list[2][list_field_name])
								documenttype_obj =  self.env['hr.documenttype'].sudo().search([('id', '=', list[2][list_field_name])])
								field_value  = ' : ' + documenttype_obj.name
							elif list_field_name == 'file_upload':
								field_value  = 'New File Uploaded'
							else:
								field_value  = ' : ' + str(list[2][list_field_name])
							description += self.getFieldName('extend_bahia_personnel_mngmt_list.model_hr_employee_documents', list_field_name)  + field_value  + '\n'
						#raise Warning(description)
				#Added New Functionality Email
				res_groups_follower_str = ""
				for res_groups_follower_id in res_groups_follower_ids:
					if res_groups_follower_id.email:
						res_groups_follower_str += res_groups_follower_id.email + ","
				email_template_obj =self.env['email.template']
				email_template_obj_id = email_template_obj.sudo().search([('model_id.model','=', 'hr.employee'),
																			 ('name','=', 'Seafarer Changes Notification')])
				if email_template_obj_id:
					#raise Warning(res_groups_follower_str[0:len(res_groups_follower_str)-1])
					values = email_template_obj.sudo().generate_email(email_template_obj_id.id, self.id, context=self.env.context)
					#raise Warning(values['body_html'])
					values['subject'] = "Seafarer's Document Information Change"
					values['email_to'] = res_groups_follower_str[0:len(res_groups_follower_str)-1]
					#values['body_html'] = values['body_html'] %{'tables': "<p>" + description + "</p>", 'system_gen': "<p>This is a system Generated Message. Do Not Reply</p>"}
					values['res_id'] = False
					#raise Warning(values)
					mail_mail_obj = self.env['mail.mail']
					msg_id = mail_mail_obj.sudo().create(values)
					if msg_id:
						mail_mail_obj.sudo().send([msg_id], context=self.env.context) 




						#raise Warning(res_groups_follower_ids)
			if 'emloyee_medical' in vals and self.env.user.share == True:
				description += 'Changes Made in Medical Document/s\n'
				for list in vals['emloyee_medical']:
					#Check Validation
					if list[2]:
						#raise Warning(vals)
						if 'medical_type' not in list[2]:
							employee_document_obj_id = employee_medical_obj.search([('id','=', list[1])])
							document_id = employee_document_obj_id.medical_type.id
						else:							
							document_id = list[2]['medical_type']

						if res_groups_follower_ids:
							res_groups_follower_ids += self.env['mail.group'].getNotificationGroups('medical', document_id)
						else:
							res_groups_follower_ids = self.env['mail.group'].getNotificationGroups('medical', document_id)

						for list_field_name in list[2]:
							if list_field_name == 'medical_type':
								#raise Warning(list[2][list_field_name])
								documenttype_obj =  self.env['hr.medicalrecord'].sudo().search([('id', '=', list[2][list_field_name])])
								field_value  = ' : ' + documenttype_obj.name
							elif list_field_name == 'file_upload':
								field_value  = 'New File Uploaded'
							else:
								field_value  = ' : ' + str(list[2][list_field_name])
							description += self.getFieldName('extend_bahia_personnel_mngmt_list.model_hr_employee_medical_records', list_field_name)  + field_value  + '\n'							
						#raise Warning(res_groups_follower_ids)
				#Added New Functionality Email
				res_groups_follower_str = ""
				for res_groups_follower_id in res_groups_follower_ids:
					if res_groups_follower_id.email:
						res_groups_follower_str += res_groups_follower_id.email + ","
				email_template_obj =self.env['email.template']
				email_template_obj_id = email_template_obj.sudo().search([('model_id.model','=', 'hr.employee'),
																			 ('name','=', 'Seafarer Changes Notification')])
				if email_template_obj_id:
					#raise Warning(res_groups_follower_str[0:len(res_groups_follower_str)-1])
					values = email_template_obj.sudo().generate_email(email_template_obj_id.id, self.id, context=self.env.context)
					#raise Warning(values['body_html'])
					values['subject'] = "Seafarer's Medical Information Change"
					values['email_to'] = res_groups_follower_str[0:len(res_groups_follower_str)-1]
					#values['body_html'] = values['body_html'] %{'tables': "<p>" + description + "</p>", 'system_gen': "<p>This is a system Generated Message. Do Not Reply</p>"}
					values['res_id'] = False
					#raise Warning(values)
					mail_mail_obj = self.env['mail.mail']
					msg_id = mail_mail_obj.sudo().create(values)
					if msg_id:
						mail_mail_obj.sudo().send([msg_id], context=self.env.context) 				

			if 'employee_licenses' in vals and self.env.user.share == True:
				description += 'Changes Made in License/s\n'
				for list in vals['employee_licenses']:
					#Check Validation
					if list[2]:
						#raise Warning(vals)
						if 'employee_licenses' not in list[2]:
							employee_document_obj_id = employee_licence_obj.search([('id','=', list[1])])
							document_id = employee_document_obj_id.license.id
						else:							
							document_id = list[2]['license']

						if res_groups_follower_ids:
							res_groups_follower_ids += self.env['mail.group'].getNotificationGroups('license', document_id)
						else:
							res_groups_follower_ids = self.env['mail.group'].getNotificationGroups('license', document_id)

						for list_field_name in list[2]:
							if list_field_name == 'license':
								#raise Warning(list[2][list_field_name])
								documenttype_obj =  self.env['hr.license'].sudo().search([('id', '=', list[2][list_field_name])])
								field_value  = ' : ' + documenttype_obj.name
							elif list_field_name == 'file_upload':
								field_value  = 'New File Uploaded'
							else:
								field_value  = ' : ' + str(list[2][list_field_name])
							description += self.getFieldName('extend_bahia_personnel_mngmt_list.model_hr_employeelicenses', list_field_name)  + field_value  + '\n'
				#Added New Functionality Email
				res_groups_follower_str = ""
				for res_groups_follower_id in res_groups_follower_ids:
					if res_groups_follower_id.email:
						res_groups_follower_str += res_groups_follower_id.email + ","
				email_template_obj =self.env['email.template']
				email_template_obj_id = email_template_obj.sudo().search([('model_id.model','=', 'hr.employee'),
																			 ('name','=', 'Seafarer Changes Notification')])
				if email_template_obj_id:
					#raise Warning(res_groups_follower_str[0:len(res_groups_follower_str)-1])
					values = email_template_obj.sudo().generate_email(email_template_obj_id.id, self.id, context=self.env.context)
					#raise Warning(values['body_html'])
					values['subject'] = "Seafarer's License Information Change"
					values['email_to'] = res_groups_follower_str[0:len(res_groups_follower_str)-1]
					#values['body_html'] = values['body_html'] %{'tables': "<p>" + description + "</p>", 'system_gen': "<p>This is a system Generated Message. Do Not Reply</p>"}
					values['res_id'] = False
					#raise Warning(values)
					mail_mail_obj = self.env['mail.mail']
					msg_id = mail_mail_obj.sudo().create(values)
					if msg_id:
						mail_mail_obj.sudo().send([msg_id], context=self.env.context) 						
			if res_groups_follower_ids:
				users_ids = []
				for follower_id in res_groups_follower_ids:
					
					res_users_obj = self.env['res.users'].sudo().search([('partner_id','=',follower_id.id)])
					if res_users_obj:
						users_ids.append(res_users_obj.id)

				values = {'status': 'draft',
						  'title': u"Seafarer's Info Change",
						  'message': " %s Information had been Updated" % self.name,
						  'employee_id': self.id,
						  'description':description,
						  'partner_ids': [(6, 0, users_ids)]}
				self.env['popup.notification'].create(values)
		return res


