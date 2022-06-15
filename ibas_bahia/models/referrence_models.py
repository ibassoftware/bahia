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

DATA_TYPE = [
('text', 'Text'),
('date', 'Date'),
('Integer', 'Integer')

]



CHECKLIST_DOCUMENT_TYPE = [
('none', 'None'),
('document', 'Document'),
('license', 'License'),
('medical', 'Medical')

]


RETRIEVE_RECORD_IN_HISTORY = [
('none', 'None'),
('latest_doc', 'Latest Doc.'),
('oldest_doc', 'Old Doc.'),
]

YEAR = 365
MONTH = 30
#ALT_255 = '            ' # ALR+255 is a Special Characters in ASCII
ALT_255 =''
DATE_NOW = datetime.datetime.now()
INT_ID_NOW = 0

#Abstract Implementation
class ParameterModel(models.AbstractModel):
	_name ='hr.abs.parameter'
	_description = 'HR Parameter'

	code = fields.Char('Code', required=True)
	name = fields.Char('Name', required=True)
	description = fields.Text('Description')
	ref_rec_id = fields.Char(string='Reference ID')

class HrEmployeeAddresses(models.Model):
	_name = 'hr.employeeaddress'
	_description = 'Employee Addresses'

	employee_address_id = fields.Many2one('hr.employee','Employee Addresses')
	addresstype = fields.Many2one('hr.addresstype','Address Type')
	address_1 = fields.Char('Address 1')
	address_2 = fields.Char('Address 2')
	address_3 = fields.Char('Address 3')
	city = fields.Char('City')
	province = fields.Char('Province')
	country = fields.Many2one('res.country', 'Country')
	telephone_number = fields.Char('Landline number')
	mobile_number = fields.Char('Mobile number')
	email_number = fields.Char('E-mail')

class HrEmployeeEducation(models.Model):
	_name = 'hr.employeducation'
	_description = 'Employee Education'

	employee_education_id = fields.Many2one('hr.employee')
	schooltype = fields.Many2one('hr.recruitment.degree','Degree')
	name_school = fields.Char('School/College University')
	date_from = fields.Date('Date From')
	date_to = fields.Date('Date To')
	school_address = fields.Char('Place')
	description = fields.Text('Remarks')

	@api.onchange('date_to')
	def checkDate(self):
		for rec in self:
			if rec.date_to < rec.date_from:
				raise ValidationError('Date to is less than the Date from.')

	@api.constrains('date_to','date_from')
	def checkConstrainDate(self):
		for rec in self:
			if rec.date_to < rec.date_from:
				raise ValidationError('Date to is less than the Date from.')

class HrEmployeeFamilies(models.Model):
	_name = 'hr.employee_families'
	_description = 'Employee Families'

	_order = 'employee_family_relationship_id,relation_level'

	@api.model
	def getLastLevel(self):
		return 1

	# Overrides
	@api.model
	def create(self, vals):
		#count_employee_families = self.env['hr.employee_families'].search_count([('employee_family_relationship_id', '=', vals['employee_family_relationship_id']),
		#                                                                    ('relation_level', '=', vals['relation_level'])])
		#if count_employee_families > 0:
		#    raise Warning('Relation Level has already define in Employee families.')
		new_record = super(HrEmployeeFamilies, self).create(vals)
		return new_record    

	def write(self, vals):
		#for rec in self:
		#	count_employee_families = self.env['hr.employee_families'].search_count([('employee_family_relationship_id', '=', rec.employee_family_relationship_id.id),('relation_level', '=', rec.relation_level)])
		super(HrEmployeeFamilies, self).write(vals)
		return True            

	employee_family_relationship_id = fields.Many2one('hr.employee')
	relation_level = fields.Integer('Level', default = getLastLevel)
	relationship = fields.Many2one('hr.familyrelations','Relationship')
	address_1 = fields.Char('Address 1')
	address_2 = fields.Char('Address 2')
	address_3 = fields.Char('Address 3')
	is_beneficiary = fields.Boolean('Beneficiary', default = True)
	is_allottee = fields.Boolean('Allottee', default = True)
	is_living = fields.Boolean('Living', default = True)
	occupation = fields.Char('Occupation')
	bank_details = fields.Text('Bank Details')
	telephone_number = fields.Char('Landline number')
	mobile_number = fields.Char('Mobile number')
	email_number = fields.Char('E-mail')
	city = fields.Char('City')
	province = fields.Char('Province')
	country_id = fields.Many2one('res.country', 'Nationality')
	gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')
	birthday = fields.Date("Date of Birth")
	full_name = fields.Char('Name', readonly=True)
	first_name = fields.Char('First name') #required = True
	last_name = fields.Char('Last name') #required = True
	middle_name = fields.Char('Middle name') #required = True
	placeof_birth = fields.Char('Place of birth')

class HrEmployeeDocuments(models.Model):
	_name = 'hr.employee_documents'
	_description = 'Employee Documents'

	_order = 'date_expiry,date_expiry,document'

	employee_doc_id =  fields.Many2one('hr.employee')
	document = fields.Many2one('hr.documenttype','Document Type')
	document_number = fields.Char('Document ID')
	date_issued = fields.Date('Date Issued',default = DATE_NOW)
	date_expiry = fields.Date('Date Expiry',default = DATE_NOW)
	issuing_authority = fields.Char('Issuing Authority')
	place_ofissue = fields.Char('Place of Issue')
	expired = fields.Char('Expired?',store = False,compute ='checkDocExpiration')

	filename = fields.Char(string='file name')
	file_upload = fields.Binary('Document File')

	def checkDocExpiration(self):
		for rec in self:
			if not isinstance(rec.document, bool):
				server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
				if rec.document.check_for_expiration == True:
					if (rec.date_expiry == False):
						rec.expired = 'NOT'
					else:
						dt_date_expiry = datetime.datetime.strptime(rec.date_expiry ,"%Y-%m-%d")
						if dt_date_expiry < server_date:
							rec.expired = 'EXP'
						else:
							rec.expired = 'NOT'
				else:
					rec.expired = 'NOT'
			else:
				rec.expired = 'NOT'

	@api.onchange('date_expiry')
	def checkDate(self):
		for rec in self:
			if rec.date_expiry < rec.date_issued:
				raise ValidationError('Date expiry is less than the Date issued.')

	@api.constrains('date_issued','date_expiry' )
	def checkConstrainDate(self):
		for rec in self:
			if rec.date_expiry < rec.date_issued:
				raise ValidationError('Date expiry is less than the Date issued.')

class HrEmployeeMedicalRecords(models.Model):
	_name = 'hr.employee_medical_records'
	_description = 'Employee Medical Records'

	employee_med_rec_id = fields.Many2one('hr.employee')
	medical_type = fields.Many2one('hr.medicalrecord','Medical')
	medical_clinic = fields.Many2one('hr.clinic','Clinic')
	date_from = fields.Date('Date From') #,required = True
	date_to = fields.Date('Date To') #,required = True
	expired = fields.Char('Expired?',store = False,compute ='checkDocExpiration')

	@api.constrains('date_from','date_to')
	def checkConstrainDate(self):
		for rec in self:
			if not isinstance(rec.date_from,bool):
				if len(rec.date_from) > 0:
					if rec.date_to < rec.date_from:
						pass

	def checkDocExpiration(self):
		for rec in self:
			rec.expired = 'NOT'

	@api.onchange('date_to')
	def checkDate(self):
		for rec in self:
			if not isinstance(rec.date_from,bool):
				if len(rec.date_from) > 0:
					if rec.date_to < rec.date_from:
						raise ValidationError('Date to is less than the Date from.')

class HrEmployeeLicenses(models.Model):
	_name = 'hr.employeelicenses'
	_description = 'Employee Licenses'

	employee_licenses_id = fields.Many2one('hr.employee')
	licensetype = fields.Many2one('hr.licensetype','License Type', required=True)
	license = fields.Many2one('hr.license','License') #, required=True
	doc_number = fields.Char('Document Number', required=True)
	country = fields.Many2one('res.country', 'Country', required=True)
	date_issued = fields.Date('Issue')
	date_expiry = fields.Date('Expiry')    
	place_issue = fields.Char('Place Issue', required=True)
	authority_issue = fields.Char('Authority Issue')
	remarks = fields.Text('Remarks')

	filename = fields.Char(string='file name')
	file_upload = fields.Binary('Document File')

