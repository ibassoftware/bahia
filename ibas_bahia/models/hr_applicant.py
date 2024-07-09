# -*- encoding: utf-8 -*-
from odoo import models, fields, api
#from openerp.osv import fields, osv
from odoo.tools.translate import _

from odoo import SUPERUSER_ID
from odoo import tools
from odoo.modules.module import get_module_resource

from odoo.exceptions import UserError, ValidationError

class hrApplicant(models.Model):
	_name = "hr.applicant"
	_description = 'HR Applicant'
	_inherit = 	['hr.applicant', 'avatar.mixin']

	@api.model
	def _getEmpId(self):
		obj_sequence = self.env['ir.sequence'].search([('code','=', 'hr.applicant.sequence')])
		return str(obj_sequence.number_next_actual).zfill(obj_sequence.padding)

	application_number = fields.Char('Application Number', default = _getEmpId, readonly=True)
	first_name = fields.Char('First name')
	last_name = fields.Char('Last name')
	middle_name = fields.Char('Middle name')

	image= fields.Binary('Applicant Image')




	weight = fields.Char('Weight')
	height = fields.Char('Height')
	placeof_birth = fields.Char('Place of birth')
	date_of_birth = fields.Date('Date of birth')
	shoe_size = fields.Char('Shoe Size')
	sss_no = fields.Char('SSS No')
	hdmf_no = fields.Char('HDMF No')
	philhealth_no = fields.Char('Philhealth No')

	nationality_id = fields.Many2one('res.country', 'Country')

	preffered_nickname = fields.Char('Preffered Nickname')


	pagibig_no = fields.Char('Pagibig Number')

	civil_status =  fields.Selection([('single', 'Single'), 
	                              ('married', 'Married'), 
	                              ('widower', 'Widower'), 
	                              ('divorced', 'Divorced'), 
	                              ('seperated', 'Seperated'), 
	                              ('live_in_partner', 'Live-in-partner'),
	                              ('annuled', 'Annuled')], 'Marital Status')

	gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')


	permanent_address_adress = fields.Char('Address')
	permanent_address_city = fields.Char('City')
	permanent_address_home_airport = fields.Selection([
        ('manila', 'Manila'),
        ('clarke', 'Clarke'),
        ('cebu', 'Cebu'),
        ('davao', 'Davao City')
    ], string='Home Airport')
	permanent_address_zipcode = fields.Char('Zipcode')
	permanent_address_contact_no = fields.Char('Contact No')

	alternative_address_adress = fields.Char('Address')
	alternative_address_city = fields.Char('City')
	alternative_address_zipcode = fields.Char('Zipcode')
	alternative_address_contact_no = fields.Char('Contact No')

	emergency_person_name = fields.Char('Name')
	emergency_relationship = fields.Char('Relationship')
	emergency_relationship_1 = fields.Char('Relationship')
	emergency_address = fields.Char('Address')
	emergency_zipcode = fields.Char('Zipcode')
	emergency_contactno = fields.Char('Contact No')



	applicant_families = fields.One2many('hr.applicant.family_details','applicant_family_relationship_id', readonly=False,copy=False)
	applicant_education = fields.One2many('hr.applicant.education','applicant_education_id', readonly=False,copy=False)
	applicant_document_ids = fields.One2many('hr.applicant.documents','applicant_documents_id', readonly=False,copy=False)

	applicant_denied_visa_ids = fields.One2many('hr.recruitment.denied.visa','applicant_id', readonly=False,copy=False)
	applicant_deported_ids = fields.One2many('hr.recruitment.deported','applicant_id', readonly=False,copy=False)
	applicant_training_courses_ids = fields.One2many('hr.recruitment.training.courses','applicant_id', readonly=False,copy=False)
	applicant_license_ids = fields.One2many('hr.recruitment.license','applicant_id', readonly=False,copy=False)

	applicant_medical_history_ids = fields.One2many('hr.recruitment.medical.history','applicant_id', readonly=False,copy=False)    
	applicant_medical_operation_ids = fields.One2many('hr.recruitment.medical.operation','applicant_id', readonly=False,copy=False)    
	applicant_medical_illness_ids = fields.One2many('hr.recruitment.medical.illness','applicant_id', readonly=False,copy=False)    

	applicant_employed_relatives_ids = fields.One2many('hr.recruitment.employee.relative','applicant_id', readonly=False,copy=False)    
	applicant_previous_application_ids = fields.One2many('hr.recruitment.previous.application','applicant_id', readonly=False,copy=False)    
	applicant_previous_employment_ids = fields.One2many('hr.recruitment.previous.employment','applicant_id', readonly=False,copy=False)


	applicant_socialmedia_ids = fields.One2many('hr.recruitment.socialmedia','applicant_id', readonly=False,copy=False)
	is_allowed_consent_form = fields.Boolean('Agreed in Consent')
	is_allowed_policy_rule = fields.Boolean('Agreed in Data Privacy')
	is_denied_visa = fields.Boolean('Denied Visa?')
	is_deported = fields.Boolean('Deported?')
	is_medical_reason_1 = fields.Boolean('Medical History?')
	is_medical_operation = fields.Boolean('Medical Operation?')
	has_hypertension = fields.Boolean('Hypertension?')
	has_diabetes = fields.Boolean('Diabetes')
	has_hepatitis_a_b = fields.Boolean('HEPA A or B')
	has_asthma = fields.Boolean('Asthma')
	is_smoker = fields.Boolean('Are you a smoker?')
	reference_1_company_name = fields.Char('Name of Company')
	reference_1_name_person = fields.Char('Name of Person')
	reference_1_address = fields.Char('Address')
	reference_1_contact_no = fields.Char('Contact Number')
	reference_2_company_name = fields.Char('Name of Company')
	reference_2_name_person = fields.Char('Name of Person')
	reference_2_address = fields.Char('Address')
	reference_2_contact_no = fields.Char('Contact Number')
	has_relative_employee = fields.Boolean('Employed Relative/s?')
	has_applied_previously = fields.Boolean('Previously Applied?')
	is_medical_his_true = fields.Boolean('I hereby declare that the above, including my Medical History is true.')

	interview_count =  fields.Integer('Interview Form', store = False, compute = "_interview_form_count")


	def _interview_form_count(self):
		for rec in self:
			interview_form_model = rec.env['hr.applicant.evaluation']
			rec.interview_count =  interview_form_model.search_count([('employment_application_id', '=', rec.id)])
		
	

	@api.depends('name','image')
	def _compute_avatar_128(self):
		super()._compute_avatar_128()


	@api.model
	def create(self, vals):
		vals['application_number'] = self._getEmpId()#obj_sequence.number_next_actual + 1        
		obj_sequence = self.env['ir.sequence'].search([('code','=', 'hr.applicant.sequence')])
		obj_sequence.write({'number_next_actual' : obj_sequence.number_next_actual + 1})
		new_record = super(hrApplicant, self).create(vals)
		return new_record


	@api.onchange('first_name','middle_name','last_name')
	def getFullname(self):
		if self.first_name == False:
			self.first_name=''
		if self.middle_name == False:
			self.middle_name=''
		if self.last_name == False:
			self.last_name=''
		self.partner_name = self.first_name + " " + self.middle_name + " " + self.last_name


	def create_employee_from_applicant(self):
		""" Create an hr.employee from the hr.applicants """
		employee = False
		for applicant in self:
			contact_name = False
			if applicant.partner_id:
				address_id = applicant.partner_id.address_get(['contact'])['contact']
				contact_name = applicant.partner_id.display_name
			else:
				if not applicant.partner_name:
					raise UserError(_('You must define a Contact Name for this applicant.'))
				new_partner_id = self.env['res.partner'].create({
			        'is_company': False,
			        'type': 'private',
			        'name': applicant.partner_name,
			        'email': applicant.email_from,
			        'phone': applicant.partner_phone,
			        'mobile': applicant.partner_mobile
			        })
				applicant.partner_id = new_partner_id
				address_id = new_partner_id.address_get(['contact'])['contact']
			if applicant.partner_name or contact_name:
				employee_data = {
			        'default_name': applicant.partner_name or contact_name,
			        'default_job_id': applicant.job_id.id,
			        'default_job_title': applicant.job_id.name,
			        'address_home_id': address_id,
			        'default_department_id': applicant.department_id.id or False,
			        'default_address_id': applicant.company_id and applicant.company_id.partner_id
			                and applicant.company_id.partner_id.id or False,
			        'default_work_email': applicant.department_id and applicant.department_id.company_id
			                and applicant.department_id.company_id.email or False,
			        'default_work_phone': applicant.department_id.company_id.phone,
			        'form_view_initial_mode': 'edit',
			        'default_applicant_id': applicant.ids,
                    'default_first_name': applicant.first_name,
                    'default_middle_name': applicant.middle_name,
                    'default_last_name': applicant.last_name,
	                'default_sss_no': applicant.sss_no or False,
	                'default_hdmf_no': applicant.hdmf_no or False,
	                'default_philhealth_no': applicant.philhealth_no or False,
	                'default_birthday': applicant.date_of_birth,
	                'default_placeof_birth': applicant.placeof_birth,
	                'default_gender': applicant.gender or False,
	                'default_marital': applicant.civil_status or False,
	                'default_country_id': applicant.nationality_id and applicant.nationality_id.id or False,
	                'default_height': applicant.shoe_size,
                    'default_image_1920': applicant.image_1920,
				}

				#Permament_address
				laddress = []
				if applicant.permanent_address_adress and applicant.permanent_address_city and applicant.permanent_address_contact_no:
					permanent_address_adress = [(0,0,{
                        'addresstype':1,
                        'address_1': applicant.permanent_address_adress,
                        'address_3': applicant.permanent_address_zipcode or False,
                        'home_airport': applicant.permanent_address_home_airport,
                        'city': applicant.permanent_address_city,
                        'telephone_number':applicant.permanent_address_contact_no,
                        'mobile_number':applicant.permanent_address_contact_no,
                    })]
					laddress = permanent_address_adress

				#Temporary Address
				if applicant.alternative_address_adress and applicant.alternative_address_city and applicant.alternative_address_contact_no:
					alternative_address_adress = [(0,0,{
                        'addresstype':2,
                        'address_1': applicant.alternative_address_adress,
                        'address_3': applicant.alternative_address_zipcode or False,
                        'city': applicant.alternative_address_city,
                        'telephone_number':applicant.alternative_address_contact_no,
                        'mobile_number':applicant.alternative_address_contact_no,
                    })]
					laddress += alternative_address_adress
				if len(laddress) > 0:
					employee_data['default_employee_addresses'] = laddress


				applicant_families_list =[]
				for family_details in applicant.applicant_families:
					applicant_families_list.append((0,0,{
                        'relation_level':1,
                        'relationship':family_details and family_details.relationship and family_details.relationship.id or False,
                        'last_name': family_details.last_name,
                        'first_name':family_details.first_name,
                        'middle_name':family_details.middle_name,
                        'birthday':family_details.date_of_birth,
                        'placeof_birth': family_details.placeof_birth,
                        'gender': family_details.gender,
                    }))

				#Get Educational Background
				employee_education = []
				for educational_background in applicant.applicant_education:
					employee_education.append((0,0,{
                        'schooltype':educational_background and educational_background.schooltype and educational_background.schooltype.id or False,
                        'name_school': educational_background.name_school,
                        'date_from':educational_background.date_from,
                        'date_to':educational_background.date_to,
                        'school_address':educational_background.school_address,
                        'description': educational_background.description,
                    }))

				#Get Documents
				applicant_document_ids = []
				for document in applicant.applicant_document_ids:
					applicant_document_ids.append((0,0,{
                        'document':document and document.document and document.document.id or False,
                        'document_number': document.document_number,
                        'date_issued':document.date_issued,
                        'date_expiry':document.date_expiry,
                        'issuing_authority':document.issuing_authority,
                        'place_ofissue': document.place_ofissue,
                    }))

				licenses =[]
				#For Training
				for training in applicant.applicant_training_courses_ids:
					licenses.append((0,0,{
                        'licensetype':18,
                        'license': training and training.training_id and training.training_id.id or False,
                        'doc_number': training.document_no,
                        'country': 178,
                        'date_issued': training.issue_date,
                        'date_expiry': False,
                        'place_issue':training.training_centers or '',
                        'authority_issue': False,
                        'remarks': training.training_name,
                    }))

				#Get License
				for training in applicant.applicant_license_ids:
					ISSUING_AUTH = {'1': 'Marina','2': 'Bahamas Maritime','3': 'Others'}

					str_issuing_auth = training.issuing_authority_other

					if training.issuing_authority:
						if training.issuing_authority == '3':
							str_issuing_auth = training.issuing_authority_other
						else:
							str_issuing_auth = ISSUING_AUTH[training.issuing_authority]

					licenses.append((0,0,{
                        'licensetype':17,
                        'license': training and training.training_id and training.training_id.id or False,
                        'doc_number': training.document_no,
                        'country': 178,
                        'date_issued': training.issue_date,
                        'date_expiry': training.expiry_date,
                        'place_issue': '',
                        'authority_issue': str_issuing_auth,
                        'remarks': training.training_name,
                    }))


				employee_data['default_employee_families'] = applicant_families_list
				employee_data['default_employee_education'] = employee_education
				employee_data['default_employee_documents'] = applicant_document_ids
				employee_data['default_employee_licenses'] = licenses

		dict_act_window = self.env['ir.actions.act_window']._for_xml_id('hr.open_view_employee_list')
		dict_act_window['context'] = employee_data
		return dict_act_window


