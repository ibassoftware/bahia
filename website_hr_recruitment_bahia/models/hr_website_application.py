from openerp import models, fields,api
from openerp.exceptions import except_orm, Warning, RedirectWarning,ValidationError

class recruitment_application(models.Model):
    _name = 'website.recruitment.application'

    name = fields.Char('Application Title')
    job_applied_id = fields.Many2one('hr.job', 'Applied Jobs')
    first_name = fields.Char()
    last_name = fields.Char()
    maiden_name = fields.Char()
    date_of_birth = fields.Date()
    place_of_birth = fields.Char()
    height = fields.Char()
    weight = fields.Char()
    preferred_nickname = fields.Char()
    shoe_size = fields.Char()
    email_address = fields.Char()
    contact_number = fields.Char()
    sss_no = fields.Char()
    philhealth_no = fields.Char()
    pagibig_no = fields.Char()
    civil_status = fields.Char()
    gender = fields.Char()
    permanent_address_adress = fields.Char()
    permanent_address_city = fields.Char()
    permanent_address_zipcode = fields.Char()
    permanent_address_contact_no = fields.Char()

    alternative_address_adress = fields.Char()
    alternative_address_city = fields.Char()
    alternative_address_zipcode = fields.Char()
    alternative_address_contact_no = fields.Char()

    emergency_person_name = fields.Char()
    emergency_relationship = fields.Char()
    emergency_address = fields.Char()
    emergency_zipcode = fields.Char()
    emergency_contactno = fields.Char()

    applicant_families = fields.One2many('website.recruitment.application.family_details','applicant_family_relationship_id', readonly=False,copy=False)
    applicant_education = fields.One2many('website.recruitment.application.education','applicant_education_id', readonly=False,copy=False)    
    applicant_document_ids = fields.One2many('website.recruitment.application.documents','applicant_documents_id', readonly=False,copy=False)
    applicant_denied_visa_ids = fields.One2many('website.recruitment.denied.visa','applicant_id', readonly=False,copy=False)
    applicant_deported_ids = fields.One2many('website.recruitment.deported','applicant_id', readonly=False,copy=False)
    applicant_training_courses_ids = fields.One2many('website.recruitment.training.courses','applicant_id', readonly=False,copy=False)
    applicant_license_ids = fields.One2many('website.recruitment.license','applicant_id', readonly=False,copy=False)

    applicant_medical_history_ids = fields.One2many('website.recruitment.medical.history','applicant_id', readonly=False,copy=False)    
    applicant_medical_operation_ids = fields.One2many('website.recruitment.medical.operation','applicant_id', readonly=False,copy=False)    
    applicant_medical_illness_ids = fields.One2many('website.recruitment.medical.illness','applicant_id', readonly=False,copy=False)    

    applicant_employed_relatives_ids = fields.One2many('website.recruitment.employee.relative','applicant_id', readonly=False,copy=False)    
    applicant_previous_application_ids = fields.One2many('website.recruitment.previous.application','applicant_id', readonly=False,copy=False)    
    applicant_previous_employment_ids = fields.One2many('website.recruitment.previous.employment','applicant_id', readonly=False,copy=False)

    applicant_socialmedia_ids = fields.One2many('website.recruitment.socialmedia','applicant_id', readonly=False,copy=False)       

    nationality_id = fields.Many2one('res.country', 'Country')

    is_allowed_consent_form = fields.Boolean('Agreed in Consent')
    is_allowed_policy_rule = fields.Boolean('Agreed in Data Privacy')

    is_denied_visa = fields.Boolean('Denied Visa?')
    is_deported = fields.Boolean('Deported?')

    is_medical_reason_1 = fields.Boolean('Have you ever singed of a ship due to medical reason?')
    is_medical_operation = fields.Boolean('Have you ever undergone any operation in the past?')

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


    has_relative_employee = fields.Boolean('A.  Do you have any relatives working with us at present?')
    has_applied_previously = fields.Boolean('B. Have you ever applied for a job with us before?')

    image= fields.Binary('Applicant Imge')
    is_medical_his_true = fields.Boolean('I hereby declare that the above, including my Medical History is true.')

    accept_privacy_policy = fields.Boolean('Privacy Policy Acceptance')