class HrEmployeeEmployment(models.Model):
	YEAR = 365
	MONTH = 30

	_name = 'hr.employmenthistory'
	_description = 'Employment History'
	_order =  'employee_employment_id, date_servicefrom desc'

	employee_employment_id = fields.Many2one('hr.employee')
	date_departure =fields.Date('Departure Date')
	date_servicefrom =fields.Date('Service from')
	date_serviceto =fields.Date('Service to')
	object_name = fields.Char('Object')
	object_code = fields.Many2one('hr.vessel','Vessel') #, required =True
	object_code_category = fields.Many2one('hr.vesselcategory','Vessel Category')
	employment_dept_code = fields.Many2one('hr.ship.department','Department') #, required =True
	employment_rank = fields.Many2one('hr.rank','Rank')
	employment_status = fields.Many2one('hr.employment.status','Status')
	remarks = fields.Text('Remarks')
	place_signOn = fields.Many2one('hr.port', 'Sign On')
	place_signOff = fields.Many2one('hr.port', 'Sign Off')
	service_range = fields.Char('Service range',store = False,compute ='getYearMonthDay')

	@api.onchange('object_code')
	def _changeCategory(self):
		for rec in self:
			rec.object_code_category = rec.object_code.vessel_category


	def getYearMonthDay(self):
		for rec in self:
			no_of_years = 0
			no_of_months = 0
			no_of_day = 0
			if rec.date_servicefrom == False or rec.date_serviceto == False:
				rec.service_range = '0Y 0M 0D'
			else:
				date_from_str = datetime.datetime.strftime(rec.date_servicefrom ,"%Y-%m-%d")
				date_to_str = datetime.datetime.strftime(rec.date_serviceto ,"%Y-%m-%d")
				date_from = datetime.datetime.strptime(date_from_str ,"%Y-%m-%d")
				date_to = datetime.datetime.strptime(date_to_str ,"%Y-%m-%d")

				_logger.info("YOW")
				_logger.info(date_from)
				_logger.info(date_to)

				no_of_days = abs((date_to - date_from).days) + 1
				# Get Years of Service
				#raise Warning(no_of_days)
				no_of_years = abs(no_of_days/365)
				no_of_days =  no_of_days - (no_of_years * 365)
				no_of_months = abs(no_of_days/30)
				no_of_days = no_of_days - (no_of_months * 30)
				no_of_day = no_of_days

				_logger.info(no_of_years)
				_logger.info(no_of_days)
				_logger.info(no_of_months)

			rec.service_range = str(no_of_years) + 'Y ' + str(no_of_months) + 'M ' +  str(no_of_day)  + 'D'
#OLD
class EmployeeCheckList(models.Model):
	_name = 'hr.employee_checklist'
	_description = 'Employee Checklist'

	employee_id = fields.Many2one('hr.employee')
	checklist_template_id = fields.Many2one('hr.checklist_template')

	param_name_1 = fields.Many2one('hr.checklist', 'Parameter 1')
	param_name_2 = fields.Many2one('hr.checklist', 'Parameter 2')
	param_name_3 = fields.Many2one('hr.checklist', 'Parameter 3')

	param_name_1_value = fields.Char("Parameter 1 value")
	param_name_2_value = fields.Char("Parameter 2 value")
	param_name_3_value = fields.Char("Parameter 3 value")

	param_name_1_check = fields.Boolean("Parameter 1 Checked?")
	param_name_2_check = fields.Boolean("Parameter 2 Checked?")
	param_name_3_check = fields.Boolean("Parameter 3 Checked?")

	param_name_1_value_visible = fields.Boolean("Parameter 1 Value visible?")
	param_name_2_value_visible = fields.Boolean("Parameter 2 Value visible?")
	param_name_3_value_visible = fields.Boolean("Parameter 3 Value visible?")

	issued_at = fields.Char("Issued at")
	date_issued = fields.Date("Date issued")
	date_expiry = fields.Date("Date Expiry")

	@api.onchange('date_expiry')
	def checkDate(self):
		for rec in self:
			if self.date_expiry < self.date_issued:
				raise ValidationError('Date expiry is less than the Date issued.')