class HrApplicantFamilies(models.Model):
	_name = 'hr.applicant.family_details'
	_description = 'HR Applicant Family Details'
	_order = 'applicant_family_relationship_id'


	applicant_family_relationship_id = fields.Many2one('hr.applicant')
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
	date_of_birth = fields.Date('Date of Birth')


class HrApplicantEducation(models.Model):
	_name = 'hr.applicant.education'
	_description = 'HR Applicant Education'

	applicant_education_id = fields.Many2one('hr.applicant')
	schooltype = fields.Many2one('hr.recruitment.degree','Degree')
	name_school = fields.Char('School/College University')
	date_from = fields.Date('Date From')
	date_to = fields.Date('Date To')
	school_address = fields.Char('Place')
	description = fields.Text('Remarks')

	@api.onchange('date_to')
	def checkDate(self):
		if self.date_to < self.date_from:
			raise ValidationError('Date to is less than the Date from.')

class HrApplicantDocuments(models.Model):
	_name = 'hr.applicant.documents'
	_description = 'HR Applicant Documents'
	_order = 'date_expiry,date_expiry,document'

	applicant_documents_id = fields.Many2one('hr.applicant')
	document = fields.Many2one('hr.documenttype','Document Type')
	document_number = fields.Char('Document No.')
	date_issued = fields.Date('Date Issued')
	date_expiry = fields.Date('Date Expiry')
	issuing_authority = fields.Char('Issuing Authority')
	place_ofissue = fields.Char('Place of Issue')

	@api.onchange('date_to')
	def checkDate(self):
		if self.date_to < self.date_from:
			raise ValidationError('Date to is less than the Date from.')