class HrApplicantFamilies(models.Model):
    _name = 'website.recruitment.application.family_details'
    _order = 'applicant_family_relationship_id'


    applicant_family_relationship_id = fields.Many2one('website.recruitment.application')
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
    allow_delete = fields.Boolean('Allowed to Delete', default = True)


    @api.model
    def getRelationIDByName(self, relation_name=''):
        relationship_obj = self.env['hr.familyrelations'].search([('name','=',relation_name)])
        return relationship_obj and relationship_obj.id or False




class HrApplicantEducation(models.Model):
    _name = 'website.recruitment.application.education'
    applicant_education_id = fields.Many2one('website.recruitment.application')
    schooltype = fields.Many2one('hr.recruitment.degree','Degree')
    name_school = fields.Char('School/College University')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    school_address = fields.Char('Place')
    description = fields.Text('Remarks')
    allow_delete = fields.Boolean('Allowed to Delete', default = True)

    @api.onchange('date_to')
    def checkDate(self):
        if self.date_to < self.date_from:
            raise ValidationError('Date to is less than the Date from.')

#    @api.constrains('date_to','date_from')
#    def checkConstrainDate(self):
#        if self.date_to < self.date_from:
#            raise ValidationError('Date to is less than the Date from.')

class HrApplicantDocuments(models.Model):
    _name = 'website.recruitment.application.documents'
    
    _order = 'date_expiry,date_expiry,document'

    applicant_documents_id = fields.Many2one('website.recruitment.application')
    document = fields.Many2one('hr.documenttype','Document Type')
    document_number = fields.Char('Document No.')
    date_issued = fields.Date('Date Issued')
    date_expiry = fields.Date('Date Expiry')
    issuing_authority = fields.Char('Issuing Authority')
    place_ofissue = fields.Char('Place of Issue')
    allow_delete = fields.Boolean('Allowed to Delete', default = True)

    @api.onchange('date_expiry')
    def checkDate(self):
        if self.date_expiry:
            if self.date_expiry < self.date_issued:
                raise ValidationError('Date Expiry is less than the Date from.')

    @api.model
    def getDocumentByName(self, document_name=''):
        document_obj = self.env['hr.documenttype'].search([('name','=',document_name)])
        return document_obj and document_obj.id or False

#    @api.constrains('date_issued','date_expiry')
#    def checkConstrainDate(self):
#        if self.date_expiry:
#            if self.date_expiry < self.date_issued:
#                raise ValidationError('Date Expiry is less than the Date from.')

class HrApplicantDeniedVisa(models.Model):
    _name = 'website.recruitment.denied.visa'

    applicant_id = fields.Many2one('website.recruitment.application')
    nationality_id = fields.Many2one('res.country', 'Country')
    date_denied = fields.Date('Date Denied')
    reason = fields.Text('Reason')
    allow_delete = fields.Boolean('Allowed to Delete', default = True)

class HrApplicantDeported(models.Model):
    _name = 'website.recruitment.deported'

    applicant_id = fields.Many2one('website.recruitment.application')
    nationality_id = fields.Many2one('res.country', 'Country')
    date_deported = fields.Date('Date Deported')
    reason = fields.Text('Reason')
    allow_delete = fields.Boolean('Allowed to Delete', default = True)

class HrApplicantTrainingCourses(models.Model):
    _name = 'website.recruitment.training.courses'

    applicant_id = fields.Many2one('website.recruitment.application')

    training_id = fields.Many2one('hr.license','Training')

    training_name = fields.Char('Training Name') 
    document_no = fields.Char('Document No.') 
    issue_date = fields.Date('Issue Date')
    training_centers = fields.Char('Training Centers')
    is_with_cop = fields.Boolean('With COP?')
    issue_date_cop = fields.Date('Issued Date of COP')
    allow_delete = fields.Boolean('Allowed to Delete', default = True)