class EmployeeChecklist(models.Model):
	_name = "hr.employee.checklist.documents"
	_description = 'Employee Checklist Documents'
	_inherit = 'mail.thread'
	_order =  'checklist_no, name'



	employee_id = fields.Many2one('hr.employee')

	checklist_no = fields.Integer('Checklist No.', store=True) #, compute = "readonly_values"
	name = fields.Char('Name', store=True) # , compute = "readonly_values"
	employee_number = fields.Char('Employee Number', store=True, compute = "readonly_values")
	joining_date = fields.Date('Joining Date')
	vessel_information = fields.Char('Vessel', store=True, compute = "readonly_values")
	position_information = fields.Char('Position', store=True, compute = "readonly_values")
	medical_date = fields.Char('Date of Med')
	visa_date = fields.Char('Date of Visa')
	contact_number = fields.Char('Contact Number')
	signoff_date = fields.Date('Date Signoff')
	reported_date = fields.Date('Date Reported') 

	employee_checklists_documents_list = fields.One2many('hr.employee.checklist.documents.list','employee_checklist_document', readonly=False,copy=False)
	employee_checklists_documents_list_main = fields.One2many('hr.employee.checklist.documents.list.main','employee_checklist_document', readonly=False,copy=False)

	#Other Data
	us_visa_boolean = fields.Boolean('US Visa', default= False)
	us_visa_latest_document = fields.Char('US Visa Document ID')
	us_visa_previous_document = fields.Char('US Visa Previous Document ID')
	us_visa_IssuedAt_document = fields.Char('US Visa Previous Document ID')    
	us_visa_expiring_date = fields.Date('Expiring Date')


	us_visa2_boolean = fields.Boolean('VISA II', default= False)
	us_visa2_latest_document = fields.Char('VISA II ID')
	us_visa2_previous_document = fields.Char('VISA II Previous Document ID')
	us_visa2_IssuedAt_document = fields.Char('VISA II Previous Document ID')    
	us_visa2_expiring_date = fields.Date('Expiring Date')

	peme_boolean = fields.Boolean('PEME', default= False)
	peme_latest_document = fields.Char('Peme')
	peme_schedule_date = fields.Date('Schedule')
	clinic = fields.Char('Clinic')

	vessel_id = fields.Many2one('hr.vessel', string='Vessel')
	position_id = fields.Many2one('hr.rank', string='Position')
	department_id = fields.Many2one('hr.ship.department', string='Department')	


	def getUseridName(self):		
		return self.env['res.users'].search([('id','=', self._uid)]).name


	#Remove all edited and updated records and get 
	#all the records again
	def regenerateChecklistDocuments(self):
		self.ensure_one()
		server_date = DATE_NOW.strftime("%d/%m/%Y")
		model_list_document_main =self.env['hr.employee.checklist.documents.list'].search([('employee_checklist_document', '=', self.id)])
		model_list_document =self.env['hr.employee.checklist.documents.list.main'].search([('employee_checklist_document', '=', self.id)])

		model_checklist_document = self.env['hr.employee.checklist.documents'].search([('id', '=', self.id)])
		#Remove first all the Data
		model_list_document_main.unlink()
		model_list_document.unlink()
		self.createChecklistDocumentList(model_checklist_document)
		self.createChecklistDocumentList_main(model_checklist_document)

		for document in self.employee_checklists_documents_list:
			model_res_users = self.env['res.users'].search([('id', '=', self._uid)])
			document.change_by = model_res_users.name
			document.change_date = server_date

		message ="""<span>Regenerate Checklist</span>
					<div><b>Triggered by</b>: %(user)s </div>
				 """ %{'user': self.getUseridName()}
		self.message_post(body=message)

	def updateChecklist(self):
		self.ensure_one()
		self.createChecklistDocumentList('')
		message ="""<span>Automated updating of Checklist</span>
					<div><b>Triggered by</b>: %(user)s </div>
					""" %{'user': self.getUseridName()}
		self.message_post(body=message)

	def readonly_values_2(self, vals):
		values = {}
		server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
		employee_info_model = self.env['hr.employee'].search([('id', '=', vals['employee_id'])])
		values.update({'name': employee_info_model.last_name + ", " + employee_info_model.first_name })
		values.update({'employee_number': employee_info_model.employee_number})

		employment_history_model = self.env['hr.employmenthistory'].search([('employee_employment_id', '=', employee_info_model.id), 
																			('date_serviceto', '>=', server_date)], limit = 1)

		total_checklist_document = self.env['hr.employee.checklist.documents'].search_count([('employee_id', '=', employee_info_model.id)])
		if total_checklist_document  == 0:
			values.update({'checklist_no': 1})
		else:
			values.update({'checklist_no': total_checklist_document + 1})

		values.update({'vessel_information': employment_history_model.object_code.name})
		values.update({'position_information': employment_history_model.employment_rank.name})
		return values

	def readonly_values(self):
		self.name = self.employee_id.last_name + ", " + self.employee_id.first_name
		self.employee_number = self.employee_id.employee_number
		#Get the Employment History
		server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
		employment_history_model = self.env['hr.employmenthistory'].search([('employee_employment_id', '=', self.employee_id.id),('date_serviceto', '>=', server_date)], limit = 1)

		# Get the Checklist Number
		total_checklist_document = self.env['hr.employee.checklist.documents'].search_count([('employee_id', '=', self.employee_id.id)])
		if self.checklist_no == 0:
			if total_checklist_document == 0:
				self.checklist_no = 1
			else:
				self.checklist_no = total_checklist_document + 1

		#Get the Vessel Information
		if isinstance(self.vessel_information, bool):
			self.vessel_information = employment_history_model.object_code.name
		elif len(self.vessel_information) == 0:
			self.vessel_information = employment_history_model.object_code.name

		#Get the Position
		if isinstance(self.position_information, bool):
			self.position_information = employment_history_model.employment_rank.name
		elif len(self.position_information) == 0:
			self.position_information = employment_history_model.employment_rank.name

	@api.onchange('employee_id')
	def onchange_employee_id(self):
		for rec in self:
			rec.readonly_values()

	# @api.model
	# def createChecklistDocumentList_main(self, pObjRecord):
	# 	checklistTemplates = self.env['hr.checklist_template'].search([])
	# 	employeeChecklist = self.env['hr.employee.checklist.documents.list.main'].search([])
	# 	#Write Now for the Sake of Demo 
	# 	#This must be hardcoded

	# 	#FOR US VISA
	# 	if len(pObjRecord) == 0:
	# 		record_id = self.id
	# 		employee_id = self.employee_id.id
	# 	else:
	# 		record_id = pObjRecord.id
	# 		employee_id = pObjRecord.employee_id.id

	# 	vals = {'employee_checklist_document': record_id}

	# 	checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_US_VISA_MAIN_CONSTANT')])
	# 	temp_1 = checklistTemplates.id
	# 	vals.update({
	# 	            'param_name_1': temp_1,
	# 	            'param_name_1_value': '',
	# 	            'param_name_1_check': False,
	# 	            'param_name_1_value_visible':  True,
	# 	            'param_name_1_check_visible':  True,})

	# 	checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_US_VISA_PREVIOUS_CONSTANT')])
	# 	temp_1 = checklistTemplates.id
	# 	vals.update({
	# 	            'param_name_2': temp_1,
	# 	            'param_name_2_value': '',
	# 	            'param_name_2_check': False,
	# 	            'param_name_2_value_visible':  True,
	# 	            'param_name_2_check_visible':  False,})

	# 	checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_US_VISA_ISSUED_AT_CONSTANT')])
	# 	temp_1 = checklistTemplates.id
	# 	vals.update({
	# 	            'param_name_3': temp_1,
	# 	            'param_name_3_value': '',
	# 	            'param_name_3_check': False,
	# 	            'param_name_3_value_visible':  True,
	# 	            'param_name_3_check_visible':  False,})

	# 	rec = employeeChecklist.create(vals)
	# 	rec.getEmployeeDocuments_Temporary(rec)
	# 	#FOR US VISA EXPIRATION DATE
	# 	vals = {'employee_checklist_document': record_id}
	# 	checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_US_VISA_EXPIRY_DATE_CONSTANT')])
	# 	temp_1 = checklistTemplates.id
	# 	vals.update({
	# 	            'param_name_2': temp_1,
	# 	            'param_name_2_value': '',
	# 	            'param_name_2_check': False,
	# 	            'param_name_2_value_visible':  True,
	# 	            'param_name_2_check_visible':  False,})
	# 	rec = employeeChecklist.create(vals)
	# 	rec.getEmployeeDocuments_Temporary(rec)

	# 	#FOR VISA 2
	# 	vals = {'employee_checklist_document': record_id}
	# 	checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_VISA_II_CONSTANT')])
	# 	temp_1 = checklistTemplates.id
	# 	vals.update({
	# 	            'param_name_1': temp_1,
	# 	            'param_name_1_value': '',
	# 	            'param_name_1_check': False,
	# 	            'param_name_1_value_visible':  True,
	# 	            'param_name_1_check_visible':  True,})   
	# 	employeeChecklist.create(vals)     

	# 	#FOR PEME
	# 	vals = {'employee_checklist_document': record_id}

	# 	checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_PEME_CONSTANT')])
	# 	temp_1 = checklistTemplates.id
	# 	vals.update({
	# 	            'param_name_1': temp_1,
	# 	            'param_name_1_value': '',
	# 	            'param_name_1_check': False,
	# 	            'param_name_1_value_visible':  True,
	# 	            'param_name_1_check_visible':  True,})

	# 	checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_SCHEDULE_PEME_CONSTANT')])
	# 	temp_1 = checklistTemplates.id
	# 	vals.update({
	# 	            'param_name_2': temp_1,
	# 	            'param_name_2_value': '',
	# 	            'param_name_2_check': False,
	# 	            'param_name_2_value_visible':  True,
	# 	            'param_name_2_check_visible':  False,})

	# 	checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_PEME_CLINIC_CONSTANT')])
	# 	temp_1 = checklistTemplates.id
	# 	vals.update({
	# 	            'param_name_3': temp_1,
	# 	            'param_name_3_value': '',
	# 	            'param_name_3_check': False,
	# 	            'param_name_3_value_visible':  True,
	# 	            'param_name_3_check_visible':  False,})
	# 	employeeChecklist.create(vals)

	# @api.model
	# def createChecklistDocumentList(self, pObjRecord):
	# 	checklistTemplates = self.env['hr.checklist_template'].search([])
	# 	employeeChecklist = self.env['hr.employee.checklist.documents.list'].search([])

	# 	for checklistTemplate in checklistTemplates:
	# 		if len(checklistTemplate.checklist_temp_param_1) > 0:
	# 			temp_1 = int(checklistTemplate.checklist_temp_param_1[0])
	# 		else:
	# 			temp_1 = None

	# 		if len(checklistTemplate.checklist_temp_param_2) > 0:
	# 			temp_2 = int(checklistTemplate.checklist_temp_param_2[0])
	# 		else:
	# 			temp_2 = None

	# 		if len(checklistTemplate.checklist_temp_param_3) > 0:
	# 			temp_3 = int(checklistTemplate.checklist_temp_param_3[0])
	# 		else:
	# 			temp_3 = None

	# 		if len(checklistTemplate.checklist_temp_param_4) > 0:
	# 			temp_4 = int(checklistTemplate.checklist_temp_param_4[0])
	# 		else:
	# 			temp_4 = None           

	# 		if len(pObjRecord) == 0:
	# 			record_id = self.id
	# 			employee_id = self.employee_id.id
	# 		else:
	# 			record_id = pObjRecord.id
	# 			employee_id = pObjRecord.employee_id.id

	# 		count_Template = self.env['hr.employee.checklist.documents.list'].search_count([('checklist_template_id', '=', checklistTemplate.id),('employee_checklist_document', '=', record_id)])

	# 		if count_Template == 0:
	# 			#Get First all the Documents Needed OLd new and How the Field has been setup by the User in 
	# 			#Checklist Template
	# 			employee_checklist_id = employeeChecklist.create({
	# 			    'employee_checklist_document': record_id,
	# 			    'checklist_template_id': checklistTemplate.id,
	# 			    'param_name_1': temp_1,
	# 			    'param_name_1_value': '',
	# 			    'param_name_1_check': False,
	# 			    'param_name_2': temp_2,
	# 			    'param_name_2_value': ALT_255,
	# 			    'param_name_2_check': False,
	# 			    'param_name_3': temp_3,
	# 			    'param_name_3_value': '',
	# 			    'param_name_3_check': False,
	# 			    'param_name_4': temp_4,
	# 			    'param_name_4_value': '',
	# 			    'param_name_4_check': False,
	# 			    'param_name_1_value_visible':  checklistTemplate.checklist_temp_param_1_with_value,
	# 			    'param_name_2_value_visible':  checklistTemplate.checklist_temp_param_2_with_value,
	# 			    'param_name_3_value_visible':  checklistTemplate.checklist_temp_param_3_with_value,
	# 			    'param_name_4_value_visible':  checklistTemplate.checklist_temp_param_4_with_value,
	# 			    'param_name_1_check_visible':  checklistTemplate.checklist_temp_param_1_check_value,
	# 			    'param_name_2_check_visible':  checklistTemplate.checklist_temp_param_2_check_value,
	# 			    'param_name_3_check_visible':  checklistTemplate.checklist_temp_param_3_check_value,
	# 			    'param_name_4_check_visible':  checklistTemplate.checklist_temp_param_4_check_value,

	# 			    'has_date_issued': checklistTemplate.checklist_temp_row_with_dateissued,
	# 			    'has_issued_at': checklistTemplate.checklist_temp_row_with_dateissued,
	# 			    'has_date_expiry': checklistTemplate.checklist_temp_param_1_with_dateexpired,
	# 			    'has_changed_by':checklistTemplate.checklist_temp_param_1_with_changeby,
	# 			    'has_change_date': checklistTemplate.checklist_temp_param_1_with_changedate, 
	# 			    })
	# 	employeeChecklist.getDataFromDocuments(record_id, employee_id)


	@api.model
	def createChecklistDocumentList(self, pObjRecord):
		checklistTemplates = self.env['hr.checklist_template'].search([('blank_row','=', False)])
		employeeChecklist = self.env['hr.employee.checklist.documents.list'].search([])
		for checklistTemplate in checklistTemplates:
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

			if len(checklistTemplate.checklist_temp_param_4) > 0:
				temp_4 = int(checklistTemplate.checklist_temp_param_4[0])
			else:
				temp_4 = None           

			if len(pObjRecord) == 0:
				record_id = self.id
				employee_id = self.employee_id.id
			else:
				record_id = pObjRecord.id
				employee_id = pObjRecord.employee_id.id

			count_Template = self.env['hr.employee.checklist.documents.list'].search_count([('checklist_template_id', '=', checklistTemplate.id),
																							('employee_checklist_document', '=', record_id)])

			if count_Template == 0:
				employee_checklist_id = employeeChecklist.create({
						'employee_checklist_document': record_id,
						'checklist_template_id': checklistTemplate.id,
						'param_name_1': temp_1,
						'param_name_2': temp_2,
						'param_name_3': temp_3,
						'param_name_4': temp_4,
						'param_name_1_value_visible':  checklistTemplate.checklist_temp_param_1_with_value,
						'param_name_2_value_visible':  checklistTemplate.checklist_temp_param_2_with_value,
						'param_name_3_value_visible':  checklistTemplate.checklist_temp_param_3_with_value,
						'param_name_4_value_visible':  checklistTemplate.checklist_temp_param_4_with_value,
						'param_name_1_check_visible':  checklistTemplate.checklist_temp_param_1_check_value,
						'param_name_2_check_visible':  checklistTemplate.checklist_temp_param_2_check_value,
						'param_name_3_check_visible':  checklistTemplate.checklist_temp_param_3_check_value,
						'param_name_4_check_visible':  checklistTemplate.checklist_temp_param_4_check_value,

						'has_date_issued': checklistTemplate.checklist_temp_row_with_dateissued,
						'has_issued_at': checklistTemplate.checklist_temp_row_with_dateissued,
						'has_date_expiry': checklistTemplate.checklist_temp_param_1_with_dateexpired,
						'has_changed_by':checklistTemplate.checklist_temp_param_1_with_changeby,
						'has_change_date': checklistTemplate.checklist_temp_param_1_with_changedate, })
		employeeChecklist.getDataFromDocuments(record_id, employee_id) 


	@api.model
	def createChecklistDocumentList_main(self, pObjRecord):
		checklistTemplates = self.env['hr.checklist_template'].search([])
		employeeChecklist = self.env['hr.employee.checklist.documents.list.main'].search([])
		#Write Now for the Sake of Demo 
		#This must be hardcoded
		
		#FOR US VISA
		if len(pObjRecord) == 0:
			record_id = self.id
			employee_id = self.employee_id.id
		else:
			record_id = pObjRecord.id
			employee_id = pObjRecord.employee_id.id

		vals = {'employee_checklist_document': record_id}

		checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_US_VISA_MAIN_CONSTANT')])
		temp_1 = checklistTemplates.id
		vals.update({
					'param_name_1': temp_1,
					'param_name_1_value': '',
					'param_name_1_check': False,
					'param_name_1_value_visible':  True,
					'param_name_1_check_visible':  True,
					})

		checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_CONTRACT_SIGNED_CONSTANT')])
		temp_1 = checklistTemplates.id
		vals.update({
					'param_name_2': temp_1,
					'param_name_2_value': '',
					'param_name_2_check': False,
					'param_name_2_value_visible':  True,
					'param_name_2_check_visible':  False,
					})

		rec = employeeChecklist.create(vals)
		rec.getEmployeeDocuments_Temporary(rec)

		#FOR VISA 2
		vals = {'employee_checklist_document': record_id}
		checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_VISA_II_CONSTANT')])
		temp_1 = checklistTemplates.id
		vals.update({
					'param_name_1': temp_1,
					'param_name_1_value': '',
					'param_name_1_check': False,
					'param_name_1_value_visible':  True,
					'param_name_1_check_visible':  True,
					})   


		checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_APPRAISAL_CONSTANT')])
		temp_1 = checklistTemplates.id
		vals.update({
					'param_name_2': temp_1,
					'param_name_2_value': '',
					'param_name_2_check': False,
					'param_name_2_value_visible':  True,
					'param_name_2_check_visible':  False,
					})

		employeeChecklist.create(vals)	 

		#FOR PEME
		vals = {'employee_checklist_document': record_id}

		checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_PEME_CONSTANT')])
		temp_1 = checklistTemplates.id
		vals.update({
					'param_name_1': temp_1,
					'param_name_1_value': '',
					'param_name_1_check': False,
					'param_name_1_value_visible':  True,
					'param_name_1_check_visible':  True,
					})

		checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_JOB_DESCRIPTION_CONSTANT')])
		temp_1 = checklistTemplates.id
		vals.update({
					'param_name_2': temp_1,
					'param_name_2_value': '',
					'param_name_2_check': False,
					'param_name_2_value_visible':  True,
					'param_name_2_check_visible':  False,
					})


		employeeChecklist.create(vals)   
		# FOR OWWA
		vals = {'employee_checklist_document': record_id}

		checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_OWWA_RECEIPT_CONSTANT')])
		temp_1 = checklistTemplates.id
		vals.update({
					'param_name_1': temp_1,
					'param_name_1_value': '',
					'param_name_1_check': False,
					'param_name_1_value_visible':  False,
					'param_name_1_check_visible':  True,
					})  

		checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_COMPA_LEAVE_CONT_CONSTANT')])
		temp_1 = checklistTemplates.id
		vals.update({
					'param_name_2': temp_1,
					'param_name_2_value': '',
					'param_name_2_check': False,
					'param_name_2_value_visible':  True,
					'param_name_2_check_visible':  False,
					})
							
		employeeChecklist.create(vals)   
		# FOR PAGIBIG
		vals = {'employee_checklist_document': record_id}

		checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_PAGIBIG_CONSTANT')])
		temp_1 = checklistTemplates.id
		vals.update({
					'param_name_1': temp_1,
					'param_name_1_value': '',
					'param_name_1_check': False,
					'param_name_1_value_visible':  False,
					'param_name_1_check_visible':  True,
					})  
		employeeChecklist.create(vals)   
		# FOR PHILHEALTH
		vals = {'employee_checklist_document': record_id}

		checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_PHILHEALTH_CONSTANT')])
		temp_1 = checklistTemplates.id
		vals.update({
					'param_name_1': temp_1,
					'param_name_1_value': '',
					'param_name_1_check': False,
					'param_name_1_value_visible':  False,
					'param_name_1_check_visible':  True,
					})  
		employeeChecklist.create(vals)

		# FOR SSS
		vals = {'employee_checklist_document': record_id}

		checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_SSS_CONSTANT')])
		temp_1 = checklistTemplates.id
		vals.update({
					'param_name_1': temp_1,
					'param_name_1_value': '',
					'param_name_1_check': False,
					'param_name_1_value_visible':  False,
					'param_name_1_check_visible':  True,
					})		  
		employeeChecklist.create(vals) 

	# Overrides
	@api.model
	def create(self, vals):
		readony_fields = self.readonly_values_2(vals)
		for readonly_field in readony_fields:
			vals.update({readonly_field: readony_fields[readonly_field]})
		new_record = super(EmployeeChecklist, self).create(vals)

		if not new_record.employee_checklists_documents_list:
			self.createChecklistDocumentList(new_record)
		if not new_record.employee_checklists_documents_list_main:
			self.createChecklistDocumentList_main(new_record)
		return new_record

	def write(self, vals):
		server_date = DATE_NOW.strftime("%d/%m/%Y")
		super(EmployeeChecklist, self).write(vals)
		if vals.has_key('employee_checklists_documents_list'):
			checklist_documents = vals['employee_checklists_documents_list']
			for checklist_document in checklist_documents:
				#To Check if Row is being Updated
				#if Updated Add the Value in Change by and Date Updated
				if checklist_document[2]:
					model_list_document_main =self.env['hr.employee.checklist.documents.list'].search([('employee_checklist_document', '=', self.id),('id','=', checklist_document[1])])
					model_list_document_main.write({
					'change_by': self.getUseridName(),
					'change_date': server_date})
		return True