class HrApplicantDeniedVisa(models.Model):
	_name = 'hr.recruitment.denied.visa'
	_description = 'HR Recruitment Denied Visa'

	applicant_id = fields.Many2one('hr.applicant')
	nationality_id = fields.Many2one('res.country', 'Country')
	date_denied = fields.Date('Date Denied')
	reason = fields.Text('Reason')

class HrApplicantDeported(models.Model):
	_name = 'hr.recruitment.deported'
	_description = 'HR Recruitment Deported'

	applicant_id = fields.Many2one('hr.applicant')
	nationality_id = fields.Many2one('res.country', 'Country')
	date_deported = fields.Date('Date Deported')
	reason = fields.Text('Reason')  

class HrApplicantTrainingCourses(models.Model):
	_name = 'hr.recruitment.training.courses'
	_description = 'HR Recruitment Training Courses'

	applicant_id = fields.Many2one('hr.applicant')

	training_id = fields.Many2one('hr.license','Training')
	training_name = fields.Char('Training Name') 
	document_no = fields.Char('Document No.') 
	issue_date = fields.Date('Issue Date')
	training_centers = fields.Char('Training Centers')
	is_with_cop = fields.Boolean('With COP?')
	issue_date_cop = fields.Date('Issued Date of COP')

class HrApplicantTrainingCourses(models.Model):
	_name = 'hr.recruitment.license'
	_description = 'HR Recruitment Licenses'

	applicant_id = fields.Many2one('hr.applicant')

	training_id = fields.Many2one('hr.license','Training')
	training_name = fields.Char('Training Name') 
	document_no = fields.Char('Document No.') 
	issue_date = fields.Date('Issue Date')
	expiry_date = fields.Date('Expiry Date')
	issuing_authority = fields.Selection([('1', 'Marina'), ('2', 'Bahamas Maritime'), ('3', 'Others')], 'Issuing Authority')
	issuing_authority_other = fields.Char('Other Issuing Authority')

