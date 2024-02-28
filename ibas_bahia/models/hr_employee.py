# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _

from odoo.exceptions import AccessError, UserError, ValidationError
import uuid 
import base64
from cryptography.fernet import Fernet

import datetime
import os
import sys
import base64

import logging

_logger = logging.getLogger(__name__)

YEAR = 365
MONTH = 30
#ALT_255 = '            ' # ALR+255 is a Special Characters in ASCII
ALT_255 =''
DATE_NOW = datetime.datetime.now()
INT_ID_NOW = 0

class HrEmployeeExtend(models.Model):
	_inherit = 'hr.employee'

	# --------------- Validation
	@api.onchange('mobile_phone','work_phone')
	def _check_phone_format(self):
		for record in self:
			if record.mobile_phone and not record.mobile_phone.isdigit():
				raise ValidationError("Please enter a valid phone!")
				# _logger.info("Please enter a valid phone!")
			if record.work_phone and not record.work_phone.isdigit():
				raise ValidationError("Please enter a valid phone!")
				# _logger.info("Please enter a valid phone!")

	#---------------- Functions/Methods
	def getCheckListId(self):
		SQL_QUERY ="SELECT id,1 employee_id ,id checklist_template_id"\
					" FROM hr_checklist_template;"

		rec.env.cr.execute(SQL_QUERY)
		checklistTemplates = self.env.cr.fetchall()
		return checklistTemplates

	def generateFile(self,vals):
		dt_tm_filename = DATE_NOW.strftime("%m%d%Y%H%M%S")
		byte_arr = base64.b64encode('Dummy File')
		document_binary = ""
		bln_must_save = False
		if 'legacy_doc_1' in  vals:
			str_filename = self.filename.rstrip('.pdf') + '_' + dt_tm_filename + '.pdf'
			FILENAME_DIR = "/opt/DataFiles/" + str_filename
			if not isinstance(vals['legacy_doc_1'], bool):
				document_binary = vals['legacy_doc_1']
				byte_arr = base64.b64encode(str_filename)

				vals['legacy_doc_1'] = byte_arr
				with open(FILENAME_DIR, "wb") as f:
					f.write(base64.b64decode(document_binary))
			else:
				is_exists = os.path.isfile(FILENAME_DIR)
				if is_exists:
					os.remove(FILENAME_DIR)

		if 'legacy_doc_2' in  vals:
			str_filename = self.filename2.rstrip('.pdf') + '_' + dt_tm_filename + '.pdf'
			FILENAME_DIR = "/opt/DataFiles/" + str_filename
			if not isinstance(vals['legacy_doc_2'], bool):
				document_binary = vals['legacy_doc_2']   
				byte_arr = base64.b64encode(str_filename)
				vals['legacy_doc_2'] = byte_arr 
				with open(FILENAME_DIR, "wb") as f:
					f.write(base64.b64decode(document_binary))    
			else:
				os.remove(FILENAME_DIR)

		if 'legacy_doc_3' in  vals:
			str_filename = self.filename3.rstrip('.pdf') + '_' + dt_tm_filename + '.pdf'
			FILENAME_DIR = "/opt/DataFiles/" + str_filename
			if not isinstance(vals['legacy_doc_3'], bool):
				document_binary = vals['legacy_doc_3']              
				byte_arr = base64.b64encode(str_filename)
				vals['legacy_doc_3'] = byte_arr
				with open(FILENAME_DIR, "wb") as f:
					f.write(base64.b64decode(document_binary))        
			else:
				os.remove(FILENAME_DIR)

	# Overrides
	@api.model
	def create(self, vals):
		#To Check if Contract Nunber Already Exists
		if 'employee_contract_number' in  vals:
			str_employee_with_contract_number = ""
			employee_model = self.env['hr.employee'].search([('employee_contract_number', '=',vals['employee_contract_number'])])
			if employee_model:
				for employee in employee_model:
					employee_name = ""
					if employee.name:
						employee_name = employee.name
					else:
						if employee.first_name or employee.last_name:
							employee_name = employee.last_name or '' + ', ' + employee.first_name or '' + ' ' + employee.middle_name or ''
					str_employee_with_contract_number += employee_name + '\n'
				raise UserError("Contract number already exists. \n Employee/s: \n" + str_employee_with_contract_number)

		new_id = super(HrEmployeeExtend, self).create(vals)
		#After Creation of Personnel create a User
		lst_groups = []
		if new_id.employee_contract_number != 'N/A':
			new_loggin_name = new_id.last_name + '_' + str(new_id.employee_contract_number)
		else:
			new_loggin_name = new_id.last_name + '_' + str(new_id.employee_number)
		if isinstance(new_id.middle_name, bool):
			new_user_fullname = new_id.first_name + ' ' + new_id.last_name
		else:
			new_user_fullname = new_id.first_name + ' '+ new_id.middle_name + ' ' + new_id.last_name

		model_userinfo = self.env['res.users']
		lst_groups.append(1)
		id_user = model_userinfo.create({
		    'name': new_user_fullname,
		    'login': new_loggin_name,
		    'password':new_loggin_name,
		    'groups_id':   [(6,0,[1])],})        
		new_id.user_id = id_user.id
		return new_id


	def write(self, vals):
		#To Check if Contract Nunber Already Exists
		if 'employee_contract_number' in vals:
			str_employee_with_contract_number = ""
			employee_model = self.env['hr.employee'].search([('employee_contract_number', '=',vals['employee_contract_number'])])
			if employee_model:
				for employee in employee_model:
					employee_name = ""
					if employee.name:
						employee_name = employee.name
					else:
						if employee.first_name or employee.last_name:
							employee_name = employee.last_name or '' + ', ' + employee.first_name or '' + ' ' + employee.middle_name or ''
					str_employee_with_contract_number += employee_name + '\n'
				raise UserError("Contract number already exists. \n Employee/s: \n" + str_employee_with_contract_number)

		# self.generateFile(vals)
		super(HrEmployeeExtend, self).write(vals)
		checklistTemplates = self.env['hr.checklist_template'].search([])
		employeeChecklist = self.env['hr.employee_checklist'].search([])


		for rec in self:
			#Check the Value if Contract Number has been updated then Update the UserName and Password
			if 'employee_contract_number' in vals:
				model_userinfo = self.env['res.users'].search([('id','=', self.user_id.id)])
				#To Check if Contract Number has a PH
				if self.employee_contract_number.find('PH', 0, len(self.employee_contract_number)) > 0:
					new_loggin_name = self.last_name + '_' + str(self.employee_contract_number[self.employee_contract_number.find('PH', 0, len(self.employee_contract_number)): len(self.employee_contract_number)])
				else:
					if len(self.employee_contract_number) < 4:
						new_loggin_name = self.last_name + '_' + self.employee_contract_number.zfill(4) 
					else:
						new_loggin_name = self.last_name + '_' + str(self.employee_contract_number)
				model_userinfo.write({'login': new_loggin_name,'password':new_loggin_name,})   

			for checklistTemplate in checklistTemplates:
				# CHARACTER IS ALT+255 and Special Character in ASCII
				#ALT_255 = '            '
				ALT_255 = ''
				if len(checklistTemplate.checklist_temp_param_1) > 0:
					temp_1 = int(checklistTemplate.checklist_temp_param_1[0])
				else:
					temp_1 = None

				if len(checklistTemplate.checklist_temp_param_2) > 0:
					temp_2 = int(checklistTemplate.checklist_temp_param_2[0])
				else:
					temp_2 = None

				if len(checklistTemplate.checklist_temp_param_3) > 0:
					temp_3 = int(checklistTemplate.checklist_temp_param_3[0])
				else:
					temp_3 = None

				count_Template = self.env['hr.employee_checklist'].search_count([('checklist_template_id', '=', checklistTemplate.id),('employee_id', '=', self.id)])
				if count_Template == 0:
					employeeChecklist.create({
				        'employee_id': self.id,
				        'checklist_template_id': checklistTemplate.id,
				        'param_name_1': temp_1,
				        'param_name_1_value': '',
				        'param_name_1_check': False,
				        'param_name_2': temp_2,
				        'param_name_2_value': ALT_255,
				        'param_name_2_check': False,
				        'param_name_3': temp_3,
				        'param_name_3_value': '',
				        'param_name_3_check': False,
				        'param_name_1_value_visible':  checklistTemplate.checklist_temp_param_1_with_value,
				        'param_name_2_value_visible':  checklistTemplate.checklist_temp_param_2_with_value,
				        'param_name_3_value_visible':  checklistTemplate.checklist_temp_param_3_with_value})

			#Check first if Employment has been updated for the convinience of optimization
			if 'employee_employment' in vals:
				server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
				model_employment_history = self.env['hr.employmenthistory'].search([('employee_employment_id','=',self.id)])
				for x in model_employment_history:
					for emp_history in vals['employee_employment']:
						if x.id == emp_history[1]:
							if emp_history[2] != False:
								if 'date_serviceto' in emp_history[2]:
									if len(emp_history[2]['date_serviceto']) > 0:
										if datetime.datetime.strptime(emp_history[2]['date_serviceto'], '%Y-%m-%d')  <= server_date:
											model_employment_history.create({
                                            'employee_employment_id' : self.id,
                                            'date_servicefrom' : x.date_serviceto,
                                            'employment_status': 23, # AVAILABLE
                                            'object_code' : 174,
                                            'employment_dept_code': x.employment_dept_code and x.employment_dept_code.id or False,
                                            'employment_rank': x.employment_rank and x.employment_rank.id or False,} # AVAILABLE
											)
										break
						else:
							pass
				break               
		return True

	@api.model
	def _getEmpId(self):
		obj_sequence = self.env['ir.sequence']
		return obj_sequence.next_by_code('hr.employee.sequence')

	@api.onchange('first_name','middle_name','last_name')
	def getFullname(self):
		for rec in self:
			if rec.first_name == False:
			    rec.first_name=''
			if rec.middle_name == False:
			    rec.middle_name=''
			if rec.last_name == False:
			    rec.last_name=''
			#rec.name_related = rec.last_name + ", " +  rec.first_name + " " + rec.middle_name
			rec.name =  rec.last_name + ", " +  rec.first_name + " " + rec.middle_name   

	@api.onchange('employee_employment')
	def computeServiceLenght(self):		
		for rec in self:
			totalyears = 0
			getEmployments = rec.employee_employment
			for getEmployment in getEmployments:
				if isinstance(getEmployment.id, models.NewId):
					if getEmployment.date_servicefrom != False and getEmployment.date_serviceto != False:
						date_from = datetime.datetime.strptime(getEmployment.date_servicefrom.strftime("%Y-%m-%d"),"%Y-%m-%d")
						date_to = datetime.datetime.strptime(getEmployment.date_serviceto.strftime("%Y-%m-%d"),"%Y-%m-%d")
						no_of_days =(((abs((date_to - date_from).days) * 24) * 60) * 60)
						_logger.info("computeServiceLenght")
						_logger.info(getEmployment.date_servicefrom)
						_logger.info(getEmployment.date_serviceto)
						_logger.info(no_of_days)
						rec.service_length = rec.service_length + no_of_days

	def getEmployeeID(self):
		prim_key = None
		empids = self.env['hr.employee'].search([('employee_number', '=', self.employee_number)])
		if len(empids) >0:
			prim_key = int(empids[0])
		else:
			prim_key = 0
		self.employee_id = prim_key
		return prim_key

	def getdocumentStatus(self):
		for rec in self:
			server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
			doc_record = self.env['hr.employee_documents'].search([('date_expiry', '<', server_date),('employee_doc_id','=', self.id)])
			for doc in doc_record:
				if not isinstance(doc.document, bool):
					if doc.document.check_for_expiration == True:
						self.documents_status = True
						break
					else:
						self.documents_status = False
				else:
					self.documents_status = False

	def getMedicalStatus(self):
		for rec in self:
			server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
			totaldoc = self.env['hr.employee_medical_records'].search_count([('date_to', '<', server_date),('employee_med_rec_id','=', rec.id)])
			if totaldoc > 0:
				rec.medical_status = True
			else:
				rec.medical_status = False


	def legacy_doc1_getFilename(self):
		for rec in self:
			if rec.employee_number:
				rec.filename = rec.employee_number + '_ConfidentialReports.pdf'
			else:
				rec.filename = 'filename_ConfidentialReports.pdf'

	def legacy_doc2_getFilename(self):
		for rec in self:
			if rec.employee_number:
				rec.filename2 = rec.employee_number + '_PersonalData.pdf'
			else:
				rec.filename2 = 'filename_PersonalData.pdf'

	def legacy_doc3_getFilename(self):
		for rec in self:
			if rec.employee_number:
				rec.filename3 = rec.employee_number + '_PersonalSummary.pdf'
			else:
				rec.filename3 = 'filename_PersonalSummary.pdf'				

	def _checklist_count(self):
		for rec in self:
			checklist_document_model = rec.env['hr.employee.checklist.documents']
			rec.checklist_count =  checklist_document_model.search_count([('employee_id', '=', rec.id)])

	def _checkLatestEmployment(self):
		for rec in self:
			server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
			model_hr_employmenthistory = self.env['hr.employmenthistory'].search([('employee_employment_id', '=', self.id),
																				  ('date_servicefrom', '<=', server_date),
																				  ('date_serviceto', '>=', server_date)])
			if len(model_hr_employmenthistory) > 0:
				model_hr_employmenthistorty_2 = model_hr_employmenthistory.sorted(key=lambda r: r.date_serviceto, reverse = True)
				for employee in model_hr_employmenthistorty_2:
					self.employee_rank = employee.employment_rank.name
					break
				model_hr_employmenthistory = self.env['hr.employmenthistory'].search([('employee_employment_id', '=', self.id)])
				if len(model_hr_employmenthistory) > 0:
					if isinstance(self.employee_rank, bool):
						for employee in model_hr_employmenthistorty_2:
							self.employee_rank = employee.employment_rank.name
							break
					elif len(self.employee_rank) > 0:
						for employee in model_hr_employmenthistorty_2:
							self.employee_rank = employee.employment_rank.name
							break        
			else:
				model_hr_employmenthistory = self.env['hr.employmenthistory'].search([('employee_employment_id', '=', self.id)])
				if len(model_hr_employmenthistory) > 0:
					model_hr_employmenthistorty_2 = model_hr_employmenthistory.sorted(key=lambda r: r.date_serviceto, reverse = True)
					for employee in model_hr_employmenthistorty_2:
						self.employee_rank = employee.employment_rank.name
						break  


	def createExcelFile(self):
		for rec in self:
			pass


	#-------- Attributes/Fields
	# employee_number = fields.Char('Employee Number',select = True, default = _getEmpId)
	employee_number = fields.Char('Employee Number', default = _getEmpId)
	first_name = fields.Char('First name', required = True)
	last_name = fields.Char('Last name', required = True)
	middle_name = fields.Char('Middle name')
	self_alotte = fields.Boolean('Self Allottee?', default = True)
	weight = fields.Char('Medical Condition')
	height = fields.Char('Shoe Size')
	placeof_birth = fields.Char('Place of birth')
	sss_no = fields.Char('SSS No')
	hdmf_no = fields.Char('HDMF No')
	philhealth_no = fields.Char('Philhealth No')
	tin_no = fields.Char('Tin')
	aa_reg_no = fields.Char('AA Registry No')
	service_length = fields.Integer('Service Length')
	focllength = fields.Integer('Foclength')
	incentive_length = fields.Integer('Incentive Length')
	booking_id = fields.Char('Booking ID')
	bankacctno = fields.Text('Bank account number')
	checklistID = fields.Char('Checklist ID')
	ccl_number = fields.Char('CCL Number')
	religion = fields.Many2one('hr.religion', 'Religion')
	marital =  fields.Selection(selection_add=[('single', 'Single'), 
	                              ('married', 'Married'), 
	                              ('widower', 'Widower'), 
	                              ('divorced', 'Divorced'), 
	                              ('seperated', 'Seperated'), 
	                              ('live_in_partner', 'Live-in-partner')], string='Marital Status')
	employee_rank = fields.Text('Rank',store = False,compute ='_checkLatestEmployment')

	pcn = fields.Char('PCN')
	legacy_doc_1 = fields.Binary('Confidential Reports')
	legacy_doc_2 = fields.Binary('Personal Data')
	legacy_doc_3 = fields.Binary('Personal Summary')
	legacy_doc_4 = fields.Binary('Consent Form')
	has_consentform = fields.Boolean('With Consent Form', default=False)

	is_legacy_doc_mig_1 = fields.Boolean(string="Is Confidential Reports Migrated?")
	is_legacy_doc_mig_2 = fields.Boolean(string="Is Personal Data Migrated?")
	is_legacy_doc_mig_3 = fields.Boolean(string="Is Personal Summary Migrated?")
	is_legacy_doc_mig_4 = fields.Boolean(string="Is Consent Form Migrated?")
	
	employee_addresses = fields.One2many('hr.employeeaddress','employee_address_id', readonly=False,copy=False)
	employee_education = fields.One2many('hr.employeducation','employee_education_id', readonly=False,copy=False)
	employee_families = fields.One2many('hr.employee_families','employee_family_relationship_id', readonly=False,copy=False)
	employee_documents = fields.One2many('hr.employee_documents','employee_doc_id', readonly=False,copy=False)
	emloyee_medical = fields.One2many('hr.employee_medical_records','employee_med_rec_id', readonly=False,copy=False)
	employee_licenses = fields.One2many('hr.employeelicenses','employee_licenses_id', readonly=False,copy=False)
	employee_employment = fields.One2many('hr.employmenthistory','employee_employment_id', readonly=False,copy=False)
	employee_checklists = fields.One2many('hr.employee_checklist','employee_id', readonly=False,copy=False)

	employee_checklists_documents = fields.One2many('hr.employee.checklist.documents','employee_id', readonly=False,copy=False)

	employee_id = fields.Integer('employee_id', readonly=False,copy=False,store =False, compute='getEmployeeID')
	documents_status = fields.Boolean('Document status', readonly = True,store = False,compute ='getdocumentStatus')
	medical_status = fields.Boolean('Medical documents', readonly = True,store = False,compute ='getMedicalStatus')
	
	filename = fields.Char('file name', readonly = True,store = False,compute ='legacy_doc1_getFilename')
	filename2 = fields.Char('file name', readonly = True,store = False,compute ='legacy_doc2_getFilename')
	filename3 = fields.Char('file name', readonly = True,store = False,compute ='legacy_doc3_getFilename')
	filename4 = fields.Char('file name', readonly = True,store = False,compute ='legacy_doc4_getFilename')

	description = fields.Text('Description')
	checklist_count =  fields.Integer('Checklist', store = False, compute = "_checklist_count")

	confidential_file = fields.Char('Confidential File')
	personal_file = fields.Char('Personal File')
	personalsummary_file = fields.Char('File Personnal Summary')
	image_file = fields.Char('Image File Summary')

	employee_contract_number = fields.Char('Employee Contract Number', required=True, default='N/A')
	total_years_of_service = fields.Char('Service Length', store=False, compute='getYearMonthDay')


	employee_e_register_number = fields.Char('E-Registration Number')
	employee_e_reg_num_username = fields.Char('User Name')
	employee_e_reg_num_password = fields.Char('Password')

	# Missing fields in Version 15
	message_last_post = fields.Datetime(string='Last Message Date')
	otherid = fields.Char(string='Other ID')



	def generateFile(self,vals):
		dt_tm_filename = DATE_NOW.strftime("%m%d%Y%H%M%S")
		byte_arr = base64.b64encode('Dummy File')
		document_binary = ""
		bln_must_save = False	
		res = super(HrEmployeeExtend, self).generateFile(vals)

		if 'legacy_doc_4' in  vals:
			str_filename = self.filename4.rstrip('.pdf') + '_' + dt_tm_filename + '.pdf'
			FILENAME_DIR = "/opt/DataFiles/" + str_filename
			if not isinstance(vals['legacy_doc_4'], bool):
				document_binary = vals['legacy_doc_4']
				byte_arr = base64.b64encode(str_filename)
				vals['legacy_doc_4'] = byte_arr
				with open(FILENAME_DIR, "wb") as f:
					f.write(base64.b64decode(document_binary))
			else:
				os.remove(FILENAME_DIR)
		return res

	def legacy_doc4_getFilename(self):
		for rec in self:
			if rec.employee_number:
				rec.filename4 = rec.employee_number + '_ConsentForm.pdf'
			else:
				rec.filename4 = 'filename_ConsentForm.pdf'

	def write(self,vals):
		if 'legacy_doc_4' in  vals:
			if vals['legacy_doc_4']:
				vals['has_consentform'] = True
			else:
				vals['has_consentform'] = False
		#else:
		#	vals['has_consentform'] = False

		res = super(HrEmployeeExtend, self).write(vals)
		return res

	def updateWithConsentForm(self):
		for rec in self:
			if rec.has_consentform:
				rec.write({'has_consentform':False})
			else:
				rec.write({'has_consentform':True})


	def getYearMonthDay(self):
		for rec in self:
			str_service_range = ''
			int_year    = 0
			int_month   = 0
			int_day     = 0

			int_final_year  = 0
			int_final_month = 0
			int_final_day   = 0

			str_final_year  = ''
			str_final_month = ''
			str_final_day   = ''

			for employment_history in rec.employee_employment:
				str_service_range = employment_history.service_range
				str_service_range = str_service_range.split()
				if employment_history.employment_status.status_id == 'ACT':
					int_year = int(float(str_service_range[0].replace('Y','')))
					int_month = int(float(str_service_range[1].replace('M','')))
					int_day = int(float(str_service_range[2].replace('D','')))
					int_final_year +=int_year
					int_final_month +=int_month
					int_final_day +=int_day

			if int_final_day > 30:
				int_final_month += int(int_final_day/30)
				int_final_day = (float(int_final_day)/30)  - int(int_final_day/30.00) 
				if int_final_day > 0:
					int_final_day = 30 * int_final_day

			if int_final_month > 12:
				int_final_year += int_final_month/12.00
				str_final_year = str(int_final_year)

				int_final_year = int(str_final_year.split('.')[0])
				int_final_month =  float('.' + str_final_year.split('.')[1])
				if int_final_month > 0:
					int_final_month = int(round(12 * int_final_month))

			rec.total_years_of_service = str(int_final_year) + 'Y ' + str(int_final_month) + 'M ' +  str(int_final_day).split('.')[0]  + 'D'

	def computeEmployeeName(self):
		for rec in self:
			# rec.getFullname()
			if rec.first_name == False:
			    rec.first_name=''
			if rec.middle_name == False:
			    rec.middle_name=''
			if rec.last_name == False:
			    rec.last_name=''

			# resource_id = self.env['resource.resource'].browse(rec.resource_id.id)
			
			# if resource_id:
			# 	rec.name =  rec.last_name + ", " +  rec.first_name + " " + rec.middle_name   

			name = rec.last_name + ", " +  rec.first_name + " " + rec.middle_name
			args = (name, rec.id)
			self.env.cr.execute("UPDATE hr_employee SET name=%s WHERE id=%s", args)


		return True