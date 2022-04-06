# -*- encoding: utf-8 -*-
from openerp import models, fields, api
#from openerp.osv import fields, osv
from openerp.tools.translate import _

from openerp import SUPERUSER_ID
from openerp import tools
from openerp.modules.module import get_module_resource
from openerp.osv import fields as osv_fields, osv as osv_osv

class ExtendHrApplicantv7(osv_osv.osv):
    _inherit = ['hr.applicant']

    #def _get_image(self, cr, uid, ids, name, args, context=None):
    #    result = dict.fromkeys(ids, False)
    #    for obj in self.browse(cr, uid, ids, context=context):
    #        result[obj.id] = tools.image_get_resized_images(obj.image)
    #    return result

    #def _set_image(self, cr, uid, id, name, value, args, context=None):
    #    return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

    _columns = {
        'image': osv_fields.binary("Photo",
            help="This field holds the image used as photo for the employee, limited to 1024x1024px."),

     #   'image_medium': osv_fields.function(_get_image, fnct_inv=_set_image,
     #       string="Medium-sized photo", type="binary", multi="_get_image",
     #       store = {
     #           'hr.employee': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
     #       },
     #       help="Medium-sized photo of the employee. It is automatically "\
     #            "resized as a 128x128px image, with aspect ratio preserved. "\
     #            "Use this field in form views or some kanban views."),
     #   'image_small': osv_fields.function(_get_image, fnct_inv=_set_image,
     #       string="Small-sized photo", type="binary", multi="_get_image",
     #       store = {
     #           'hr.employee': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
     #       },
     #       help="Small-sized photo of the employee. It is automatically "\
     #            "resized as a 64x64px image, with aspect ratio preserved. "\
     #            "Use this field anywhere a small image is required."),
    }

    def _get_default_image(self, cr, uid, context=None):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    defaults = {
        'image': _get_default_image,
    }

class ExtendHrApplicant(models.Model):
    _name = 'hr.applicant'
    _inherit = ['hr.applicant']


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



    @api.model
    def create(self, vals):
        vals['application_number'] = self._getEmpId()#obj_sequence.number_next_actual + 1        
        obj_sequence = self.env['ir.sequence'].search([('code','=', 'hr.applicant.sequence')])
        obj_sequence.write({'number_next_actual' : obj_sequence.number_next_actual + 1})


        new_record = super(ExtendHrApplicant, self).create(vals)
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


    # Overriding the create_employee_from_applicant from hr.applicants object
    #@api.one
    #def create_employee_from_applicant(self):
    #    cr = self._cr
    #    uid = self._uid
    #    ids = self.ids
    #    context = self._context

    #    super(ExtendHrApplicant, self).create_employee_from_applicant()
    #    hr_employee = self.env['hr.employee'].search([('id', '=', int(self.emp_id[0]))])
    #    hr_employee.write({
    #                        'first_name': self.first_name,
    #                        'middle_name': self.middle_name,
    #                        'last_name': self.last_name,
    #      
    #                  })

    #@api.multi
    #def write(self, vals):

    #    if vals.has_keys('stage_id'):
    #        for employee in self:
    #            if employee.emp_id 
    #    super(ExtendHrApplicant, self).write()


    def create_employee_from_applicant(self, cr, uid, ids, context=None):
        """ Create an hr.employee from the hr.applicants """
        if context is None:
            context = {}
        hr_employee = self.pool.get('hr.employee')
        model_data = self.pool.get('ir.model.data')
        act_window = self.pool.get('ir.actions.act_window')
        emp_id = False
        for applicant in self.browse(cr, uid, ids, context=context):
            address_id = contact_name = False
            if applicant.partner_id:
                address_id = self.pool.get('res.partner').address_get(cr, uid, [applicant.partner_id.id], ['contact'])['contact']
                contact_name = self.pool.get('res.partner').name_get(cr, uid, [applicant.partner_id.id])[0][1]
            if applicant.job_id and (applicant.partner_name or contact_name):
                applicant.job_id.write({'no_of_hired_employee': applicant.job_id.no_of_hired_employee + 1})
                create_ctx = dict(context, mail_broadcast=True)
                emp_id = hr_employee.create(cr, uid, {'name': applicant.partner_name or contact_name,
                                                     'job_id': applicant.job_id.id,
                                                     'address_home_id': address_id,
                                                     'department_id': applicant.department_id.id or False,
                                                     'address_id': applicant.company_id and applicant.company_id.partner_id and applicant.company_id.partner_id.id or False,
                                                     'work_email': applicant.department_id and applicant.department_id.company_id and applicant.department_id.company_id.email or False,
                                                     'work_phone': applicant.department_id and applicant.department_id.company_id and applicant.department_id.company_id.phone or False,
                                                     'first_name': applicant.first_name,
                                                     'middle_name': applicant.middle_name,
                                                     'last_name': applicant.last_name,                                                     
                                                     }, context=create_ctx)
                self.write(cr, uid, [applicant.id], {'emp_id': emp_id}, context=context)
                self.pool['hr.job'].message_post(
                    cr, uid, [applicant.job_id.id],
                    body=_('New Employee %s Hired') % applicant.partner_name if applicant.partner_name else applicant.name,
                    subtype="hr_recruitment.mt_job_applicant_hired", context=context)
            else:
                raise osv.except_osv(_('Warning!'), _('You must define an Applied Job and a Contact Name for this applicant.'))

        action_model, action_id = model_data.get_object_reference(cr, uid, 'hr', 'open_view_employee_list')
        dict_act_window = act_window.read(cr, uid, [action_id], [])[0]
        if emp_id:
            dict_act_window['res_id'] = emp_id
        dict_act_window['view_mode'] = 'form,tree'
        return dict_act_window