class EmployeeChecklist_list(models.Model):
	_name = "hr.employee.checklist.documents.list"
	_description = 'Employee Checklist Documents List'

	checklist_template_id = fields.Many2one('hr.checklist_template')
	employee_checklist_document = fields.Many2one('hr.employee.checklist.documents') 
	param_name_1 = fields.Many2one('hr.checklist', 'Parameter 1')
	param_name_2 = fields.Many2one('hr.checklist', 'Parameter 2')
	param_name_3 = fields.Many2one('hr.checklist', 'Parameter 3')
	param_name_4 = fields.Many2one('hr.checklist', 'Parameter 4')

	param_name_1_value = fields.Char("Parameter 1 value")
	param_name_2_value = fields.Char("Parameter 2 value")
	param_name_3_value = fields.Char("Parameter 3 value")
	param_name_4_value = fields.Char("Parameter 4 value")

	param_name_1_check = fields.Boolean("Parameter 1 Checked?")
	param_name_2_check = fields.Boolean("Parameter 2 Checked?")
	param_name_3_check = fields.Boolean("Parameter 3 Checked?")
	param_name_4_check = fields.Boolean("Parameter 4 Checked?")

	param_name_1_value_visible = fields.Boolean("Parameter 1 Value visible?")
	param_name_2_value_visible = fields.Boolean("Parameter 2 Value visible?")
	param_name_3_value_visible = fields.Boolean("Parameter 3 Value visible?")
	param_name_4_value_visible = fields.Boolean("Parameter 4 Value visible?")


	param_name_1_check_visible = fields.Boolean("Parameter 1 Check visible?")
	param_name_2_check_visible = fields.Boolean("Parameter 2 Check visible?")
	param_name_3_check_visible = fields.Boolean("Parameter 3 Check visible?")
	param_name_4_check_visible = fields.Boolean("Parameter 4 Check visible?")

	has_date_issued = fields.Boolean("Date Issued Enable?")
	has_issued_at = fields.Boolean("Issued At Enable?")
	has_date_expiry = fields.Boolean("Date Expiry Enable?")
	has_changed_by = fields.Boolean("Change by Enable")
	has_change_date = fields.Boolean("Date Change Enable?")

	issued_at = fields.Char("Issued at")
	date_issued = fields.Date("Date issued")
	date_expiry = fields.Date("Date Expiry")
	change_by = fields.Char("Change By")
	change_date = fields.Char("Change Date")

	param_name_1_related = fields.Many2one('hr.checklist', related='checklist_template_id.checklist_temp_param_1', string='Parameter 1')
	param_name_2_related = fields.Many2one('hr.checklist', related='checklist_template_id.checklist_temp_param_2', string='Parameter 2')
	param_name_3_related = fields.Many2one('hr.checklist', related='checklist_template_id.checklist_temp_param_3', string='Parameter 3')
	param_name_4_related = fields.Many2one('hr.checklist', related='checklist_template_id.checklist_temp_param_4', string='Parameter 4')

	@api.model
	def getEmployeeMedicalRecord(self, pchecklist, pfield_name, pemployee_id):
		model_employee_medical = self.env['hr.employee_medical_records'].search([('employee_med_rec_id', '=', pemployee_id)])
		model_employee_medical_ret =  model_employee_medical.search([('medical_type', '=',pchecklist.param_name_1.link_medical_type.id)])
		if pfield_name == 'param_name_1':
			parameter_field = pchecklist.param_name_1
			str_parameter_value = 'param_name_1_value'
			str_parameter_check = 'param_name_1_check'
		elif pfield_name == 'param_name_2':
			parameter_field = pchecklist.param_name_2
			str_parameter_value = 'param_name_2_value'
			str_parameter_check = 'param_name_2_check'
		elif pfield_name == 'param_name_3':
			parameter_field = pchecklist.param_name_3
			str_parameter_value = 'param_name_3_value'
			str_parameter_check = 'param_name_3_check'

		write_values = {}
		if not isinstance(parameter_field, bool):
			if len(parameter_field) > 0:
				#Get Document Properties
				if parameter_field.link_selection == 'medical':
					model_employee_medical_ret =  model_employee_medical.search([('medical_type', '=',pchecklist.param_name_1.link_medical_type.id),('employee_med_rec_id', '=', pemployee_id)])
					if parameter_field.retrieve_history_records == 'latest_doc':
						for license  in model_employee_medical_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
							write_values.update({str_parameter_check: 1})
							break
					elif parameter_field.retrieve_history_records == 'oldest_doc':
						int_counter_record = 0
						if len(model_employee_medical_ret) > 1:
							for license  in model_employee_medical_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
								if int_counter_record >= 1:
									write_values.update({str_parameter_check: 1})
									break
								int_counter_record +=1  
		return write_values  

	@api.model
	def getEmployeeLicenses(self, pchecklist, pfield_name, pemployee_id):
		model_employee_license = self.env['hr.employeelicenses'].search([('employee_licenses_id', '=', pemployee_id)])
		model_employee_license_ret =  model_employee_license.search([('license', '=',pchecklist.param_name_1.link_license_type.id)])
		if pfield_name == 'param_name_1':
			parameter_field = pchecklist.param_name_1
			str_parameter_value = 'param_name_1_value'
			str_parameter_check = 'param_name_1_check'
		elif pfield_name == 'param_name_2':
			parameter_field = pchecklist.param_name_2
			str_parameter_value = 'param_name_2_value'
			str_parameter_check = 'param_name_2_check'
		elif pfield_name == 'param_name_3':
			parameter_field = pchecklist.param_name_3
			str_parameter_value = 'param_name_3_value'
			str_parameter_check = 'param_name_3_check'

		write_values = {}
		if not isinstance(parameter_field, bool):
			if len(parameter_field) > 0:
				#Get Document Properties
				if parameter_field.link_selection == 'license':
					model_employee_license_ret =  model_employee_license.search([('license', '=',parameter_field.link_license_type.id),('employee_licenses_id', '=', pemployee_id)])
					if parameter_field.retrieve_history_records == 'latest_doc':
						for license  in model_employee_license_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
							write_values.update({str_parameter_value: license.doc_number,str_parameter_check: 1})
							break
					elif parameter_field.retrieve_history_records == 'oldest_doc':
						int_counter_record = 0
						if len(model_employee_license_ret) > 1:
							for license  in model_employee_license_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
								if int_counter_record >= 1:
									write_values.update({str_parameter_value: license.doc_number,str_parameter_check: 1})
									break
								int_counter_record +=1  
		return write_values

	@api.model
	def getEmployeeDocuments(self, pchecklist, pfield_name, pemployee_id):
		model_employee_document = self.env['hr.employee_documents'].search([('employee_doc_id', '=', pemployee_id)])
		model_employee_document_ret =  model_employee_document.search([('document', '=',pchecklist.param_name_1.link_document_type.id)])

		if pfield_name == 'param_name_1':
			parameter_field = pchecklist.param_name_1
			str_parameter_value = 'param_name_1_value'
			str_parameter_check = 'param_name_1_check'
		elif pfield_name == 'param_name_2':
			parameter_field = pchecklist.param_name_2
			str_parameter_value = 'param_name_2_value'
			str_parameter_check = 'param_name_2_check'
		elif pfield_name == 'param_name_3':
			parameter_field = pchecklist.param_name_3
			str_parameter_value = 'param_name_3_value'
			str_parameter_check = 'param_name_3_check'  

		write_values = {}
		if not isinstance(parameter_field, bool):
			if len(parameter_field) > 0:
				#Get Document Properties
				if parameter_field.link_selection == 'document':
					model_employee_document_ret =  model_employee_document.search([('employee_doc_id', '=', pemployee_id),('document', '=',parameter_field.link_document_type.id)])
					if parameter_field.retrieve_history_records == 'latest_doc':
						for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
							write_values.update({str_parameter_value: document.document_number,str_parameter_check: 1,})

							if pchecklist.checklist_template_id.checklist_temp_row_with_dateissued:
								write_values.update({'issued_at': document.place_ofissue,'date_issued': document.date_issued})
							if pchecklist.checklist_template_id.checklist_temp_param_1_with_dateexpired:
								write_values.update({'date_expiry': document.date_expiry})
							break
					elif parameter_field.retrieve_history_records == 'oldest_doc':
						int_counter_record = 0
						if len(model_employee_document_ret) > 1:
							for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
								if int_counter_record >= 1:
									write_values.update({str_parameter_value: document.document_number,str_parameter_check: 1,'param_name_2_value':document.date_expiry})
									break
								int_counter_record +=1
		return write_values

	@api.model
	def getDataFromDocuments(self, pchecklist_document_id, employee_id):
		model_checklist_document_list = self.env[self._name].search([('employee_checklist_document', '=', pchecklist_document_id)])

		if len(model_checklist_document_list) > 0:
			server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
			for checklist in model_checklist_document_list:
				write_values = {}
				write_values_final = {} 
				write_values = self.getEmployeeDocuments(checklist, 'param_name_1',employee_id)
				write_values_final.update(write_values)
				write_values = self.getEmployeeDocuments(checklist, 'param_name_2',employee_id)
				write_values_final.update(write_values) 
				write_values = self.getEmployeeDocuments(checklist, 'param_name_3',employee_id)
				write_values_final.update(write_values)

				write_values = self.getEmployeeLicenses(checklist, 'param_name_1',employee_id)
				write_values_final.update(write_values)
				write_values = self.getEmployeeLicenses(checklist, 'param_name_2',employee_id)
				write_values_final.update(write_values)
				write_values = self.getEmployeeLicenses(checklist, 'param_name_3',employee_id)
				write_values_final.update(write_values)

				write_values = self.getEmployeeMedicalRecord(checklist, 'param_name_1',employee_id)
				write_values_final.update(write_values)
				write_values = self.getEmployeeMedicalRecord(checklist, 'param_name_2',employee_id)
				write_values_final.update(write_values)
				write_values = self.getEmployeeMedicalRecord(checklist, 'param_name_3',employee_id)
				write_values_final.update(write_values) 
				checklist.write(write_values_final) 

