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
                                                     'sss_no': applicant.sss_no or False,
                                                     'hdmf_no': applicant.hdmf_no or False,
                                                     'philhealth_no': applicant.philhealth_no or False,
                                                     'birthday': applicant.date_of_birth,
                                                     'placeof_birth': applicant.placeof_birth,
                                                     'gender': applicant.gender or False,
                                                     'marital': applicant.civil_status or False,
                                                     'country_id': applicant.nationality_id and applicant.nationality_id.id or False,
                                                     'height': applicant.shoe_size,
                                                     'image': applicant.image or False,
                                                     }, context=create_ctx)

                if emp_id:
                    #Get Family Details
                    applicant_id = emp_id
                    employee_education = self.pool.get('hr.employeducation')
                    employee_family = self.pool.get('hr.employee_families')
                    employee_documents = self.pool.get('hr.employee_documents')
                    employee_employee_licenses = self.pool.get('hr.employeelicenses')
                    employee_address = self.pool.get('hr.employeeaddress')

                    #For Address
                    #Permanent Address
                    if applicant.permanent_address_adress and applicant.permanent_address_city and applicant.permanent_address_contact_no:
                        employee_address.create(cr, uid,{
                            'employee_address_id': applicant_id,
                            'addresstype':1,
                            'address_1': applicant.permanent_address_adress,
                            'address_3': applicant.permanent_address_zipcode or False,
                            'city': applicant.permanent_address_city,
                            'telephone_number':applicant.permanent_address_contact_no,
                            'mobile_number':applicant.permanent_address_contact_no,
                            }
                            ,context=create_ctx)

                    #Temporary Address
                    if applicant.alternative_address_adress and applicant.alternative_address_city and applicant.alternative_address_contact_no:
                        employee_address.create(cr, uid,{
                            'employee_address_id': applicant_id,
                            'addresstype':2,
                            'address_1': applicant.alternative_address_adress,
                            'address_3': applicant.alternative_address_zipcode or False,
                            'city': applicant.alternative_address_city,
                            'telephone_number':applicant.alternative_address_contact_no,
                            'mobile_number':applicant.alternative_address_contact_no,
                            }
                            ,context=create_ctx)                    


                    for family_details in applicant.applicant_families:
                        employee_family.create(cr, uid,{
                            'employee_family_relationship_id': applicant_id,
                            'relation_level':1,
                            'relationship':family_details and family_details.relationship and family_details.relationship.id or False,
                            'last_name': family_details.last_name,
                            'first_name':family_details.first_name,
                            'middle_name':family_details.middle_name,
                            'birthday':family_details.date_of_birth,
                            'placeof_birth': family_details.placeof_birth,
                            'gender': family_details.gender,}
                            ,context=create_ctx)
                    #Get Educational Background
                    for educational_background in applicant.applicant_education:
                        employee_education.create(cr, uid,{
                            'employee_education_id': applicant_id,
                            'schooltype':educational_background and educational_background.schooltype and educational_background.schooltype.id or False,
                            'name_school': educational_background.name_school,
                            'date_from':educational_background.date_from,
                            'date_to':educational_background.date_to,
                            'school_address':educational_background.school_address,
                            'description': educational_background.description,
                            }
                            ,context=create_ctx)
                    #Get Documents
                    for document in applicant.applicant_document_ids:
                        employee_documents.create(cr, uid,{
                            'employee_doc_id': applicant_id,
                            'document':document and document.document and document.document.id or False,
                            'document_number': document.document_number,
                            'date_issued':document.date_issued,
                            'date_expiry':document.date_expiry,
                            'issuing_authority':document.issuing_authority,
                            'place_ofissue': document.place_ofissue,
                            }
                            ,context=create_ctx)
                    #For Training
                    for training in applicant.applicant_training_courses_ids:
                        employee_employee_licenses.create(cr, uid,{
                            'employee_licenses_id':applicant_id,
                            'licensetype':18,
                            'license': training and training.training_id and training.training_id.id or False,
                            'doc_number': training.document_no,
                            'country': 178,
                            'date_issued': training.issue_date,
                            'date_expiry': False,
                            'place_issue':training.training_centers or '',
                            'authority_issue': False,
                            'remarks': training.training_name,
                            }
                            ,context=create_ctx)

                    #Get License
                    for training in applicant.applicant_license_ids:
                        ISSUING_AUTH = {'1': 'Marina',
                                        '2': 'Bahamas Maritime',
                                        '3': 'Others'}

                        str_issuing_auth = training.issuing_authority_other


                        if training.issuing_authority:
                            if training.issuing_authority == '3':
                                str_issuing_auth = training.issuing_authority_other
                            else:
                                str_issuing_auth = ISSUING_AUTH[training.issuing_authority]

                        employee_employee_licenses.create(cr, uid, {
                            'employee_licenses_id':applicant_id,
                            'licensetype':17,
                            'license': training and training.training_id and training.training_id.id or False,
                            'doc_number': training.document_no,
                            'country': 178,
                            'date_issued': training.issue_date,
                            'date_expiry': training.expiry_date,
                            'place_issue': '',
                            'authority_issue': str_issuing_auth,
                            'remarks': training.training_name,
                            }
                            ,context=create_ctx)

                self.write(cr, uid, [applicant.id], {'emp_id': emp_id, 'active': False}, context=context)
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