class HrApplicantFamilies(models.Model):
    _name = 'hr.applicant.family_details'
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

#    @api.constrains('date_to','date_from')
#    def checkConstrainDate(self):
#        if self.date_to < self.date_from:
#            raise ValidationError('Date to is less than the Date from.')


class HrApplicantDocuments(models.Model):
    _name = 'hr.applicant.documents'
    
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

#    @api.constrains('date_to','date_from')
#    def checkConstrainDate(self):
#        if self.date_to < self.date_from:
#            raise ValidationError('Date to is less than the Date from.')

class HrApplicantDeniedVisa(models.Model):
    _name = 'hr.recruitment.denied.visa'

    applicant_id = fields.Many2one('hr.applicant')
    nationality_id = fields.Many2one('res.country', 'Country')
    date_denied = fields.Date('Date Denied')
    reason = fields.Text('Reason')

class HrApplicantDeported(models.Model):
    _name = 'hr.recruitment.deported'

    applicant_id = fields.Many2one('hr.applicant')
    nationality_id = fields.Many2one('res.country', 'Country')
    date_deported = fields.Date('Date Deported')
    reason = fields.Text('Reason')  

class HrApplicantTrainingCourses(models.Model):
    _name = 'hr.recruitment.training.courses'

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

    applicant_id = fields.Many2one('hr.applicant')

    vessel_name = fields.Char('Vessel Name') 
    occurence_place = fields.Char('Place of Occurence') 
    occurence_date = fields.Date('Date of Occurence')
    description = fields.Text('Description')

class HrApplicantMedicalHistoryMedOperation(models.Model):
    _name = 'hr.recruitment.medical.operation'

    applicant_id = fields.Many2one('hr.applicant')

    details_of_operation = fields.Char('Details of Operation') 
    date_of_operation = fields.Date('Date of Operation')
    period_of_disability = fields.Integer('Periods of Disability')
    #date_of_operation = fields.Date('Date of Operation')
    occurence_date = fields.Date('Date of Occurence')
    description = fields.Text('Description')

class HrApplicantMedicalHistoryMedIllness(models.Model):
    _name = 'hr.recruitment.medical.illness'

    applicant_id = fields.Many2one('hr.applicant')

    details_of_illness_accident = fields.Char('Details of Illness/Accident') 
    date_illness_accident = fields.Date('Date')
    therapy_treatment_description = fields.Text('Therapy/Treatment')


class HrApplicantEmployeeRelative(models.Model):
    _name = 'hr.recruitment.employee.relative'

    applicant_id = fields.Many2one('hr.applicant')

    name_of_crew = fields.Char('Place of Occurence')
    position_and_principal = fields.Char('Place of Occurence')
    relationship = fields.Many2one('hr.familyrelations','Relationship')


class HrApplicantPrevApplication(models.Model):
    _name = 'hr.recruitment.previous.application'

    applicant_id = fields.Many2one('hr.applicant')

    date_applied = fields.Date('Date')
    job_applied_id = fields.Many2one('hr.job', 'Position')


class HrApplicantPrevApplication(models.Model):
    _name = 'hr.recruitment.previous.employment'

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

    applicant_id = fields.Many2one('hr.applicant')
    name = fields.Char('Personal Link', required=True)
    socialmedia_id = fields.Many2one('hr.socialmedia.config', string="Social Media Platform")

class SocialMedia(models.Model):
    _name = 'hr.socialmedia.config'

    name = fields.Char('Social Media', required=True)
    allow_to_add_in_application  = fields.Boolean('Allow to View in Website', default=False)