class EmployeeChecklist_list(models.Model):
	_name = "hr.employee.checklist.documents.list.main"
	_description = 'Employee Checklist Documents List Main'

	checklist_template_id = fields.Many2one('hr.checklist_template')
	employee_checklist_document = fields.Many2one('hr.employee.checklist.documents')  


	param_name_1 = fields.Many2one('hr.checklist', 'Parameter 1')
	param_name_2 = fields.Many2one('hr.checklist', 'Parameter 2')
	param_name_3 = fields.Many2one('hr.checklist', 'Parameter 3')
	param_name_4 = fields.Many2one('hr.checklist', 'Parameter 4')

	param_name_1_value = fields.Char("Parameter 1 value")
	param_name_2_value = fields.Char("Parameter 2 value")
	param_name_3_value = fields.Char("Parameter 3 value")
	param_name_4_value = fields.Char("Parameter 4 value")

	param_name_1_check = fields.Boolean("Parameter 1 Checked?")
	param_name_2_check = fields.Boolean("Parameter 2 Checked?")
	param_name_3_check = fields.Boolean("Parameter 3 Checked?")
	param_name_4_check = fields.Boolean("Parameter 4 Checked?")

	param_name_1_value_visible = fields.Boolean("Parameter 1 Value visible?")
	param_name_2_value_visible = fields.Boolean("Parameter 2 Value visible?")
	param_name_3_value_visible = fields.Boolean("Parameter 3 Value visible?")
	param_name_4_value_visible = fields.Boolean("Parameter 4 Value visible?")


	param_name_1_check_visible = fields.Boolean("Parameter 1 Check visible?")
	param_name_2_check_visible = fields.Boolean("Parameter 2 Check visible?")
	param_name_3_check_visible = fields.Boolean("Parameter 3 Check visible?")
	param_name_4_check_visible = fields.Boolean("Parameter 4 Check visible?")

	has_date_issued = fields.Boolean("Date Issued Enable?")
	has_issued_at = fields.Boolean("Issued At Enable?")
	has_date_expiry = fields.Boolean("Date Expiry Enable?")  
	has_changed_by = fields.Boolean("Change by Enable")  
	has_change_date = fields.Boolean("Date Change Enable?")  

	issued_at = fields.Char("Issued at")
	date_issued = fields.Date("Date issued")
	date_expiry = fields.Date("Date Expiry")
	change_by = fields.Char("Change By")
	change_date = fields.Char("Change Date")

	@api.model
	def getEmployeeDocuments_Temporary(self,pemployee_id):
		model_employee_document = self.env['hr.employee_documents'].search([('employee_doc_id', '=', pemployee_id.employee_checklist_document.employee_id.id)])
		if len(pemployee_id) > 0:
			#Get Document Properties
			model_employee_document_ret =  model_employee_document.search([('document', '=',pemployee_id.param_name_1.link_document_type.id),('employee_doc_id', '=', pemployee_id.employee_checklist_document.employee_id.id)])
			if pemployee_id.param_name_1.retrieve_history_records == 'latest_doc':
				for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
					pemployee_id.param_name_1_value = document.document_number
					pemployee_id.param_name_1_check = 1
					#pemployee_id.write()
					break

			model_employee_document_ret =  model_employee_document.search([('document', '=',pemployee_id.param_name_2.link_document_type.id),('employee_doc_id', '=', pemployee_id.employee_checklist_document.employee_id.id)])

			if pemployee_id.param_name_2.retrieve_history_records == 'oldest_doc':
				int_counter_record = 0
				if len(model_employee_document_ret) > 1:
					for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
						if int_counter_record >= 1:
							pemployee_id.param_name_2_value = document.document_number
							pemployee_id.param_name_2_check = 1
							#pemployee_id.write()
							break
						int_counter_record +=1

			model_employee_document_ret =  model_employee_document.search([('document', '=',pemployee_id.param_name_3.link_document_type.id),('employee_doc_id', '=', pemployee_id.employee_checklist_document.employee_id.id)])
			if pemployee_id.param_name_3.retrieve_history_records == 'latest_doc':
				for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
					pemployee_id.param_name_3_value = document.place_ofissue
					pemployee_id.param_name_3_check = 1
					break

			if pemployee_id.param_name_2.checklist_code  == 'CODE_US_VISA_EXPIRY_DATE_CONSTANT':
				date_exp = ''
				model_employee_document_ret =  model_employee_document.search([('document', '=',pemployee_id.param_name_2.link_document_type.id),('employee_doc_id', '=', pemployee_id.employee_checklist_document.employee_id.id)])
				if pemployee_id.param_name_2.retrieve_history_records == 'latest_doc':
					for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
						if not isinstance(pemployee_id.date_expiry, bool):
							date_exp = datetime.datetime.strptime(pemployee_id.date_expiry ,"%Y-%m-%d")
							pemployee_id.param_name_2_value = date_exp.strptime('%m/%d/%y')
							pemployee_id.param_name_2_check = 1
						break

	@api.model
	def getEmployeeMedicalRecord(self, pchecklist, pfield_name, pemployee_id):
		model_employee_medical = self.env['hr.employee_medical_records'].search([('employee_med_rec_id', '=', pemployee_id)])
		model_employee_medical_ret =  model_employee_medical.search([('medical_type', '=',pchecklist.param_name_1.link_medical_type.id)])
		if pfield_name == 'param_name_1':
			parameter_field = pchecklist.param_name_1
			str_parameter_value = 'param_name_1_value'
			str_parameter_check = 'param_name_1_check'
		elif pfield_name == 'param_name_2':
			parameter_field = pchecklist.param_name_2
			str_parameter_value = 'param_name_2_value'
			str_parameter_check = 'param_name_2_check'
		elif pfield_name == 'param_name_3':
			parameter_field = pchecklist.param_name_3
			str_parameter_value = 'param_name_3_value'
			str_parameter_check = 'param_name_3_check'

		write_values = {}
		if not isinstance(parameter_field, bool):
			if len(parameter_field) > 0:
				#Get Document Properties
				if parameter_field.link_selection == 'medical':
					if parameter_field.retrieve_history_records == 'latest_doc':
						for license  in model_employee_medical_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
							write_values.update({str_parameter_check: 1})
							break
					elif parameter_field.retrieve_history_records == 'oldest_doc':
						int_counter_record = 0
						if len(model_employee_medical_ret) > 1:
							for license  in model_employee_medical_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
								if int_counter_record >= 1:
									write_values.update({str_parameter_check: 1})
									break 
								int_counter_record +=1
		return write_values

	@api.model
	def getEmployeeLicenses(self, pchecklist, pfield_name, pemployee_id):
		model_employee_license = self.env['hr.employeelicenses'].search([('employee_licenses_id', '=', pemployee_id)])
		model_employee_license_ret =  model_employee_license.search([('license', '=',pchecklist.param_name_1.link_license_type.id)])
		if pfield_name == 'param_name_1':
			parameter_field = pchecklist.param_name_1
			str_parameter_value = 'param_name_1_value'
			str_parameter_check = 'param_name_1_check'
		elif pfield_name == 'param_name_2':
			parameter_field = pchecklist.param_name_2
			str_parameter_value = 'param_name_2_value'
			str_parameter_check = 'param_name_2_check'
		elif pfield_name == 'param_name_3':
			parameter_field = pchecklist.param_name_3
			str_parameter_value = 'param_name_3_value'
			str_parameter_check = 'param_name_3_check'
		write_values = {}
		if not isinstance(parameter_field, bool):
			if len(parameter_field) > 0:
				#Get Document Properties
				if parameter_field.link_selection == 'license':
					if parameter_field.retrieve_history_records == 'latest_doc':
						for license  in model_employee_license_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
							write_values.update({str_parameter_value: license.doc_number,str_parameter_check: 1})
							break
					elif parameter_field.retrieve_history_records == 'oldest_doc':
						int_counter_record = 0
						if len(model_employee_license_ret) > 1:
							for license  in model_employee_license_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
								if int_counter_record >= 1:
									write_values.update({str_parameter_value: license.doc_number,str_parameter_check: 1})
									break 
								int_counter_record +=1
		return write_values

	@api.model
	def getEmployeeDocuments(self, pchecklist, pfield_name, pemployee_id):
		model_employee_document = self.env['hr.employee_documents'].search([('employee_doc_id', '=', pemployee_id)])
		model_employee_document_ret =  model_employee_document.search([('document', '=',pchecklist.param_name_1.link_document_type.id)])

		if pfield_name == 'param_name_1':
			parameter_field = pchecklist.param_name_1
			str_parameter_value = 'param_name_1_value'
			str_parameter_check = 'param_name_1_check'
		elif pfield_name == 'param_name_2':
			parameter_field = pchecklist.param_name_2
			str_parameter_value = 'param_name_2_value'
			str_parameter_check = 'param_name_2_check'
		elif pfield_name == 'param_name_3':
			parameter_field = pchecklist.param_name_3
			str_parameter_value = 'param_name_3_value'
			str_parameter_check = 'param_name_3_check'  

		write_values = {}
		if not isinstance(parameter_field, bool):
			if len(parameter_field) > 0:
				#Get Document Properties
				if parameter_field.link_selection == 'document':
					model_employee_document_ret =  model_employee_document.search([('document', '=',parameter_field.link_document_type.id)])
					if parameter_field.retrieve_history_records == 'latest_doc':
						for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
							write_values.update({str_parameter_value: document.document_number,str_parameter_check: 1})
							break
					elif parameter_field.retrieve_history_records == 'oldest_doc':
						int_counter_record = 0
						if len(model_employee_document_ret) > 1:
							for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
								if int_counter_record >= 1:
									write_values.update({str_parameter_value: document.document_number,str_parameter_check: 1})
									break 
								int_counter_record +=1
		return write_values

	@api.model
	def getDataFromDocuments(self, pchecklist_document_id, employee_id):
		model_checklist_document_list = self.env[self._name].search([('employee_checklist_document', '=', pchecklist_document_id)])  
		if len(model_checklist_document_list) > 0:
			server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
			for checklist in model_checklist_document_list:
				write_values = {}
				write_values_final = {} 
				write_values = self.getEmployeeDocuments(checklist, 'param_name_1',employee_id)
				write_values_final.update(write_values)
				write_values = self.getEmployeeDocuments(checklist, 'param_name_2',employee_id)
				write_values_final.update(write_values) 
				write_values = self.getEmployeeDocuments(checklist, 'param_name_3',employee_id)
				write_values_final.update(write_values)

				write_values = self.getEmployeeLicenses(checklist, 'param_name_1',employee_id)
				write_values_final.update(write_values)
				write_values = self.getEmployeeLicenses(checklist, 'param_name_2',employee_id)
				write_values_final.update(write_values)
				write_values = self.getEmployeeLicenses(checklist, 'param_name_3',employee_id)
				write_values_final.update(write_values)

				write_values = self.getEmployeeMedicalRecord(checklist, 'param_name_1',employee_id)
				write_values_final.update(write_values)
				write_values = self.getEmployeeMedicalRecord(checklist, 'param_name_2',employee_id)
				write_values_final.update(write_values)
				write_values = self.getEmployeeMedicalRecord(checklist, 'param_name_3',employee_id)
				write_values_final.update(write_values) 
				checklist.write(write_values_final) 