class HrApplicantMedicalHistoryMedInShip(models.Model):
	_name = 'hr.recruitment.medical.history'
	_description = 'HR Recruitment Medical History'

	applicant_id = fields.Many2one('hr.applicant')

	vessel_name = fields.Char('Vessel Name') 
	occurence_place = fields.Char('Place of Occurence') 
	occurence_date = fields.Date('Date of Occurence')
	description = fields.Text('Description')

class HrApplicantMedicalHistoryMedOperation(models.Model):
	_name = 'hr.recruitment.medical.operation'
	_description = 'HR Recruitment Medical Operation'

	applicant_id = fields.Many2one('hr.applicant')

	details_of_operation = fields.Char('Details of Operation') 
	date_of_operation = fields.Date('Date of Operation')
	period_of_disability = fields.Integer('Periods of Disability')
	#date_of_operation = fields.Date('Date of Operation')
	occurence_date = fields.Date('Date of Occurence')
	description = fields.Text('Description')

class HrApplicantMedicalHistoryMedIllness(models.Model):
	_name = 'hr.recruitment.medical.illness'
	_description = 'HR Recruitment Medical Illness'

	applicant_id = fields.Many2one('hr.applicant')

	details_of_illness_accident = fields.Char('Details of Illness/Accident') 
	date_illness_accident = fields.Date('Date')
	therapy_treatment_description = fields.Text('Therapy/Treatment')