class HrApplicantTrainingCourses(models.Model):
    _name = 'website.recruitment.license'

    applicant_id = fields.Many2one('website.recruitment.application')

    license_id = fields.Many2one('hr.license','License')

    training_name = fields.Char('Training Name') 
    document_no = fields.Char('Document No.') 
    issue_date = fields.Date('Issue Date')
    expiry_date = fields.Date('Expiry Date')
    issuing_authority = fields.Selection([('1', 'Marina'), ('2', 'Bahamas Maritime'), ('3', 'Others')], 'Issuing Authority')
    issuing_authority_other = fields.Char('Other Issuing Authority')
    allow_delete = fields.Boolean('Allowed to Delete', default = True)

class HrApplicantMedicalHistoryMedInShip(models.Model):
    _name = 'website.recruitment.medical.history'

    applicant_id = fields.Many2one('website.recruitment.application')

    vessel_name = fields.Char('Vessel Name') 
    occurence_place = fields.Char('Place of Occurence') 
    occurence_date = fields.Date('Date of Occurence')
    description = fields.Text('Description')
    allow_delete = fields.Boolean('Allowed to Delete', default = True)

class HrApplicantMedicalHistoryMedOperation(models.Model):
    _name = 'website.recruitment.medical.operation'

    applicant_id = fields.Many2one('website.recruitment.application')

    details_of_operation = fields.Char('Details of Operation') 
    date_of_operation = fields.Date('Date of Operation')
    period_of_disability = fields.Integer('Periods of Disability')
    #date_of_operation = fields.Date('Date of Operation')
    occurence_date = fields.Date('Date of Occurence')
    description = fields.Text('Description')
    allow_delete = fields.Boolean('Allowed to Delete', default = True)

class HrApplicantMedicalHistoryMedIllness(models.Model):
    _name = 'website.recruitment.medical.illness'

    applicant_id = fields.Many2one('website.recruitment.application')

    details_of_illness_accident = fields.Char('Details of Illness/Accident') 
    date_illness_accident = fields.Date('Date')
    therapy_treatment_description = fields.Text('Therapy/Treatment')
    allow_delete = fields.Boolean('Allowed to Delete', default = True)


class HrApplicantEmployeeRelative(models.Model):
    _name = 'website.recruitment.employee.relative'

    applicant_id = fields.Many2one('website.recruitment.application')

    name_of_crew = fields.Char('Place of Occurence')
    position_and_principal = fields.Char('Place of Occurence')
    relationship = fields.Many2one('hr.familyrelations','Relationship')
    allow_delete = fields.Boolean('Allowed to Delete', default = True)


class HrApplicantPrevApplication(models.Model):
    _name = 'website.recruitment.previous.application'

    applicant_id = fields.Many2one('website.recruitment.application')

    date_applied = fields.Date('Date')
    job_applied_id = fields.Many2one('hr.job', 'Position')
    allow_delete = fields.Boolean('Allowed to Delete', default = True)


class HrApplicantPrevApplication(models.Model):
    _name = 'website.recruitment.previous.employment'

    applicant_id = fields.Many2one('website.recruitment.application')

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
                                   ], 
                                   'Vessel Type')
    grt = fields.Char('GRT')

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')

    duties_and_responsibility = fields.Text('Duties and Responsibilities')
    allow_delete = fields.Boolean('Allowed to Delete', default = True)

class HrApplicantSocialMedia(models.Model):
    _name = 'website.recruitment.socialmedia'

    applicant_id = fields.Many2one('website.recruitment.application')
    name = fields.Char('Personal Link', required=True)
    socialmedia_id = fields.Many2one('hr.socialmedia.config', string="Social Media Platform")