#Models
class AddressType(models.Model):
	_name = 'hr.addresstype'
	_description = 'Address Type'

	name = fields.Char('Address Type', required = True)
	description = fields.Text('Description')

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_addresstype_name',
		'UNIQUE (name)',
		'Address Type must be unique!')]

class EducationType(models.Model):
	_name = 'hr.educationtype'
	_description = 'Education Type'

	name = fields.Char('Education')
	description = fields.Text('Description')

class DocumentType(models.Model):
	_name = 'hr.documenttype'
	_description = 'Document Type'

	abbreviation = fields.Char('Code', required =True)
	name = fields.Char('Document name', required=True)
	check_for_expiration = fields.Boolean('Check Expiration', default= False)
	description = fields.Text('Full Description')
	ref_rec_id = fields.Char(string='Reference ID')

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_documenttype_name',
		'UNIQUE (abbreviation)',
		'Code must be unique!')]

class FamilyRelations(models.Model):
	_name = 'hr.familyrelations'
	_description = 'Family Relations'

	code = fields.Char('Code', required =True)
	name = fields.Char('Relationship', required=True)
	description = fields.Text('Description')

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_familyrelations_name',
		'UNIQUE (code,name)',
		'Family relation must be unique!')]

class MedicalRecordType(models.Model):
	_name = 'hr.medicalrecord'
	_description = 'Medical Record Type'

	code = fields.Char('Code', required =True)
	name = fields.Char('Medical', required =True)
	description = fields.Text('Description')
	ref_rec_id = fields.Char(string='Reference ID')

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_medicalrecord_name',
		'UNIQUE (code,name)',
		'Medical record type must be unique!')]