class HrApplicantEmployeeRelative(models.Model):
	_name = 'hr.recruitment.employee.relative'
	_description = 'HR Recruitment Employee Relative'

	applicant_id = fields.Many2one('hr.applicant')

	name_of_crew = fields.Char('Place of Occurence')
	position_and_principal = fields.Char('Place of Occurence')
	relationship = fields.Many2one('hr.familyrelations','Relationship')


class HrApplicantPrevApplication(models.Model):
	_name = 'hr.recruitment.previous.application'
	_description = 'HR Recruitment Previous Applicantion'

	applicant_id = fields.Many2one('hr.applicant')

	date_applied = fields.Date('Date')
	job_applied_id = fields.Many2one('hr.job', 'Position')


class HrApplicantPrevApplication(models.Model):
	_name = 'hr.recruitment.previous.employment'
	_description = 'HR Recruitment Previous Employment'

	applicant_id = fields.Many2one('hr.applicant')

	rank_position = fields.Char('Rank/Position')
	manning_agency = fields.Char('Manning Agency')
	employer_principal = fields.Char('Employer/Principal')



	address_contact_info_manning_agen = fields.Char('Address and Contact No. of Manning Agency')
	vessel_name = fields.Char('Vessel Name')
	vessel_type = fields.Selection([('gcd', 'GCD - General Cargo'), 
	                                ('obo', 'OBO - Ore/Bulk/Oil Carriers'),
	                                ('gas', 'GAS - LPG/LNG Gas Carrier'),
	                                ('osv', 'OSV - Offshore Supply Vessel'),
	                                ('b_c', 'B/C - Bulk Carrier'),
	                                ('tnc', 'TNC - Tanker (Crude)'),
	                                ('chm', 'CHM - Chemical Carriers'),
	                                ('drg', 'DRG - Dredgers'),
	                                ('con', 'CON - Cellular Container'),
	                                ('tnp', 'TNP - Tanker(Product)'),
	                                ('pas', 'PAS - Passenger Ship'),
	                                ('srv', 'SRV - Survey Ship'),
	                                ('mlp', 'MLP - Multipurpose'),
	                                ('tnv', 'TNV - VLCC/ULCC'),
	                                ('r_o', 'R/O - Ro/Ro Carriers'),
	                                ('log', 'LOG - Log/Timber'),
	                                ('o_o', 'O/O - Ore/Oil Carrier'),
	                                ('tns', 'TNS - Tanker (Storage)'),
	                                ('c_s', 'C/S - Car Ship'),
	                                ('rfr', 'RFR - Reefer'),
	                                ('psv_smc', 'SEI - Seismic'),
	                                ('psv_pltsprt', 'PSV - Platform Support'),
	                                ('psv_subsea', 'SUB - Subsea'),
	                                ('psv_drill', 'DRL - Drill'),
	                                ('dsv_dsprt', 'DSV - Diving Support'),
	                                ('dsv_accmd', 'ACV - Accomodation'),
	                                ('plv_pplying', 'PLV - Pipe Laying'),
	                                ('ahtv_anchundlingtug', 'AHTV - Anchor Handling Tug Vessel'),
	                                ('dsv_dpwcons', 'DCV - Deep Water Construction'),
	                                ('clv_cbllayingvsl', 'CLV - Cable Laying Vessel'),
	                                ('csv_conssupvessl', 'CSV - Construction Support Vessels'),
	                               ], 
	                               'Vessel Type')
	grt = fields.Char('GRT')

	date_from = fields.Date('Date From')
	date_to = fields.Date('Date To')

	duties_and_responsibility = fields.Text('Duties and Responsibilities')

class HrApplicantSocialMedia(models.Model):
	_name = 'hr.recruitment.socialmedia'
	_description = 'HR Recruitment Social Media'

	applicant_id = fields.Many2one('hr.applicant')
	name = fields.Char('Personal Link', required=True)
	socialmedia_id = fields.Many2one('hr.socialmedia.config', string="Social Media Platform")

class SocialMedia(models.Model):
	_name = 'hr.socialmedia.config'
	_description = 'Social Media Configuration'

	name = fields.Char('Social Media', required=True)
	allow_to_add_in_application  = fields.Boolean('Allow to View in Website', default=False)