class LicenseType(models.Model):
	_name ='hr.licensetype'
	_description = 'License Type'

	@api.model
	def _getClassID(self):
		obj_sequence = self.env['ir.sequence']
		return obj_sequence.next_by_code('hr.licensetype.sequence')

	id_name = fields.Char('Class ID', default=_getClassID)
	name = fields.Char('Class Name', required =True)
	# active = fields.Boolean(default=True)

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_medicalrecord_name_uniq',
		'UNIQUE (id_name)',
		'License type must be unique')]

class License(models.Model):
	_name = 'hr.license'
	_description = 'Licenses'

	id_class_name = fields.Integer('Class ID')
	license_name = fields.Many2one('hr.licensetype','Class Name', required=True)
	name = fields.Char('Doc Abbreviation', required=True)
	doc_description = fields.Text('Doc Full Description')

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_license_name_uniq',
		'UNIQUE (id_class_name,name)',
		'License must be unique')]

class MedicalClinic(models.Model):
	_name = 'hr.clinic'
	_description = 'Medical Clinic'
	_inherit = 'hr.documenttype'

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_clinic_name_uniq',
		'UNIQUE (abbreviation,name)',
		'Clinic name must be unique!')]

class LengthOfExpiration(models.Model):
	_name = 'hr.lengthofexpiration'
	_description = 'Length Of Expiration'
	_inherit = 'hr.familyrelations'

	days = fields.Integer('Days before Expiration')

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_lengthofexp_name_uniq',
		'UNIQUE (abbreviation,name)',
		'Length of expiration must be unique!')]

class PortInformation(models.Model):
	_name = 'hr.port'
	_description = 'Port'
	_inherit = 'hr.abs.parameter'

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_port_name_uniq',
		'UNIQUE (code, name)',
		'Port must be unique!')]

class Companies(models.Model):
	_name = 'hr.companies'
	_description = 'Companies'
	_inherit = 'hr.abs.parameter'

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_company_name_uniq',
		'UNIQUE (code, name)',
		'Port must be unique!')]

class VesselCategory(models.Model):
	_name = 'hr.vesselcategory'
	_description = 'Vessel Category'

	category = fields.Char('Category', required=True)
	name = fields.Char('Name', required=True)
	vessel_cat_ids = fields.Many2many('hr.ship.department','department_vessel_rel', 'vessel_cat_id','department_id', 'Vessel Category')

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_vesselcat_name_uniq',
		'UNIQUE (category,name)',
		'Vessel category must be unique!')]

class Vessel(models.Model):
	_name = 'hr.vessel'
	_description = 'Vessel'
	_inherit ='hr.abs.parameter'

	company_code = fields.Many2one('hr.companies', 'Company', required =True)
	vessel_category = fields.Many2one('hr.vesselcategory','Category', required =True)

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_vessel_name_uniq',
		'UNIQUE (code,name,vessel_category,company_code)',
		'Vessel must be unique!')]

class RankType(models.Model):
	_name = 'hr.ranktype'
	_description = 'Rank Type'
	_inherit = 'hr.abs.parameter'

	rate = fields.Float('Incentive Rate',digits=(18,2))

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_ranktype_name_uniq',
		'UNIQUE (code,name)',
		'Rank type must be unique!')]

class Rank(models.Model):
	_name = 'hr.rank'
	_description = 'Rank'

	rank_identification = fields.Char('Rank ID')
	rank = fields.Char('Rank')
	name= fields.Char('Name')
	rank_type = fields.Many2one('hr.ranktype', 'Rank Type')
	rank_department_ids = fields.Many2many('hr.ship.department', 'rank_department_table','rank_department_id','department_id','Departments')

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_rank_name_uniq',
		'UNIQUE (rank_identification,name,rank_type)',
		'Rank must be unique!')]

class ShipDepartment(models.Model):
	_name = 'hr.ship.department'
	_description = 'Ship Department'

	ship_dept_code = fields.Char('Code', required=True)
	name = fields.Char('Name')
	department = fields.Char('Department', required=True)
	department_ids = fields.Many2many('hr.vesselcategory','department_vessel_rel', 'department_id','vessel_cat_id', 'Vessel Category')

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_shipdep_name_uniq',
		'UNIQUE (ship_dept_code,name,department_ids)',
		'Ship Department must be unique!')]

	@api.onchange('department', 'ship_dept_code')
	def onchangeName(self):
		for rec in self:
			if not isinstance( self.ship_dept_code, bool) and not isinstance( self.department, bool):
				self.name = "[" + self.ship_dept_code + "]" + " " + self.department

	# Overrides
	@api.model
	def create(self, vals):
		if vals.has_key('name'):
			vals['name'] =  "[" + vals['ship_dept_code'] + "]" + " " + vals['department']
		else: 
			vals.update({'name': "[" + vals['ship_dept_code'] + "]" + " " + vals['department']})                   
		new_record = super(ShipDepartment, self).create(vals)
		return new_record  


	def write(self, vals):
		for rec in self:
			name_value = ''
			if not vals.has_key('name'):
				if vals.has_key('ship_dept_code'):
					name_value = "[" + vals['ship_dept_code']  + "]" + " "
				else:
					name_value = "[" + self.ship_dept_code  + "]" + " "
				if vals.has_key('department'):
					name_value += vals['department']
				else:
					name_value += self.department
				vals.update({'name': name_value})   

		super(ShipDepartment, self).write(vals)        
		return True        

class Status(models.Model):
	_name = 'hr.employment.status'
	_description = 'Employment Status'

	status_id = fields.Char('Status ID')
	name = fields.Text('Description', required=True)

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_empstat_name_uniq',
		'UNIQUE (status_id,name)',
		'Rank must be unique!')]

class CheckList(models.Model):
	_name= 'hr.checklist'
	_description = 'Checklist'

	checklist_code = fields.Char('Code', required=True)
	name = fields.Char('Name', required=True)
	link_selection = fields.Selection(CHECKLIST_DOCUMENT_TYPE, 'Document Link', default ='none')
	link_document_type = fields.Many2one('hr.documenttype', 'Document Type')
	link_license_type = fields.Many2one('hr.license', 'License Type')
	link_medical_type = fields.Many2one('hr.medicalrecord', 'Medical Type')
	retrieve_history_records = fields.Selection(RETRIEVE_RECORD_IN_HISTORY, 'Retrieving of Records', default ='latest_doc')

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_chekclist_name_uniq',
		'UNIQUE (checklist_code,name)',
		'Checklist must be unique!')]


	@api.onchange('link_selection')
	def onchange_selection(self):
		for rec in self:
			rec.link_document_type = None
			rec.link_license_type = None    
			rec.link_medical_type = None  
			rec.retrieve_history_records  = 'latest_doc'


class religion(models.Model):
	_name= 'hr.religion'
	_description = 'Religion'

	religion_code = fields.Char('Code', required=True)
	name = fields.Char('Name', required=True)

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_religion_code_uniq',
		'UNIQUE (religion_code)',
		'Checklist must be unique!')]


class CheckListTemplate(models.Model):
	_name='hr.checklist_template.main'
	_description = 'Checklist Template Main'

	name = fields.Char('Checklist Name')
	#department_id = fields.Many2one('hr.ship.department', 'Ship Department')
	department_ids = fields.Many2many('hr.ship.department','checklist_department_rel','checklist_main_id','department_id', 'Ship Department')
	allow_to_fill_by_dep = fields.Boolean('Auto Fill Employee Checklist by Department?')
	checklist_template_ids = fields.One2many('hr.checklist_template','checklist_template_main_id', string='Checklist Template Details')

class ChecklistTemplate(models.Model):
	_name = 'hr.checklist_template'
	_description = 'Checklist Template'
	_order =  'csequence'

	checklist_temp_code = fields.Char('Code')
	name = fields.Char('Name')
	checklist_temp_param_1 = fields.Many2one('hr.checklist', 'Parameter 1')
	checklist_temp_param_1_with_value = fields.Boolean('With Value')
	checklist_temp_param_1_data_type = fields.Selection(DATA_TYPE, 'Data Type')
	checklist_temp_param_1_colspan = fields.Integer('Column Span')
	checklist_temp_param_1_check_value = fields.Boolean('Allow Check', default = True)



	checklist_temp_param_2 = fields.Many2one('hr.checklist', 'Parameter 2')
	checklist_temp_param_2_with_value = fields.Boolean('With Value')
	checklist_temp_param_2_data_type = fields.Selection(DATA_TYPE, 'Data Type')
	checklist_temp_param_2_colspan = fields.Integer('Column Span')
	checklist_temp_param_2_check_value = fields.Boolean('Allow Check', default = True)


	checklist_temp_param_3 = fields.Many2one('hr.checklist', 'Parameter 3')
	checklist_temp_param_3_with_value = fields.Boolean('With Value')
	checklist_temp_param_3_data_type = fields.Selection(DATA_TYPE, 'Data Type')
	checklist_temp_param_3_colspan = fields.Integer('Column Span')
	checklist_temp_param_3_check_value = fields.Boolean('Allow Check', default = True)

	checklist_temp_param_4 = fields.Many2one('hr.checklist', 'Parameter 4')
	checklist_temp_param_4_with_value = fields.Boolean('With Value')
	checklist_temp_param_4_data_type = fields.Selection(DATA_TYPE, 'Data Type')
	checklist_temp_param_4_colspan = fields.Integer('Column Span')
	checklist_temp_param_4_check_value = fields.Boolean('Allow Check', default = True)

	checklist_temp_row_with_dateissued = fields.Boolean('With Value', default = True)
	checklist_temp_param_1_with_dateexpired = fields.Boolean('With Value', default = True)
	checklist_temp_param_1_with_changeby = fields.Boolean('With Value', default = True)
	checklist_temp_param_1_with_changedate = fields.Boolean('With Value', default = True)
	csequence = fields.Integer("Sequence", default = 0)


	checklist_template_main_id = fields.Many2one('hr.checklist_template.main', 'Checklist Template Details')
	blank_row = fields.Boolean('Blank Row')

	@api.model
	def create(self, vals):
		if vals['csequence'] == False:
			raise Warning('No Checklist template sequence define.')

		if vals['name'] == False:
			raise Warning('No Checklist template name define.')
		new_record = super(ChecklistTemplate, self).create(vals)

		return new_record

	# [TMP] - Disable for data mig
	_sql_constraints = [
		('hr_chekclist_name_uniq',
		'UNIQUE (name,name)',
		'Template name must be unique!')]
