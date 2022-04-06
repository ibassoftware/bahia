# -*- coding: utf-8 -*-
import base64

from openerp import SUPERUSER_ID
from openerp import http
from openerp.tools.translate import _
from openerp.http import request

from openerp.addons.website.models.website import slug

import logging
_logger = logging.getLogger(__name__)


class website_hr_recruitment_bahia(http.Controller):
    @http.route([
        '/jobs',
        '/jobs/country/<model("res.country"):country>',
        '/jobs/department/<model("hr.department"):department>',
        '/jobs/country/<model("res.country"):country>/department/<model("hr.department"):department>',
        '/jobs/office/<int:office_id>',
        '/jobs/country/<model("res.country"):country>/office/<int:office_id>',
        '/jobs/department/<model("hr.department"):department>/office/<int:office_id>',
        '/jobs/country/<model("res.country"):country>/department/<model("hr.department"):department>/office/<int:office_id>',
    ], type='http', auth="public", website=True)
    def jobs(self, country=None, department=None, office_id=None, **kwargs):
        env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))

        Country = env['res.country']
        Jobs = env['hr.job']

        # List jobs available to current UID
        job_ids = Jobs.search([], order="website_published desc,no_of_recruitment desc").ids
        country_id = Country.search([]).ids
        # Browse jobs as superuser, because address is restricted
        jobs = Jobs.sudo().browse(job_ids)
        country_all = Country.sudo().browse(country_id)

        # Deduce departments and offices of those jobs
        departments = set(j.department_id for j in jobs if j.department_id)
        offices = set(j.address_id for j in jobs if j.address_id)
        countries = set(o.country_id for o in offices if o.country_id)



        #added to get only the internal (Bahia) Job Positions
        model_res_partner = env['res.partner'].sudo().search([('name','=', 'OFFICE PERSONNEL/S')], limit=1)
        model_jobs_bahia =  Jobs.sudo().search([('address_id', '=', model_res_partner.id), ('website_published', '=', True)], order="website_published desc,no_of_recruitment desc")


        model_principal = env['res.partner'].sudo().search([('is_company','=', 1),('customer','=', 1)])



        # Default search by user country
        if not (country or department or office_id or kwargs.get('all_countries')):
            country_code = request.session['geoip'].get('country_code')
            if country_code:
                countries_ = Country.search([('code', '=', country_code)])
                country = countries_[0] if countries_ else None
                if not any(j for j in jobs if j.address_id and j.address_id.country_id == country):
                    country = False

        # Filter the matching one
        if country and not kwargs.get('all_countries'):
            jobs = (j for j in jobs if j.address_id is None or j.address_id.country_id and j.address_id.country_id.id == country.id)
        if department:
            jobs = (j for j in jobs if j.department_id and j.department_id.id == department.id)
        if office_id:
            jobs = (j for j in jobs if j.address_id and j.address_id.id == office_id)

        # Render page
        return request.website.render("website_hr_recruitment_bahia.index", {
            'jobs': jobs,
            'jobs_bahia': model_jobs_bahia,
            'principals' : model_principal,
            'countries': countries,
            'departments': departments,
            'offices': offices,
            'country_id': country,
            'country_all':country_all,
            'department_id': department,
            'office_id': office_id,
        })

    @http.route('/jobs/add', type='http', auth="user", website=True)
    def jobs_add(self, **kwargs):
        job = request.env['hr.job'].create({
            'name': _('New Job Offer'),
        })
        return request.redirect("/jobs/detail/%s?enable_editor=1" % slug(job))

    @http.route('/jobs/detail/<model("hr.job"):job>', type='http', auth="public", website=True)
    def jobs_detail(self, job, **kwargs):
        return request.render("website_hr_recruitment_bahia.detail", {
            'job': job,
            'main_object': job,
        })

    @http.route(['/jobs/updateApplication'], type='json', auth="public", methods=['POST'], website=True)
    def updateApplication(self, 
                        new_applicant_id, 
                        first_name,
                        job_applied_id,
                        nationality_id,
                        last_name,
                        maiden_name,
                        date_of_birth,
                        place_of_birth,
                        height,
                        weight,
                        preferred_nickname,
                        shoe_size,
                        email_address,
                        contact_number,
                        sss_no,
                        philhealth_no,
                        pagibig_no,
                        civil_status,
                        gender,
                        permanent_address_adress,
                        permanent_address_city,
                        permanent_address_zipcode,
                        permanent_address_contact_no,
                        alternative_address_adress,
                        alternative_address_city,
                        alternative_address_zipcode,
                        alternative_address_contact_no,
                        emergency_person_name,
                        emergency_relationship,
                        emergency_address,
                        emergency_zipcode,
                        emergency_contactno,
                        image,
                        ):
        error = {}
        default = {}




        application_obj = http.request.env['website.recruitment.application'].search([('id', 
                                                                                '=', 
                                                                                int(new_applicant_id))])

        #raise Warning(image)

        image_value = False
        if not image:
            if application_obj.image:
                image_value = application_obj.image
        else:
            image_value = base64.encodestring(image)

        int_applied_id = False
        int_nationality_id = False
        if job_applied_id:
            int_applied_id = int(job_applied_id)

        if nationality_id:
            int_nationality_id = int(nationality_id)


        res = application_obj.write({
                                    'first_name':first_name or False,
                                    'job_applied_id': int_applied_id,
                                    'nationality_id': int_nationality_id,
                                    'last_name':last_name or False,
                                    'maiden_name':maiden_name or False,
                                    'date_of_birth':date_of_birth or False,
                                    'place_of_birth':place_of_birth or False,
                                    'height':height or False,
                                    'weight':weight or False,
                                    'preferred_nickname':preferred_nickname or False,
                                    'shoe_size':shoe_size or False,
                                    'email_address':email_address or False,
                                    'contact_number':contact_number or False,
                                    'sss_no':sss_no or False,
                                    'philhealth_no':philhealth_no or False,
                                    'pagibig_no':pagibig_no or False,
                                    'civil_status':civil_status or False,
                                    'gender':gender or False,
                                    'permanent_address_adress':permanent_address_adress or False,
                                    'permanent_address_city':permanent_address_city or False,
                                    'permanent_address_zipcode':permanent_address_zipcode or False,
                                    'permanent_address_contact_no':permanent_address_contact_no or False,
                                    'alternative_address_adress':alternative_address_adress or False,
                                    'alternative_address_city':alternative_address_city or False,
                                    'alternative_address_zipcode':alternative_address_zipcode or False,
                                    'alternative_address_contact_no':alternative_address_contact_no or False,
                                    'emergency_person_name':emergency_person_name or False,
                                    'emergency_relationship':emergency_relationship or False,
                                    'emergency_address':emergency_address or False,
                                    'emergency_zipcode':emergency_zipcode or False,
                                    'emergency_contactno':emergency_contactno or False,
                                    'image': image
                                    })
        return { 'Validate': True}



    @http.route(['/jobs/updateApplication2'], type='json', auth="public", methods=['POST'], website=True)
    def updateApplication2(self, 
                        new_applicant_id, 
                        denied_visa,
                        deported,
                        ):
        error = {}
        default = {}



        application_obj = http.request.env['website.recruitment.application'].search([('id', 
                                                                                '=', 
                                                                                int(new_applicant_id))])

        is_denied_visa = False
        is_deported = False

        if denied_visa == 'yes':
            is_denied_visa = True
        if is_deported == 'yes':
            is_deported = True

        res = application_obj.write({
                                    'is_denied_visa': is_denied_visa,
                                    'is_deported': is_deported,})
        return { 'Validate': True}


    @http.route(['/jobs/updateApplication3'], type='json', auth="public", methods=['POST'], website=True)
    def updateApplication3(self, 
                        new_applicant_id, 
                        is_medical_reason_1,
                        is_medical_operation,
                        has_hypertension,
                        has_diabetes,
                        has_hepatitis_a_b,
                        has_asthma,
                        is_smoker,
                        reference_1_company_name,
                        reference_1_name_person,
                        reference_1_address,
                        reference_1_contact_no,
                        reference_2_company_name,
                        reference_2_name_person,
                        reference_2_address,
                        reference_2_contact_no,
                        has_relative_employee,
                        has_applied_previously,):
        error = {}
        default = {}

        application_obj = http.request.env['website.recruitment.application'].search([('id', 
                                                                                '=', 
                                                                                int(new_applicant_id))])


        is_with_medical_reason_1 = False
        is_with_medical_operation = False
        has_with_hypertension = False
        has_with_diabetes = False
        has_with_hepatitis_a_b = False
        has_with_asthma = False
        is_with_smoker =False
        has_with_relative_employee = False
        has_with_applied_previously = False

        if is_medical_reason_1 == 'yes':
            is_with_medical_reason_1 = True
        if is_medical_operation == 'yes':
            is_with_medical_operation = True

        if has_hypertension == 'yes':
            has_with_hypertension = True
        if has_diabetes == 'yes':
            has_with_diabetes = True

        if has_hepatitis_a_b == 'yes':
            has_with_hepatitis_a_b = True
        if has_asthma == 'yes':
            has_with_asthma = True            

        if is_smoker == 'yes':
            is_with_smoker = True

        if has_relative_employee == 'yes':
            has_with_relative_employee = True

        if has_applied_previously == 'yes':
            has_with_applied_previously = True

        res = application_obj.write({
                                    'is_medical_reason_1': is_with_medical_reason_1,
                                    'is_medical_operation': is_with_medical_operation,
                                    'has_hypertension':has_with_hypertension,
                                    'has_diabetes':has_with_diabetes,
                                    'has_hepatitis_a_b':has_with_hepatitis_a_b,
                                    'has_asthma':has_with_asthma,
                                    'is_smoker':is_with_smoker,
                                    'has_relative_employee':has_with_relative_employee,
                                    'reference_1_company_name': reference_1_company_name or False,
                                    'reference_1_name_person': reference_1_name_person or False,
                                    'reference_1_address': reference_1_address or False,
                                    'reference_1_contact_no' : reference_1_contact_no or False,
                                    'reference_2_company_name': reference_2_company_name or False,
                                    'reference_2_name_person': reference_2_name_person or False,
                                    'reference_2_address': reference_2_address or False,
                                    'reference_2_contact_no' : reference_2_contact_no or False,
                                    'has_relative_employee': has_with_relative_employee,
                                    'has_applied_previously': has_with_applied_previously                            
                                    })

        return { 'Validate': True}



    @http.route('/jobs/start_apply', type='http', auth="public", website=True)
    def start_apply(self):

        error = {}
        default = {}
        value = {}
        env = request.env(user=SUPERUSER_ID)
        #SAMPLE
        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        value['name'] = 'Applicant'
        value['accept_privacy_policy'] = True
        applicant = env['website.recruitment.application'].sudo().create(value)

        relations_list = ['Father','Mother','Spouse']

        #Create Family Details
        family_relation_obj = http.request.env['hr.familyrelations'].sudo().search([('name',
                                                                                    'in',
                                                                                    relations_list)])

        family_detail_obj = http.request.env['website.recruitment.application.family_details'].sudo()
        for family_relation in family_relation_obj.sorted(key = lambda r: r.name):
            res = family_detail_obj.create({
                    'applicant_family_relationship_id' : applicant.id,
                    'relationship': family_relation.id,
                    'allow_delete': False,
                })

        relations_list = ['Child']
        family_relation_obj = http.request.env['hr.familyrelations'].sudo().search([('name',
                                                                                    'in',
                                                                                    relations_list)])

        family_detail_obj = http.request.env['website.recruitment.application.family_details'].sudo()
        for family_relation in family_relation_obj:
            res = family_detail_obj.create({
                    'applicant_family_relationship_id' : applicant.id,
                    'relationship': family_relation.id,
                    'allow_delete': False,

                })

        #Create Documents
        applicant_document_bac_obj = http.request.env['website.recruitment.application.documents'].sudo()
        document_list = ['Phil Passport','Phil Seamansbook','SRC', 'US VISA']
        document_obj = http.request.env['hr.documenttype'].sudo().search([('name',
                                                                            'in',
                                                                            document_list)])

        for document in document_obj.sorted(key = lambda r: r.name):
            res = applicant_document_bac_obj.create({
                    'applicant_documents_id' : applicant.id,
                    'document': document.id,
                    'allow_delete': False,
                })



        return request.redirect("/jobs/apply_all/%s"  % slug(applicant))
        #return request.render("website_hr_recruitment_bahia.start_apply", {})


    @http.route('/jobs/start_privacy_policy', type='http', auth="public", website=True)
    def jobs_start_privacy_policy(self):
        error = {}
        default = {}

        model_jobs = http.request.env['hr.job'].sudo().search([])

        str_url =""


        error = {}
        default = {}
        value = {}
        env = request.env(user=SUPERUSER_ID)
        #SAMPLE
        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        return request.render("website_hr_recruitment_bahia.apply_privacy_policy", {
            'error': error,
            'default': default,
            'jobs':model_jobs,
            'with_jobs': 0,
            })                   
        
    @http.route('/jobs/start_privacy_policy/<model("hr.job"):job>', type='http', auth="public", website=True)
    def jobs_start_privacy_policy_with_jobs(self, job):
        error = {}
        default = {}

        model_jobs = http.request.env['hr.job'].sudo().search([])

        str_url =""


        error = {}
        default = {}
        value = {}
        env = request.env(user=SUPERUSER_ID)
        #SAMPLE
        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        return request.render("website_hr_recruitment_bahia.apply_privacy_policy", {
            'error': error,
            'default': default,
            'jobs':model_jobs,
            'job_view': job,
            'with_jobs': 1.
            })

    @http.route('/jobs/start_apply/<model("hr.job"):job>', type='http', auth="public", website=True)
    def jobs_start_apply_with_job(self, job):
        error = {}
        default = {}

        model_jobs = http.request.env['hr.job'].sudo().search([])

        str_url =""


        error = {}
        default = {}
        value = {}
        env = request.env(user=SUPERUSER_ID)
        #SAMPLE
        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        value['name'] = 'Applicant'
        applicant = env['website.recruitment.application'].sudo().create(value)
        return request.redirect("/jobs/apply_all/%s/jobs/%s"  % (slug(applicant), slug(job)))
        #return request.render("website_hr_recruitment_bahia.start_apply", {})



    @http.route('/jobs/apply_all/<model("website.recruitment.application"):applicant>', type='http', auth="public", website=True)
    def jobs_apply_all(self, applicant):
        error = {}
        default = {}
        #attachment = http.request.env['ir.attachment'].sudo().search([('name', '=', 'Application-Form-rev2.docx')])
        model_jobs = http.request.env['hr.job'].sudo().search([])
        country_all = http.request.env['res.country'].sudo().search([('id','<', 254)])
        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_all", {
            'applicant':applicant.sudo(),
            #'job': job,
            'error': error,
            'country_all':country_all,
            'default': default,
            'jobs':model_jobs,
        })           

    @http.route('/jobs/apply_all/<model("website.recruitment.application"):applicant>/jobs/<model("hr.job"):job>', type='http', auth="public", website=True)
    def jobs_apply_all_with_jobs(self, applicant, job):
        error = {}
        default = {}
        attachment = http.request.env['ir.attachment'].sudo().search([('name', '=', 'Application-Form-rev2.docx')])

        model_jobs = http.request.env['hr.job'].sudo().search([])
        country_all = http.request.env['res.country'].sudo().search([('id','<', 254)])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_all", {
            'applicant':applicant.sudo(),
            #'job': job,
            'error': error,
            'country_all':country_all,
            'default': default,
            'jobs':model_jobs,
            'job':job,
        })   



    @http.route('/jobs/apply_add_family_details/<int:new_applicant_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_add_family_details(self, new_applicant_id,update_only):
        error = {}
        default = {}
        relations_list = ['Father','Mother','Spouse','Child']

        relationship_obj = http.request.env['hr.familyrelations'].sudo().search([('name','not in',relations_list)])

        applicant_family_relation_obj = http.request.env['website.recruitment.application.family_details'].sudo().search([])

        applicant_family_relation_obj = http.request.env['website.recruitment.application.family_details'].sudo().search([('id', '=', new_applicant_id)])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_family_details", {
            'applicant':applicant_family_relation_obj,
            'new_applicant_id':new_applicant_id,
            'edit_files':0,
            'update_only':update_only,
            #'job': job,
            'error': error,
            'default': default,
            'relationships':relationship_obj,
        })   


    @http.route('/jobs/add_family_details_exectute', type='http', auth="public", website=True)
    def add_family_details_exectute(self,**post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('applicant_id'))])
        family_detail_obj = http.request.env['website.recruitment.application.family_details'].sudo()

        gender_val = False

        if post.get('gender') !='0':
            gender_val = post.get('gender')

        if int(post.get('edit_file') or 0) != 1:
            applicant_family_relation_obj = family_detail_obj
            res = applicant_family_relation_obj.create({
                    'applicant_family_relationship_id' : post.get('applicant_id'),
                    'relationship': int(post.get('relationships') or 0),
                    'full_name': post.get('last_name')  or ''+ ',' + post.get('first_name') or '' + post.get('middle_name') or '',
                    'last_name': post.get('last_name'),
                    'first_name': post.get('first_name'),
                    'middle_name': post.get('middle_name'),
                    'gender': gender_val,
                    'placeof_birth': post.get('placeof_birth'),
                    'date_of_birth': post.get('date_of_birth') or False,
                })
        else:
            applicant_family_relation_obj = family_detail_obj.search([('id','=',post.get('child_id'))])

            res = applicant_family_relation_obj.update({
                    'relationship': int(post.get('relationships') or 0),
                    'full_name': post.get('last_name')  or ''+ ',' + post.get('first_name') or '' + post.get('middle_name') or '',
                    'last_name': post.get('last_name'),
                    'first_name': post.get('first_name'),
                    'middle_name': post.get('middle_name'),
                    'gender': gender_val,
                    'placeof_birth': post.get('placeof_birth'),
                    'date_of_birth': post.get('date_of_birth') or False,
                })            


        if int(post.get('update_only') or 0) != 1:        
            return request.redirect("/jobs/apply_all/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_update/%s/1"  % post.get('applicant_id'))

        #return request.redirect("/jobs/apply_all/%s"  % slug(application_obj))   


    @http.route('/jobs/add_educ_back_details/<int:new_applicant_id>/<int:update_only>', type='http', auth="public", website=True)
    def add_educ_back_details(self, new_applicant_id,update_only):
        error = {}
        default = {}
        level_obj = http.request.env['hr.recruitment.degree'].sudo().search([])

        applicant_educ_bac_obj = http.request.env['website.recruitment.application.education'].sudo()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_educational_background", {
            'applicant':applicant_educ_bac_obj,
            'new_applicant_id':new_applicant_id,
            'schooltypes': level_obj,
            'edit_files':0,
            'update_only':update_only,
            #'job': job,
            'error': error,
            'default': default,
            'relationships':level_obj,
        })   

    @http.route('/jobs/add_educ_back_exectute', type='http', auth="public", website=True)
    def add_educ_back_exectute(self,**post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('applicant_id'))])
        applicant_educ_bac_obj = http.request.env['website.recruitment.application.education'].sudo()
        #raise Warning(post.get('new_applicant_id'))
        if int(post.get('edit_file') or 0) != 1:
            res = applicant_educ_bac_obj.create({
                    'applicant_education_id' : post.get('applicant_id'),
                    'schooltype': int(post.get('schooltypes') or 0),
                    'name_school': post.get('name_school'),
                    'date_from': post.get('date_from') or False,
                    'date_to': post.get('date_to') or False,
                    'school_address': post.get('school_address') or False,
                    'description': post.get('description') or False,
                })
        else:
            applicant_educ_bac_obj = http.request.env['website.recruitment.application.education'].sudo().search([('id',
                                                                                                                    '=',
                                                                                                                    post.get('child_id'))])

            res = applicant_educ_bac_obj.update({
                    'schooltype': int(post.get('schooltypes') or 0),
                    'name_school': post.get('name_school'),
                    'date_from': post.get('date_from') or False,
                    'date_to': post.get('date_to') or False,
                    'school_address': post.get('school_address') or False,
                    'description': post.get('description') or False,
                })            

        if int(post.get('update_only') or 0) != 1:        
            return request.redirect("/jobs/apply_all/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_update/%s/1"  % post.get('applicant_id'))

        #return request.redirect("/jobs/apply_all/%s"  % slug(application_obj))   

    @http.route('/jobs/apply_add_documents/<int:new_applicant_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_add_documents(self, new_applicant_id,update_only):
        error = {}
        default = {}
        doc_type_obj = http.request.env['hr.documenttype'].sudo().search([])

        applicant_document_obj = http.request.env['website.recruitment.application.documents'].sudo()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_documents", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'documents': doc_type_obj,
            'update_only': update_only or 0,
            #'job': job,
            'error': error,
            'default': default,
        })   


    @http.route('/jobs/add_documents_exectute', type='http', auth="public", website=True)
    def add_documents_exectute(self,**post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('applicant_id'))])
        applicant_document_bac_obj = http.request.env['website.recruitment.application.documents'].sudo()

        if int(post.get('edit_file') or 0) != 1:
            res = applicant_document_bac_obj.create({
                    'applicant_documents_id' : post.get('applicant_id'),
                    'document': int(post.get('documents') or 0),
                    'document_number': post.get('document_number'),
                    'date_issued': post.get('date_issued') or False,
                    'date_expiry': post.get('date_expiry')  or False,
                    'issuing_authority': post.get('issuing_authority')  or False,
                })
        else:
            applicant_document_bac_obj = http.request.env['website.recruitment.application.documents'].sudo().search([('id','=',
                                                                                                                        post.get('child_id'))])
            res = applicant_document_bac_obj.update({
                    'document': int(post.get('documents') or 0),
                    'document_number': post.get('document_number'),
                    'date_issued': post.get('date_issued') or False,
                    'date_expiry': post.get('date_expiry')  or False,
                    'issuing_authority': post.get('issuing_authority')  or False,
                })
        if int(post.get('update_only') or 0) != 1:        
            return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_2_update/%s/1"  % post.get('applicant_id'))

    @http.route('/jobs/jobs_apply_add_family_details_exectute', type='http', auth="public", website=True)
    def jobs_apply_add_family_details_exectute(self,**post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('new_applicant_id'))])
        return request.redirect("/jobs/apply_add_family_details/%s"  % slug(application_obj))        


    @http.route('/jobs/apply_add_denied_visa/<int:new_applicant_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_add_denied_visa(self, new_applicant_id,update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.denied.visa'].sudo()
        country_all = http.request.env['res.country'].sudo().search([])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_denied_visa", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'nationality_ids': country_all,
            'update_only': update_only,
            #'job': job,
            'error': error,
            'default': default,
        })   


    @http.route('/jobs/add_denied_visa_execute', type='http', auth="public", website=True)
    def add_denied_visa_execute(self,**post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('applicant_id'))])
        applicant_document_bac_obj = http.request.env['website.recruitment.denied.visa'].sudo()
        if int(post.get('edit_file') or 0) != 1:
            res = applicant_document_bac_obj.create({
                    'applicant_id' : post.get('applicant_id'),
                    'nationality_id': int(post.get('nationality_id') or 0),
                    'date_denied': post.get('date_denied'),
                    'reason': post.get('reason'),
                })
        else:
            applicant_document_bac_obj = http.request.env['website.recruitment.denied.visa'].sudo().search([('id','=',
                                                                                                             post.get('child_id'))])
            res = applicant_document_bac_obj.update({
                    'nationality_id': int(post.get('nationality_id') or 0),
                    'date_denied': post.get('date_denied') or False,
                    'reason': post.get('reason'),
                })            

        if int(post.get('update_only') or 0) != 1:        
            return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_2_update/%s/1"  % post.get('applicant_id'))

    @http.route('/jobs/apply_add_deported/<int:new_applicant_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_add_deported(self, new_applicant_id, update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.deported'].sudo()
        country_all = http.request.env['res.country'].sudo().search([])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_deported", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'nationality_ids': country_all,
            'update_only': update_only,
            'error': error,
            'default': default,
        })

    @http.route('/jobs/add_deported_execute', type='http', auth="public", website=True)
    def add_add_deported_execute(self,**post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('applicant_id'))])
        applicant_document_bac_obj = http.request.env['website.recruitment.deported'].sudo()
        if int(post.get('edit_file') or 0) != 1:
            res = applicant_document_bac_obj.create({
                    'applicant_id' : post.get('applicant_id'),
                    'nationality_id': int(post.get('nationality_id') or 0),
                    'date_deported': post.get('date_deported'),
                    'reason': post.get('reason'),
                })
        else:
            applicant_document_bac_obj = http.request.env['website.recruitment.deported'].sudo().search([('id','=',
                                                                                                             post.get('child_id'))])
            res = applicant_document_bac_obj.update({
                    'nationality_id': int(post.get('nationality_id') or 0),
                    'date_deported': post.get('date_deported'),
                    'reason': post.get('reason'),
                })            

        if int(post.get('update_only') or 0) != 1:        
            return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_2_update/%s/1"  % post.get('applicant_id'))

    @http.route('/jobs/apply_add_training_courses/<int:new_applicant_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_add_training_courses(self, new_applicant_id,update_only):
        error = {}
        default = {}

        applicant_license_type = http.request.env['hr.licensetype'].sudo().search([('name','=','Training')])

        applicant_license = http.request.env['hr.license'].sudo().search([('license_name', '=', applicant_license_type.id)])        

        applicant_document_obj = http.request.env['website.recruitment.training.courses'].sudo()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_training_courses", {
            'trainings': applicant_license,
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'update_only':update_only,
            'error': error,
            'default': default,
        }) 

    @http.route('/jobs/add_training_execute', type='http', auth="public", website=True)
    def add_training_execute(self,**post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('applicant_id'))])
        applicant_document_bac_obj = http.request.env['website.recruitment.training.courses'].sudo()

        bln_cop = False
        if post.get('is_with_cop') == 'yes':
            bln_cop = True

        training_id = False

        if int(post.get('training_id')) not in [0,99999]:
            training_id = int(post.get('training_id'))


        if int(post.get('edit_file') or 0) != 1:
            res = applicant_document_bac_obj.create({
                    'applicant_id' : post.get('applicant_id'),
                    'training_name': post.get('training_name'),
                    'document_no': post.get('document_no'),
                    'issue_date': post.get('issue_date') or False,
                    'training_centers': post.get('training_centers'),
                    'is_with_cop': bln_cop,
                    'issue_date_cop': post.get('issue_date_cop') or False,
                    'training_id': training_id,
                })
        else:
            applicant_document_bac_obj = http.request.env['website.recruitment.training.courses'].sudo().search([('id','=',
                                                                                                                  post.get('child_id'))])
            res = applicant_document_bac_obj.update({
                    'training_name': post.get('training_name'),
                    'document_no': post.get('document_no'),
                    'issue_date': post.get('issue_date') or False,
                    'training_centers': post.get('training_centers'),
                    'is_with_cop': bln_cop,
                    'issue_date_cop': post.get('issue_date_cop') or False,
                    'training_id': training_id,
                })            


        if int(post.get('update_only') or 0) != 1:        
            return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_2_update/%s/1"  % post.get('applicant_id'))

    @http.route('/jobs/apply_add_license/<int:new_applicant_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_add_license(self, new_applicant_id,update_only):
        error = {}
        default = {}

        applicant_license_type = http.request.env['hr.licensetype'].sudo().search([('name','=','License')])

        applicant_license = http.request.env['hr.license'].sudo().search([('license_name', '=', applicant_license_type.id)])        

        applicant_document_obj = http.request.env['website.recruitment.license'].sudo()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_license", {
            'trainings':applicant_license,
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'error': error,
            'update_only':update_only,
            'default': default,
        }) 
    
    @http.route('/jobs/add_license_execute', type='http', auth="public", website=True)
    def add_license_execute(self, **post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('applicant_id'))])
        applicant_document_bac_obj = http.request.env['website.recruitment.license'].sudo()

        license_id = False

        if int(post.get('license_id')) not in [0,99999]:
            license_id = int(post.get('license_id'))        

        if int(post.get('edit_file') or 0) != 1:
            res = applicant_document_bac_obj.create({
                    'applicant_id' : post.get('applicant_id'),
                    'training_name': post.get('training_name'),
                    'document_no': post.get('document_no'),
                    'issue_date': post.get('issue_date') or False,
                    'expiry_date': post.get('expiry_date') or False,
                    'issuing_authority': post.get('issuing_authority') or False,
                    'issuing_authority_other': post.get('issuing_authority_other') or False,
                    'license_id': license_id,
                })
        else:
            applicant_document_bac_obj = http.request.env['website.recruitment.license'].sudo().search([('id','=',
                                                                                                        post.get('child_id'))])
            res = applicant_document_bac_obj.update({
                    'training_name': post.get('training_name'),
                    'document_no': post.get('document_no'),
                    'issue_date': post.get('issue_date')  or False,
                    'expiry_date': post.get('expiry_date') or False,
                    'issuing_authority': post.get('issuing_authority') or False,
                    'issuing_authority_other': post.get('issuing_authority_other') or False,
                    'license_id': license_id,
                })            

        if int(post.get('update_only') or 0) != 1:        
            return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_2_update/%s/1"  % post.get('applicant_id'))


    @http.route('/jobs/apply_add_medical_history/<int:new_applicant_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_add_medical_history(self, new_applicant_id,update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.medical.history'].sudo()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_medical_history", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'update_only':update_only,
            'error': error,
            'default': default,
        }) 

    @http.route('/jobs/add_medical_history_execute', type='http', auth="public", website=True)
    def add_medical_history_execute(self, **post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('applicant_id'))])
        applicant_document_bac_obj = http.request.env['website.recruitment.medical.history'].sudo()

        if int(post.get('edit_file') or 0) != 1:
            res = applicant_document_bac_obj.create({
                    'applicant_id' : post.get('applicant_id'),
                    'vessel_name': post.get('vessel_name'),
                    'occurence_place': post.get('occurence_place'),
                    'occurence_date': post.get('occurence_date') or False,
                    'description': post.get('description'),
                })
        else:
            applicant_document_bac_obj = http.request.env['website.recruitment.medical.history'].sudo().search([('id','=',
                                                                                                                  post.get('child_id'))])
            res = applicant_document_bac_obj.update({
                    'vessel_name': post.get('vessel_name'),
                    'occurence_place': post.get('occurence_place'),
                    'occurence_date': post.get('occurence_date') or False,
                    'description': post.get('description'),
                })            

        if int(post.get('update_only') or 0) != 1:        
            return request.redirect("/jobs/apply_all_3/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_3_update/%s/1"  % post.get('applicant_id'))

        #return request.redirect("/jobs/apply_all_3/%s"  % slug(application_obj))


    @http.route('/jobs/apply_add_medical_operation/<int:new_applicant_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_add_medical_operation(self, new_applicant_id,update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.medical.operation'].sudo()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_medical_operation", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'update_only':update_only,
            'error': error,
            'default': default,
        }) 

    @http.route('/jobs/add_medical_operation_execute', type='http', auth="public", website=True)
    def add_medical_operation_execute(self, **post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('applicant_id'))])
        applicant_document_bac_obj = http.request.env['website.recruitment.medical.operation'].sudo()


        if int(post.get('edit_file') or 0) != 1:
            res = applicant_document_bac_obj.create({
                    'applicant_id' : post.get('applicant_id'),
                    'details_of_operation': post.get('details_of_operation'),
                    'date_of_operation': post.get('date_of_operation') or False,
                    'period_of_disability': post.get('period_of_disability'),
                    'description': post.get('description'),
                })
        else:
            applicant_document_bac_obj = http.request.env['website.recruitment.medical.operation'].sudo().search([('id','=',post.get('child_id'))])
            res = applicant_document_bac_obj.update({
                    'details_of_operation': post.get('details_of_operation'),
                    'date_of_operation': post.get('date_of_operation') or False,
                    'period_of_disability': post.get('period_of_disability'),
                    'description': post.get('description'),
                })            

        if int(post.get('update_only') or 0) != 1:        
            return request.redirect("/jobs/apply_all_3/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_3_update/%s/1"  % post.get('applicant_id'))


    @http.route('/jobs/apply_apply_add_medical_illness/<int:new_applicant_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_add_medical_illness(self, new_applicant_id,update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.medical.illness'].sudo()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_medical_illness", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'update_only':update_only,
            'error': error,
            'default': default,
        }) 


    @http.route('/jobs/add_medical_illness_execute', type='http', auth="public", website=True)
    def add_medical_illness_execute(self, **post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('applicant_id'))])
        applicant_document_bac_obj = http.request.env['website.recruitment.medical.illness'].sudo()

        if int(post.get('edit_file') or 0) != 1:
            res = applicant_document_bac_obj.create({
                    'applicant_id' : post.get('applicant_id'),
                    'details_of_illness_accident': post.get('details_of_illness_accident'),
                    'date_illness_accident': post.get('date_illness_accident') or False,
                    'therapy_treatment_description': post.get('therapy_treatment_description'),
                })
        else:
            applicant_document_bac_obj = http.request.env['website.recruitment.medical.illness'].sudo().search([('id','=',post.get('child_id'))])
            res = applicant_document_bac_obj.update({
                    'details_of_illness_accident': post.get('details_of_illness_accident'),
                    'date_illness_accident': post.get('date_illness_accident') or False,
                    'therapy_treatment_description': post.get('therapy_treatment_description'),
                })

        if int(post.get('update_only') or 0) != 1:        
            return request.redirect("/jobs/apply_all_3/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_3_update/%s/1"  % post.get('applicant_id'))

    @http.route('/jobs/apply_add_employee_relatives/<int:new_applicant_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_add_employee_relatives(self, new_applicant_id,update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.employee.relative'].sudo()
        relationship_obj = http.request.env['hr.familyrelations'].sudo().search([])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_employee_relatives", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'error': error,
            'update_only':update_only,
            'relationships':relationship_obj,
            'default': default,
        }) 

    @http.route('/jobs/add_employee_relatives_execute', type='http', auth="public", website=True)
    def add_employee_relatives_execute(self, **post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('applicant_id'))])
        applicant_document_bac_obj = http.request.env['website.recruitment.employee.relative'].sudo()

        if int(post.get('edit_file') or 0) != 1:
            res = applicant_document_bac_obj.create({
                    'applicant_id' : post.get('applicant_id'),
                    'name_of_crew': post.get('name_of_crew'),
                    'position_and_principal': post.get('position_and_principal'),
                    'relationship': int(post.get('relationships') or 0),
                })
        else:
            applicant_document_bac_obj = http.request.env['website.recruitment.employee.relative'].sudo().search([('id','=',post.get('child_id'))])
            res = applicant_document_bac_obj.update({
                    'name_of_crew': post.get('name_of_crew'),
                    'position_and_principal': post.get('position_and_principal'),
                    'relationship': int(post.get('relationships') or 0),
                })            

        if int(post.get('update_only') or 0) != 1:        
            return request.redirect("/jobs/apply_all_3/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_3_update/%s/1"  % post.get('applicant_id'))

    @http.route('/jobs/apply_add_previous_application/<int:new_applicant_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_add_previous_application(self, new_applicant_id,update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.previous.application'].sudo()
        model_jobs = http.request.env['hr.job'].sudo().search([])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_previous_application", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'error': error,
            'update_only':update_only,
            'default': default,
            'jobs': model_jobs,
        }) 

    @http.route('/jobs/add_previous_application_execute', type='http', auth="public", website=True)
    def add_previous_application_execute(self, **post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('applicant_id'))])
        applicant_document_bac_obj = http.request.env['website.recruitment.previous.application'].sudo()

        if int(post.get('edit_file') or 0) != 1:
            res = applicant_document_bac_obj.create({
                    'applicant_id' : post.get('applicant_id'),
                    'date_applied': post.get('date_applied') or False,
                    'job_applied_id': int(post.get('job_applied_id') or 0),
                })
        else:
            applicant_document_bac_obj = http.request.env['website.recruitment.previous.application'].sudo().search([('id','=',post.get('child_id'))])
            res = applicant_document_bac_obj.update({
                    'date_applied': post.get('date_applied') or False,
                    'job_applied_id': int(post.get('job_applied_id') or 0),
                })            

        if int(post.get('update_only') or 0) != 1:        
            return request.redirect("/jobs/apply_all_3/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_3_update/%s/1"  % post.get('applicant_id'))


    @http.route('/jobs/apply_add_employment_history/<int:new_applicant_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_add_employment_history(self, new_applicant_id,update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.previous.employment'].sudo()
        model_jobs = http.request.env['hr.job'].sudo().search([])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_employment_history", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'error': error,
            'update_only':update_only,
            'default': default,
            'jobs': model_jobs,
        })

    @http.route('/jobs/add_employment_history_execute', type='http', auth="public", website=True)
    def add_employment_history_execute(self, **post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('applicant_id'))])
        applicant_document_bac_obj = http.request.env['website.recruitment.previous.employment'].sudo()
        #raise Warning(post.get('vessel_type'))

        if int(post.get('edit_file') or 0) != 1:
            res = applicant_document_bac_obj.create({
                    'applicant_id' : post.get('applicant_id'),
                    'rank_position': post.get('rank_position'),
                    'manning_agency': post.get('manning_agency'),
                    'employer_principal': post.get('employer_principal'),
                    'address_contact_info_manning_agen': post.get('address_contact_info_manning_agen'),
                    'vessel_name': post.get('vessel_name'),
                    'grt': post.get('grt'),
                    'vessel_type': post.get('vessel_type'),
                    'date_from': post.get('date_from') or False,
                    'date_to': post.get('date_to') or False,
                    'duties_and_responsibility': post.get('duties_and_responsibility'),
                })
        else:
            applicant_document_bac_obj = http.request.env['website.recruitment.previous.employment'].sudo().search([('id','=',post.get('child_id'))])
            res = applicant_document_bac_obj.update({
                    'rank_position': post.get('rank_position'),
                    'manning_agency': post.get('manning_agency'),
                    'employer_principal': post.get('employer_principal'),
                    'address_contact_info_manning_agen': post.get('address_contact_info_manning_agen'),
                    'vessel_name': post.get('vessel_name'),
                    'grt': post.get('grt'),
                    'vessel_type': post.get('vessel_type'),
                    'date_from': post.get('date_from') or False,
                    'date_to': post.get('date_to') or False,
                    'duties_and_responsibility': post.get('duties_and_responsibility'),
                })

        if int(post.get('update_only') or 0) != 1:        
            return request.redirect("/jobs/apply_all_4/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_4_update/%s/1"  % post.get('applicant_id'))

        #return request.redirect("/jobs/apply_all_4/%s"  % slug(application_obj))  

    #2->1
    @http.route('/jobs/apply_all_back_execute', methods=['POST'], type='http', auth="public", website=True)
    def apply_all_back_execute(self,**post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('new_applicant_id'))])
        return request.redirect("/jobs/apply_all/%s"  % slug(application_obj))
    #3->2
    @http.route('/jobs/apply_all_2_back_execute', methods=['POST'], type='http', auth="public", website=True)
    def apply_all_2_back_execute(self,**post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('new_applicant_id'))])
        return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))

    #4->3
    @http.route('/jobs/apply_all_3_back_execute', methods=['POST'], type='http', auth="public", website=True)
    def apply_all_3_back_execute(self,**post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('new_applicant_id'))])
        return request.redirect("/jobs/apply_all_3/%s"  % slug(application_obj))


    #Final Form
    @http.route('/jobs/apply_all_4_back_execute', methods=['POST'], type='http', auth="public", website=True)
    def apply_all_4_back_execute(self,**post):
        error = {}
        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('new_applicant_id'))])
        return request.redirect("/jobs/apply_all_3/%s"  % slug(application_obj))

    @http.route('/jobs/apply_all_2_execute', methods=['POST'], type='http', auth="public", website=True)
    def apply_all_2_execute(self,**post):
        error = {}
        env = request.env(user=SUPERUSER_ID)
        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('new_applicant_id'))])

        image_value = False
        if not post['image_applicant']:
            if application_obj.image:
                image_value = application_obj.image
        else:
            image_value = base64.encodestring(post['image_applicant'].read())


        res = application_obj.write({
                                    'job_applied_id': int(post.get('job_id') or 0),
                                    'nationality_id': int(post.get('country_id') or 0),                                    
                                    'first_name':post.get('first_name'),
                                    'last_name':post.get('last_name'),
                                    'maiden_name':post.get('maiden_name'),
                                    'date_of_birth':post.get('date_of_birth'),
                                    'place_of_birth':post.get('place_of_birth'),
                                    'height':post.get('height'),
                                    'weight':post.get('weight'),
                                    'preferred_nickname':post.get('preferred_nickname'),
                                    'shoe_size':post.get('shoe_size'),
                                    'email_address':post.get('email_from'),
                                    'contact_number':post.get('phone'),
                                    'sss_no':post.get('sss_no'),
                                    'philhealth_no':post.get('philhealth_no'),
                                    'pagibig_no':post.get('pagibig_no'),
                                    'civil_status':post.get('civil_status'),
                                    'gender':post.get('gender'),
                                    'permanent_address_adress':post.get('address_1'),
                                    'permanent_address_city':post.get('city_address_1'),
                                    'permanent_address_zipcode':post.get('zipcode_address_1'),
                                    'permanent_address_contact_no':post.get('contact_address_1'),
                                    'alternative_address_adress':post.get('address_2'),
                                    'alternative_address_city':post.get('city_address_2'),
                                    'alternative_address_zipcode':post.get('zipcode_address_2'),
                                    'alternative_address_contact_no':post.get('contact_address_2'),
                                    'emergency_person_name':post.get('emergency_person_name'),
                                    'emergency_relationship':post.get('emergency_relationship'),
                                    'emergency_address':post.get('emergency_address'),
                                    'emergency_zipcode':post.get('emergency_zipcode'),
                                    'emergency_contactno':post.get('emergency_contactno'),
                                    'image': image_value
                                    })

        #Check Image
        image_error = 1
        #raise Warning(application_obj.image)
        if post['image_applicant'] or application_obj.image:
            if len(post['image_applicant'].filename) > 0 or application_obj.image:
                image_error = 0        

        #Check the Default Family Details
        family_detail_model = env['website.recruitment.application.family_details'].sudo()
        #Create Family Details
        father_id = family_detail_model.getRelationIDByName('Father')
        mother_id = family_detail_model.getRelationIDByName('Mother')

        notify_error_father = 0
        notify_error_mother = 0
        #SDS
        # Remove Notification on Requiring the Mother and Father Relation.

        #Check if Father Has Value
        #family_detail_obj = family_detail_model.search([('applicant_family_relationship_id','=',int(post.get('new_applicant_id'))),
        #                                                ('relationship','=',father_id)])

        #if family_detail_obj:
        #    if family_detail_obj.full_name and family_detail_obj.date_of_birth:
        #        notify_error_father = 0


        #Check if Mother Has Value
        #family_detail_obj = family_detail_model.search([('applicant_family_relationship_id','=',int(post.get('new_applicant_id'))),
        #                                                ('relationship','=',mother_id)])

        #if family_detail_obj:
        #    if family_detail_obj.full_name and family_detail_obj.date_of_birth:
        #        notify_error_mother = 0


        #Check Educational Background
        notify_error_educ_back = 1
        applicant_educ_bac_model = env['website.recruitment.application.education'].sudo()

        applicant_educ_bac_obj = applicant_educ_bac_model.search_count([('applicant_education_id',
                                                                         '=',
                                                                         int(post.get('new_applicant_id')))])

        if applicant_educ_bac_obj >= 1:
            notify_error_educ_back =0;



        if notify_error_mother == 1 or  notify_error_father == 1 or notify_error_educ_back == 1 or image_error == 1:
            model_jobs = http.request.env['hr.job'].sudo().search([])
            country_all = http.request.env['res.country'].sudo().search([])
            default ={}
            if 'website_hr_recruitment_bahia_error' in request.session:
                error = request.session.pop('website_hr_recruitment_bahia_error')
                default = request.session.pop('website_hr_recruitment_bahia_default')

            return request.render("website_hr_recruitment_bahia.apply_all", {
                'applicant':application_obj,
                #'job': job,
                'error': error,
                'country_all':country_all,
                'default': default,
                'jobs':model_jobs,
                'notify_error_mother': notify_error_mother,
                'notify_error_father': notify_error_father,
                'notify_error_educ_back':notify_error_educ_back,
                'image_error':image_error,                
            })

        else:
            if int(post.get('update_only') or 0) != 1:
                return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))        
            else:
                return request.redirect("/jobs/apply_all_summary/%s"  % slug(application_obj))

        #return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))

    @http.route('/jobs/apply_all_3_execute', methods=['POST'], type='http', auth="public", website=True)
    def apply_all_3_execute(self,**post):
        error = {}

        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('new_applicant_id'))])

        denied_visa = False
        deported = False

        if post.get('denied_visa') == 'yes':
            denied_visa = True
        if post.get('is_deported') == 'yes':
            deported = True

        res = application_obj.write({
                                    'is_denied_visa': denied_visa,
                                    'is_deported': deported,})


        passport_error_notify = 1
        #To Check if Passport Record has no Value
        document_detail_model = env['website.recruitment.application.documents'].sudo()
        passport_id = document_detail_model.getDocumentByName('Phil Passport')

        document_detail_obj = document_detail_model.search([('applicant_documents_id', '=',int(post.get('new_applicant_id'))),
                                                            ('document','=',passport_id)]) 

        if document_detail_obj:
            if (document_detail_obj.document_number and 
                document_detail_obj.date_issued and 
                document_detail_obj.issuing_authority and 
                document_detail_obj.date_expiry):
                passport_error_notify = 0

        if passport_error_notify == 1:
            model_jobs = http.request.env['hr.job'].sudo().search([])
            country_all = http.request.env['res.country'].sudo().search([])

            if 'website_hr_recruitment_bahia_error' in request.session:
                error = request.session.pop('website_hr_recruitment_bahia_error')
                default = request.session.pop('website_hr_recruitment_bahia_default')  
            return request.render("website_hr_recruitment_bahia.apply_all_2", 
                                 {'applicant':application_obj,
                                  'passport_error_notify': passport_error_notify,})


        else:
            if int(post.get('update_only') or 0) != 1:
                return request.redirect("/jobs/apply_all_3/%s"  % slug(application_obj))        
            else:
                return request.redirect("/jobs/apply_all_summary/%s"  % slug(application_obj))


    @http.route('/jobs/apply_all_4_execute', methods=['POST'], type='http', auth="public", website=True)
    def apply_all_4_execute(self,**post):
        error = {}

        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('new_applicant_id'))])

        is_medical_reason_1 = False
        is_medical_operation = False
        has_hypertension = False
        has_diabetes = False
        has_hepatitis_a_b = False
        has_asthma = False
        is_smoker =False
        has_relative_employee = False
        has_applied_previously = False

        if post.get('is_medical_reason_1') == 'yes':
            is_medical_reason_1 = True
        if post.get('is_medical_operation') == 'yes':
            is_medical_operation = True

        if post.get('has_hypertension') == 'yes':
            has_hypertension = True
        if post.get('has_diabetes') == 'yes':
            has_diabetes = True

        if post.get('has_hepatitis_a_b') == 'yes':
            has_hepatitis_a_b = True
        if post.get('has_asthma') == 'yes':
            has_asthma = True            


        if post.get('is_smoker') == 'yes':
            is_smoker = True


        if post.get('has_relative_employee') == 'yes':
            has_relative_employee = True

        if post.get('has_applied_previously') == 'yes':
            has_applied_previously = True           


        res = application_obj.write({
                                    'is_medical_reason_1': is_medical_reason_1,
                                    'is_medical_operation': is_medical_operation,
                                    'has_hypertension':has_hypertension,
                                    'has_diabetes':has_diabetes,
                                    'has_hepatitis_a_b':has_hepatitis_a_b,
                                    'has_asthma':has_asthma,
                                    'is_smoker':is_smoker,
                                    'has_relative_employee':has_relative_employee,
                                    'reference_1_company_name': post.get('reference_1_company_name') or False,
                                    'reference_1_name_person': post.get('reference_1_name_person') or False,
                                    'reference_1_address': post.get('reference_1_address') or False,
                                    'reference_1_contact_no' : post.get('reference_1_contact_no') or False,
                                    'reference_2_company_name': post.get('reference_2_company_name') or False,
                                    'reference_2_name_person': post.get('reference_2_name_person') or False,
                                    'reference_2_address': post.get('reference_2_address') or False,
                                    'reference_2_contact_no' : post.get('reference_2_contact_no') or False,
                                    'has_relative_employee': has_relative_employee,
                                    'has_applied_previously': has_applied_previously                            
                                    })        


        if int(post.get('update_only') or 0) != 1:
            return request.redirect("/jobs/apply_all_4/%s"  % slug(application_obj))
        else:
            return request.redirect("/jobs/apply_all_summary/%s"  % slug(application_obj))        

    @http.route('/jobs/apply_all_2/<model("website.recruitment.application"):applicant>',  type='http', auth="public", website=True)
    def jobs_apply_all_2(self,applicant):
        error = {}
        default = {}
        attachment = http.request.env['ir.attachment'].sudo().search([('name', '=', 'Application-Form-rev2.docx')])

        model_jobs = http.request.env['hr.job'].sudo().search([])
        country_all = http.request.env['res.country'].sudo().search([])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')  
        return request.render("website_hr_recruitment_bahia.apply_all_2", {'applicant':applicant.sudo()})   

#UPDATE UPON FINAL SUBMISSION FORM
    @http.route('/jobs/apply_all_update/<int:new_applicant_id>/<int:update_only>',  type='http', auth="public", website=True)
    def jobs_apply_all_update(self,new_applicant_id,update_only):
        error = {}
        default = {}

        model_jobs = http.request.env['hr.job'].sudo().search([])
        country_all = http.request.env['res.country'].sudo().search([])

        applicant_obj = http.request.env['website.recruitment.application'].sudo().search([('id', '=', new_applicant_id)])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')  
        return request.render("website_hr_recruitment_bahia.apply_all", 
            {
                'applicant':applicant_obj.sudo(),
                'update_only': update_only,
                'error': error,
                'country_all':country_all,
                'default': default,
                'jobs':model_jobs,                
            })   


    @http.route('/jobs/apply_all_2_update/<int:new_applicant_id>/<int:update_only>',  type='http', auth="public", website=True)
    def jobs_apply_all_2_update(self,new_applicant_id,update_only):
        error = {}
        default = {}

        model_jobs = http.request.env['hr.job'].sudo().search([])
        country_all = http.request.env['res.country'].sudo().search([])

        applicant_obj = http.request.env['website.recruitment.application'].sudo().search([('id', '=', new_applicant_id)])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')  
        return request.render("website_hr_recruitment_bahia.apply_all_2", 
            {
                'applicant':applicant_obj.sudo(),
                'update_only': update_only,
            })   


    @http.route('/jobs/apply_all_3_update/<int:new_applicant_id>/<int:update_only>',  type='http', auth="public", website=True)
    def jobs_apply_all_3_update(self,new_applicant_id,update_only):
        error = {}
        default = {}

        model_jobs = http.request.env['hr.job'].sudo().search([])
        country_all = http.request.env['res.country'].sudo().search([])

        applicant_obj = http.request.env['website.recruitment.application'].sudo().search([('id', '=', new_applicant_id)])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')  
        return request.render("website_hr_recruitment_bahia.apply_all_3", 
            {
                'applicant':applicant_obj.sudo(),
                'error': error,
                'update_only': update_only,
            })


    @http.route('/jobs/apply_all_4_update/<int:new_applicant_id>/<int:update_only>',  type='http', auth="public", website=True)
    def jobs_apply_all_4_update(self,new_applicant_id,update_only):
        error = {}
        default = {}

        model_jobs = http.request.env['hr.job'].sudo().search([])
        country_all = http.request.env['res.country'].sudo().search([])

        applicant_obj = http.request.env['website.recruitment.application'].sudo().search([('id', '=', new_applicant_id)])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')  
        return request.render("website_hr_recruitment_bahia.apply_all_4", 
            {
                'applicant':applicant_obj.sudo(),
                'update_only': update_only,
            })

    @http.route('/jobs/apply_all_3/<model("website.recruitment.application"):applicant>',  type='http', auth="public", website=True)
    def jobs_apply_all_3(self,applicant):
        error = {}
        default = {}
        attachment = http.request.env['ir.attachment'].sudo().search([('name', '=', 'Application-Form-rev2.docx')])

        model_jobs = http.request.env['hr.job'].sudo().search([])
        country_all = http.request.env['res.country'].sudo().search([])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        #return request.render("website_hr_recruitment_bahia.apply_all_2", {
            #'job': job,
        #    'error': error,
            #'country_all':country_all,
            #'default': default,
            #'jobs':model_jobs,
        #})   
        return request.render("website_hr_recruitment_bahia.apply_all_3", 
                              {'applicant':applicant.sudo(),
                                'error': error,
                              }
                            )   


    @http.route('/jobs/apply_all_4/<model("website.recruitment.application"):applicant>',  type='http', auth="public", website=True)
    def jobs_apply_all_4(self,applicant):
        error = {}
        default = {}
        attachment = http.request.env['ir.attachment'].sudo().search([('name', '=', 'Application-Form-rev2.docx')])

        model_jobs = http.request.env['hr.job'].sudo().search([])
        country_all = http.request.env['res.country'].sudo().search([])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_all_4", {'applicant':applicant.sudo()})   

    @http.route('/jobs/apply/<model("hr.job"):job>', type='http', auth="public", website=True)
    def jobs_apply(self, job):
        error = {}
        default = {}
        #Added by SDS 19022016
        attachment = http.request.env['ir.attachment'].sudo().search([('name', '=', 'Application-Form-rev2.docx')])

        model_jobs = http.request.env['hr.job'].sudo().search([])

        #str_url = 'http://localhost:8069'+'/web/binary/saveas?model=ir.attachment&field=datas&filename_field=name&id='+str(attachment.id)
        str_url =""
        #str_url = request.httprequest.host_url +'web/binary/saveas?model=ir.attachment&field=datas&filename_field=name&id='+str(attachment.id) +'&uid=1'
        #raise Warning(str_url)

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply", {
            'job': job,
            'error': error,
            'default': default,
            'jobs':model_jobs,
            'url_link': str_url,
        })


    @http.route('/jobs/apply_all_summary/<model("website.recruitment.application"):applicant>',  type='http', auth="public", website=True)
    def jobs_apply_all_summary(self,applicant):
        error = {}
        default = {}
        attachment = http.request.env['ir.attachment'].sudo().search([('name', '=', 'Application-Form-rev2.docx')])

        model_jobs = http.request.env['hr.job'].sudo().search([])
        country_all = http.request.env['res.country'].sudo().search([])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_all_summary", {'applicant':applicant.sudo()})   

#   DELETION OF RECORDS
    @http.route('/jobs/apply_delete_family_details/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_delete_family_details(self, new_applicant_id, child_id,update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)
        applicant_family_relation_obj = http.request.env['website.recruitment.application.family_details'].sudo().search([('id',
                                                                                  '=',
                                                                                  child_id)])
        applicant_family_relation_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])
        if int(update_only or 0) != 1:        
            return request.redirect("/jobs/apply_all/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_update/%s/1"  % new_applicant_id)                
        #return request.redirect("/jobs/apply_all/%s"  % slug(application_obj))

    @http.route('/jobs/delete_educ_back_details/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def delete_educ_back_details(self, new_applicant_id,child_id,update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)
        applicant_educ_bac_obj = http.request.env['website.recruitment.application.education'].sudo().search([('id',
                                                                                                                    '=',
                                                                                                                    child_id)])
        applicant_educ_bac_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])
        if int(update_only or 0) != 1:        
            return request.redirect("/jobs/apply_all/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_update/%s/1"  % new_applicant_id)        
        #return request.redirect("/jobs/apply_all/%s"  % slug(application_obj))


    @http.route('/jobs/apply_delete_documents/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_delete_documents(self, new_applicant_id,child_id,update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)

        applicant_document_obj = http.request.env['website.recruitment.application.documents'].sudo().search([('id','=',
                                                                                                                child_id)])

        applicant_document_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])
        if int(update_only or 0) != 1:        
            return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_2_update/%s/1"  % new_applicant_id)

        #return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))


    @http.route('/jobs/apply_delete_denied_visa/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_delete_denied_visa(self, new_applicant_id,child_id,update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)

        model_obj = http.request.env['website.recruitment.denied.visa'].sudo().search([('id','=',
                                                                                        child_id)])

        model_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])

        if int(update_only or 0) != 1:        
            return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_2_update/%s/1"  % new_applicant_id)

    @http.route('/jobs/apply_delete_deported/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_delete_deported(self, new_applicant_id,child_id,update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)

        model_obj = http.request.env['website.recruitment.deported'].sudo().search([('id','=',
                                                                                    child_id)])

        model_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])
        if int(update_only or 0) != 1:        
            return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_2_update/%s/1"  % new_applicant_id)

    @http.route('/jobs/apply_delete_deported/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_delete_deported(self, new_applicant_id,child_id,update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)

        model_obj = http.request.env['website.recruitment.deported'].sudo().search([('id','=',
                                                                                    child_id)])

        model_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])
        if int(update_only or 0) != 1:        
            return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_2_update/%s/1"  % new_applicant_id)

    @http.route('/jobs/apply_delete_training_courses/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_delete_training_courses(self, new_applicant_id,child_id,update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)

        model_obj = http.request.env['website.recruitment.training.courses'].sudo().search([('id','=',
                                                                                            child_id)])

        model_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])
        if int(update_only or 0) != 1:        
            return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_2_update/%s/1"  % new_applicant_id)

    @http.route('/jobs/apply_delete_license/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_delete_training_license(self, new_applicant_id,child_id,update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)

        model_obj = http.request.env['website.recruitment.license'].sudo().search([('id','=',
                                                                                    child_id)])

        model_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])
        if int(update_only or 0) != 1:        
            return request.redirect("/jobs/apply_all_2/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_2_update/%s/1"  % new_applicant_id)

    @http.route('/jobs/apply_delete_medical_history/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_delete_medical_history(self, new_applicant_id,child_id,update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)

        model_obj = http.request.env['website.recruitment.medical.history'].sudo().search([('id','=',
                                                                                            child_id)])

        model_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])

        if int(update_only or 0) != 1:        
            return request.redirect("/jobs/apply_all_3/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_3_update/%s/1"  % new_applicant_id)


    @http.route('/jobs/apply_delete_medical_operation/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_delete_medical_operation(self, new_applicant_id,child_id, update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)

        model_obj = http.request.env['website.recruitment.medical.operation'].sudo().search([('id','=',
                                                                                            child_id)])

        model_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])

        if int(update_only or 0) != 1:        
            return request.redirect("/jobs/apply_all_3/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_3_update/%s/1"  % new_applicant_id)

    @http.route('/jobs/apply_delete_medical_illness/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_delete_medical_illness(self, new_applicant_id,child_id,update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)

        model_obj = http.request.env['website.recruitment.medical.illness'].sudo().search([('id','=',
                                                                                            child_id)])

        model_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])

        if int(update_only or 0) != 1:        
            return request.redirect("/jobs/apply_all_3/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_3_update/%s/1"  % new_applicant_id)

    @http.route('/jobs/apply_delete_employee_relatives/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_delete_employee_relatives(self, new_applicant_id,child_id,update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)

        model_obj = http.request.env['website.recruitment.employee.relative'].sudo().search([('id','=',
                                                                                              child_id)])

        model_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])

        if int(update_only or 0) != 1:        
            return request.redirect("/jobs/apply_all_3/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_3_update/%s/1"  % new_applicant_id)

    @http.route('/jobs/apply_delete_previous_application/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_delete_previous_application(self, new_applicant_id,child_id,update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)

        model_obj = http.request.env['website.recruitment.previous.application'].sudo().search([('id','=',
                                                                                                 child_id)])

        model_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])

        if int(update_only or 0) != 1:        
            return request.redirect("/jobs/apply_all_3/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_3_update/%s/1"  % new_applicant_id)

    @http.route('/jobs/apply_delete_employment_history/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_delete_employment_history(self, new_applicant_id,child_id,update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)

        model_obj = http.request.env['website.recruitment.previous.employment'].sudo().search([('id','=',
                                                                                                 child_id)])

        model_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])

        if int(update_only or 0) != 1:        
            return request.redirect("/jobs/apply_all_4/%s"  % slug(application_obj))          
        else:
            return request.redirect("/jobs/apply_all_4_update/%s/1"  % new_applicant_id)        
        #return request.redirect("/jobs/apply_all_4/%s"  % slug(application_obj))

#EDIT OF RECORDS
    @http.route('/jobs/apply_edit_family_details/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_edit_family_details(self, new_applicant_id,child_id, update_only):
        error = {}
        default = {}


        
        applicant_family_relation_obj = http.request.env['website.recruitment.application.family_details'].sudo().search([])

        applicant_family_relation_obj = http.request.env['website.recruitment.application.family_details'].sudo().search([('id', '=', child_id)])

        search_list=[]

        if applicant_family_relation_obj.allow_delete==False:
            search_list = [('id', '=', applicant_family_relation_obj.relationship.id)]

        relationship_obj = http.request.env['hr.familyrelations'].sudo().search(search_list)

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_family_details", {
            'applicant':applicant_family_relation_obj,
            'new_applicant_id':new_applicant_id,
            'child_id':child_id,
            'edit_files':1,
            'update_only':update_only,
            #'job': job,
            'error': error,
            'default': default,
            'relationships':relationship_obj,
        })   

    @http.route('/jobs/edit_educ_back_details/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def edit_educ_back_details(self, new_applicant_id,child_id, update_only):
        error = {}
        default = {}
        level_obj = http.request.env['hr.recruitment.degree'].sudo().search([])

        applicant_educ_bac_obj = http.request.env['website.recruitment.application.education'].sudo().search([('id', '=', child_id)])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_educational_background", {
            'applicant':applicant_educ_bac_obj,
            'new_applicant_id':new_applicant_id,
            'schooltypes': level_obj,
            'edit_files':1,
            'child_id':child_id,
            'update_only':update_only,
            #'job': job,
            'error': error,
            'default': default,
            'relationships':level_obj,
        })

    @http.route('/jobs/apply_edit_documents/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_edit_documents(self, new_applicant_id,child_id,update_only):
        error = {}
        default = {}
        

        applicant_document_obj = http.request.env['website.recruitment.application.documents'].sudo().search([('id', '=', child_id)])

        search_list=[]

        if applicant_document_obj.allow_delete==False:
            search_list = [('id', '=', applicant_document_obj.document.id)]


        doc_type_obj = http.request.env['hr.documenttype'].sudo().search(search_list)

        #relationship_obj = http.request.env['hr.familyrelations'].sudo().search(search_list)

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_documents", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'documents': doc_type_obj,
            'edit_files':1,
            'update_only':update_only,
            'child_id':child_id,            
            #'job': job,
            'error': error,
            'default': default,
        })  

    @http.route('/jobs/apply_edit_denied_visa/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_edit_denied_visa(self, new_applicant_id,child_id, update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.denied.visa'].sudo().search([('id', '=', child_id)])
        country_all = http.request.env['res.country'].sudo().search([])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_denied_visa", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'nationality_ids': country_all,
            'edit_files':1,
            'child_id':child_id, 
            'update_only':update_only,             
            #'job': job,
            'error': error,
            'default': default,
        })   

    @http.route('/jobs/apply_edit_deported/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_edit_deported(self, new_applicant_id,child_id, update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.deported'].sudo().search([('id', '=', child_id)])
        country_all = http.request.env['res.country'].sudo().search([])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_deported", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'nationality_ids': country_all,
            'edit_files':1,
            'child_id':child_id, 
            'update_only':update_only,             
            'error': error,
            'default': default,
        })

    @http.route('/jobs/apply_edit_training_courses/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_edit_training_courses(self, new_applicant_id,child_id, update_only):
        error = {}
        default = {}

        applicant_license_type = http.request.env['hr.licensetype'].sudo().search([('name','=','Training')])

        applicant_license = http.request.env['hr.license'].sudo().search([('license_name', '=', applicant_license_type.id)])        

        applicant_document_obj = http.request.env['website.recruitment.training.courses'].sudo().search([('id', '=', child_id)])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_training_courses", {
            'trainings': applicant_license,
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'edit_files':1,
            'child_id':child_id,
            'update_only':update_only,
            'error': error,
            'default': default,
        })        

    @http.route('/jobs/apply_edit_license/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_edit_license(self, new_applicant_id,child_id, update_only):
        error = {}
        default = {}

        applicant_license_type = http.request.env['hr.licensetype'].sudo().search([('name','=','License')])

        applicant_license = http.request.env['hr.license'].sudo().search([('license_name', '=', applicant_license_type.id)])                

        applicant_document_obj = http.request.env['website.recruitment.license'].sudo().search([('id', '=', child_id)])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_license", {
            'trainings': applicant_license,
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'edit_files':1,
            'child_id':child_id,  
            'update_only':update_only,          
            'error': error,
            'default': default,
        }) 

    @http.route('/jobs/apply_edit_medical_history/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_edit_medical_history(self, new_applicant_id,child_id, update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.medical.history'].sudo().search([('id', '=', child_id)])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_medical_history", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'edit_files':1,
            'child_id':child_id,   
            'update_only':update_only,         
            'error': error,
            'default': default,
        })         


    @http.route('/jobs/apply_edit_medical_operation/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_edit_medical_operation(self, new_applicant_id,child_id, update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.medical.operation'].sudo().search([('id', '=', child_id)])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_medical_operation", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'error': error,
            'edit_files':1,
            'update_only':update_only,
            'child_id':child_id,            
            'default': default,
        })

    @http.route('/jobs/apply_edit_medical_illness/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_edit_medical_illness(self, new_applicant_id,child_id, update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.medical.illness'].sudo().search([('id', '=', child_id)])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_medical_illness", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'error': error,
            'edit_files':1,
            'update_only':update_only,
            'child_id':child_id,            
            'default': default,
        })

    @http.route('/jobs/apply_edit_employee_relatives/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_edit_employee_relatives(self, new_applicant_id,child_id, update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.employee.relative'].sudo().search([('id', '=', child_id)])
        relationship_obj = http.request.env['hr.familyrelations'].sudo().search([])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_employee_relatives", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'error': error,
            'edit_files':1,
            'child_id':child_id,
            'update_only':update_only,            
            'relationships':relationship_obj,
            'default': default,
        })

    @http.route('/jobs/apply_edit_previous_application/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_edit_previous_application(self, new_applicant_id,child_id, update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.previous.application'].sudo().search([('id', '=', child_id)])
        model_jobs = http.request.env['hr.job'].sudo().search([])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_previous_application", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'error': error,
            'edit_files':1,
            'child_id':child_id, 
            'update_only':update_only,           
            'default': default,
            'jobs': model_jobs,
        })

    @http.route('/jobs/apply_edit_employment_history/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_edit_employment_history(self, new_applicant_id,child_id, update_only):
        error = {}
        default = {}

        applicant_document_obj = http.request.env['website.recruitment.previous.employment'].sudo().search([('id', '=', child_id)])
        model_jobs = http.request.env['hr.job'].sudo().search([])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_employment_history", {
            'applicant':applicant_document_obj,
            'new_applicant_id':new_applicant_id,
            'error': error,
            'edit_files':1,
            'child_id':child_id, 
            'update_only':update_only,           
            'default': default,
            'jobs': model_jobs,
        })        

#Final Form
    @http.route('/jobs/apply_final_execute', methods=['POST'], type='http', auth="public", website=True)
    def jobs_apply_final_form_execute(self, **post):
        env = request.env(user=SUPERUSER_ID)

        applicant_emp_his_cnt = env['website.recruitment.previous.employment'].sudo().search_count([('applicant_id',
                                                                                                     '=',
                                                                                                     int(post.get('new_applicant_id')))])

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('new_applicant_id'))])

        if applicant_emp_his_cnt > 0:
            return request.redirect("/jobs/apply_all_summary/%s"  % slug(application_obj))
        else:
            return request.render("website_hr_recruitment_bahia.apply_all_4", 
                {
                    'applicant':application_obj.sudo(),
                    'update_only': int(post.get('update_only') or 0),
                    'with_error':1,
                })            

    @http.route('/jobs/thankyou', methods=['POST'], type='http', auth="public", website=True)
    def jobs_thankyou(self, **post):
        error = {}
        #"partner_name"
        #, "ufile"
        for field_name in ["phone", "email_from", "first_name","last_name"]:
            if not post.get(field_name):
                error[field_name] = 'missing'
        if error:
            request.session['website_hr_recruitment_bahia_error'] = error
            #ufile = post.pop('ufile')
            #if ufile:
            #    error['ufile'] = 'reset'
            #request.session['website_hr_recruitment_bahia_default'] = post
            #return request.redirect('/jobs/apply/%s' % post.get("job_id"))

        # public user can't create applicants (duh)

        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('new_applicant_id'))])        
        value = {
            'source_id' : env.ref('hr_recruitment.source_website_company').id,
            'name': '%s\'s Application' % post.get('partner_name'),
        }
        # Added by SDS NEW October 07 2015
        #'gender','applicants_address','date_applied'
        #'partner_name',
        #for f in ['email_from', 'description', "first_name","last_name"]:
        #    value[f] = post.get(f)
        #for f in ['department_id', 'job_id']:
        #    value[f] = int(post.get(f) or 0)


        #Get Address
        family_details = []
        family_details_list =[]
        for family in application_obj.applicant_families:
            family_details_list =[ 0, False,
                {
                    'relationship': family.relationship.id,
                    'first_name': family.first_name,
                    'last_name': family.last_name,
                    'middle_name': family.middle_name,
                    'gender': family.gender,
                    'date_of_birth': family.date_of_birth,
                    'place_of_birth': family.placeof_birth,

                }
            ]
            family_details.append(family_details_list)

        #Get Education
        eduction_details = []
        eduction_details_list =[]
        for education in application_obj.applicant_education:
            eduction_details_list =[ 0, False,
                {
                    'schooltype': education.schooltype.id,
                    'name_school': education.name_school,
                    'date_from': education.date_from,
                    'date_to': education.date_to,
                    'school_address': education.school_address,
                    'description': education.description,

                }
            ]
            eduction_details.append(eduction_details_list)


        #Get Document
        document_details = []
        document_details_list =[]
        for document in application_obj.applicant_document_ids:
            document_details_list =[ 0, False,
                {
                    'document': document.document.id,
                    'document_number': document.document_number,
                    'date_issued': document.date_issued,
                    'date_expiry': document.date_expiry,
                    'issuing_authority': document.issuing_authority,

                }
            ]
            document_details.append(document_details_list)

        #Denied Visa
        denied_visa = []
        denied_visa_list =[]
        for document in application_obj.applicant_denied_visa_ids:
            denied_visa_list =[ 0, False,
                {
                    'nationality_id': document and document.nationality_id and document.nationality_id.id or False,
                    'date_denied': document.date_denied or False,
                    'reason': document.reason,
                }
            ]
            denied_visa.append(denied_visa_list)


        #Denied Visa
        deported = []
        deported_list =[]
        for document in application_obj.applicant_deported_ids:
            deported_list =[ 0, False,
                {
                    'nationality_id': document.nationality_id.id,
                    'date_deported': document.date_deported or False,
                    'reason': document.reason,
                }
            ]
            deported.append(deported_list)

        #Training Course
        training_course = []
        training_course_list =[]
        for document in application_obj.applicant_training_courses_ids:
            training_course_list =[ 0, False,
                {
                    'training_name': document.training_name,
                    'training_id' : document and document.training_id and document.training_id.id or False,
                    'document_no': document.document_no,
                    'issue_date': document.issue_date or False,
                    'training_centers': document.training_centers,
                    'is_with_cop': document.is_with_cop,
                    'issue_date_cop': document.issue_date_cop or False,
                }
            ]
            training_course.append(training_course_list)

        #License
        license = []
        license_list = []
        for document in application_obj.applicant_license_ids:
            license_list =[ 0, False,
                {
                    'training_name': document.training_name,
                    'training_id' : document and document.license_id and document.license_id.id or False,
                    'document_no': document.document_no,
                    'issue_date': document.issue_date,
                    'expiry_date': document.expiry_date,
                    'issuing_authority': document.issuing_authority,
                    'issuing_authority_other': document.issuing_authority_other,
                }
            ]
            license.append(license_list)

        
        #Med Hist.
        med_hist = []
        med_hist_list = [] 
        for document in application_obj.applicant_medical_history_ids:
            med_hist_list =[ 0, False,
                {
                    'vessel_name': document.vessel_name,
                    'occurence_place': document.occurence_place,
                    'occurence_date': document.occurence_date,
                    'description': document.description,
                }
            ]
            med_hist.append(med_hist_list)   

        #Med Opertation
        med_oper = []
        med_oper_list = [] 
        for document in application_obj.applicant_medical_operation_ids:
            med_oper_list =[ 0, False,
                {
                    'details_of_operation': document.details_of_operation,
                    'date_of_operation': document.date_of_operation,
                    'period_of_disability': document.period_of_disability,
                    'occurence_date': document.occurence_date or False,
                    'description': document.description,
                }
            ]
            med_oper.append(med_oper_list)    


        #Med Ilness
        med_illness = []
        med_illness_list = [] 
        for document in application_obj.applicant_medical_illness_ids:
            med_illness_list =[ 0, False,
                {
                    'details_of_illness_accident': document.details_of_illness_accident,
                    'date_illness_accident': document.date_illness_accident,
                    'therapy_treatment_description': document.therapy_treatment_description,
                }
            ]
            med_illness.append(med_illness_list)    

        #Employed Relatives
        emp_rel = []
        emp_rel_list = [] 
        for document in application_obj.applicant_employed_relatives_ids:
            emp_rel_list =[ 0, False,
                {
                    'name_of_crew': document.name_of_crew,
                    'position_and_principal': document.position_and_principal,
                    'relationship': document.relationship.id,
                }
            ]
            emp_rel.append(emp_rel_list)  

        #Previous Application
        prev_app_rel = []
        prev_app_list = [] 
        for document in application_obj.applicant_previous_application_ids:
            prev_app_list =[ 0, False,
                {
                    'date_applied': document.date_applied or False,
                    'job_applied_id': document and document.job_applied_id and document.job_applied_id.id or False,
                }
            ]
            prev_app_rel.append(prev_app_list) 

        #Previous Application
        prev_app_emp = []
        prev_app_emp_list = [] 
        for document in application_obj.applicant_previous_employment_ids:
            prev_app_emp_list =[ 0, False,
                {
                    'rank_position': document.rank_position,
                    'manning_agency': document.manning_agency,
                    'employer_principal': document.employer_principal,
                    'address_contact_info_manning_agen': document.address_contact_info_manning_agen,
                    'vessel_name': document.vessel_name,
                    'vessel_type': document.vessel_type or False,
                    'grt': document.grt,
                    'date_from': document.date_from or False,
                    'date_to': document.date_to or False,
                    'duties_and_responsibility': document.duties_and_responsibility,
                }
            ]
            prev_app_emp.append(prev_app_emp_list)

        #Social Media
        socialmedia_app = []
        socialmedia_app_list = []
        for document in application_obj.applicant_socialmedia_ids:
            socialmedia_app_list =[ 0, False,
                {
                    'socialmedia_id': document and document.socialmedia_id and document.socialmedia_id.id, 
                    'name': document.name,
                }
            ]
            socialmedia_app.append(socialmedia_app_list)



        #raise Warning(post)
        # Retro-compatibility for saas-3. "phone" field should be replace by "partner_phone" in the template in trunk.
        value['partner_phone'] =  application_obj.contact_number #post.pop('phone', False)
        value['partner_name'] =  application_obj.last_name or '' + ', ' +  application_obj.first_name or '' #post.pop('last_name') + ', ' +  post.pop('first_name')
        value['name'] = value['partner_name']
        value['job_id'] = application_obj.job_applied_id.id

        value['middle_name'] = application_obj.maiden_name or ''

        value['preffered_nickname'] = application_obj.preferred_nickname
        value['weight'] = application_obj.weight
        value['height'] = application_obj.height
        value['placeof_birth'] = application_obj.place_of_birth
        value['sss_no'] = application_obj.sss_no
        value['hdmf_no'] = application_obj.pagibig_no
        value['philhealth_no'] = application_obj.philhealth_no
        value['pagibig_no'] = application_obj.pagibig_no

        value['date_of_birth'] = application_obj.date_of_birth
        value['email_from'] = application_obj.email_address
        value['shoe_size'] = application_obj.shoe_size

        #value['nationality_id'] = application_obj.nationality_id and application_obj.nationality_id.name or False
        


        



        value['last_name'] = application_obj.last_name
        value['first_name'] = application_obj.first_name
        value['maiden_name'] = application_obj.maiden_name

        civil_status = False
        if application_obj.civil_status != '0':
            civil_status = application_obj.civil_status

        gender = False
        if application_obj.gender != '0':
            gender = application_obj.gender


        value['civil_status'] = civil_status
        value['gender'] = gender

        value['permanent_address_adress'] = application_obj.permanent_address_adress
        value['permanent_address_city'] = application_obj.permanent_address_city
        value['permanent_address_zipcode'] = application_obj.permanent_address_zipcode
        value['permanent_address_contact_no'] = application_obj.permanent_address_contact_no


        value['alternative_address_adress'] = application_obj.alternative_address_adress
        value['alternative_address_city'] = application_obj.alternative_address_city
        value['alternative_address_zipcode'] = application_obj.alternative_address_zipcode
        value['alternative_address_contact_no'] = application_obj.alternative_address_contact_no


        value['emergency_person_name'] = application_obj.emergency_person_name
        value['emergency_relationship_1'] = application_obj.emergency_relationship
        value['emergency_address'] = application_obj.emergency_address
        value['emergency_zipcode'] = application_obj.emergency_zipcode
        value['emergency_contactno'] = application_obj.emergency_contactno
        value['image'] = application_obj.image

        is_denied_visa = False
        if application_obj.is_denied_visa and application_obj.is_denied_visa !=False:
            is_denied_visa = True

        is_deported = False
        if application_obj.is_deported and application_obj.is_deported !=False:
            is_deported = True

        is_medical_reason_1 = False
        if application_obj.is_medical_reason_1 and application_obj.is_medical_reason_1 !=False:
            is_medical_reason_1 = True

        is_medical_operation = False
        if application_obj.is_deported and application_obj.is_deported !=False:
            is_medical_operation = True

        has_hypertension = False
        if application_obj.has_hypertension and application_obj.has_hypertension !=False:
            has_hypertension = True

        has_diabetes = False
        if application_obj.has_diabetes and application_obj.has_diabetes !=False:
            has_diabetes = True

        has_hepatitis_a_b = False
        if application_obj.has_hepatitis_a_b and application_obj.has_hepatitis_a_b !=False:
            has_hepatitis_a_b = True

        has_asthma = False
        if application_obj.has_asthma and application_obj.has_asthma !=False:
            has_asthma = True            

        is_smoker = False
        if application_obj.is_smoker and application_obj.is_smoker !=False:
            is_smoker = True

        value['is_denied_visa'] = is_denied_visa
        value['is_deported'] = is_deported
        value['is_medical_reason_1'] = is_medical_reason_1 
        value['is_medical_operation'] = is_medical_operation 
        value['has_hypertension'] = has_hypertension 
        value['has_diabetes'] = has_diabetes 
        value['has_hepatitis_a_b'] = has_hepatitis_a_b 
        value['has_asthma'] = has_asthma


        value['is_smoker'] = is_smoker
        value['reference_1_company_name'] = application_obj.reference_1_company_name
        value['reference_1_name_person'] = application_obj.reference_1_name_person
        value['reference_1_address'] = application_obj.reference_1_address
        value['reference_1_contact_no'] = application_obj.reference_1_contact_no
        value['reference_2_company_name'] = application_obj.reference_2_company_name
        value['reference_2_name_person'] = application_obj.reference_2_name_person
        value['reference_2_address'] = application_obj.reference_2_address
        value['reference_2_contact_no'] = application_obj.reference_2_contact_no


        has_relative_employee = False
        if application_obj.has_relative_employee and application_obj.has_relative_employee !=False:
            has_relative_employee = True

        has_applied_previously = False
        if application_obj.has_applied_previously and application_obj.has_applied_previously !=False:
            has_applied_previously = True            

        value['has_relative_employee'] = has_relative_employee 
        value['has_applied_previously'] =has_applied_previously





        if len(family_details) > 0:
            value['applicant_families'] = family_details
        if len(eduction_details) > 0:
            value['applicant_education'] = eduction_details
        if len(document_details) > 0:
            value['applicant_document_ids'] = document_details
        if len(denied_visa) > 0:
            value['applicant_denied_visa_ids'] = denied_visa
        if len(deported) > 0:
            value['applicant_deported_ids'] = deported
        if len(training_course) > 0:
            value['applicant_training_courses_ids'] = training_course
        if len(license) > 0:
            value['applicant_license_ids'] = license
        if len(med_hist) > 0:
            value['applicant_medical_history_ids'] = med_hist
        if len(med_oper) > 0:
            value['applicant_medical_operation_ids'] = med_oper
        if len(med_illness) > 0:
            value['applicant_medical_illness_ids'] = med_illness
        if len(emp_rel) > 0:
            value['applicant_employed_relatives_ids'] = emp_rel
        if len(prev_app_rel) > 0:
            value['applicant_previous_application_ids'] = prev_app_rel
        if len(prev_app_emp) > 0:
            value['applicant_previous_employment_ids'] = prev_app_emp

        if len(socialmedia_app) > 0:
            value['applicant_socialmedia_ids'] = socialmedia_app
        


        
        applicant_id = env['hr.applicant'].create(value).id

        if applicant_id:
            application_obj.unlink()

            applicant_obj = env['hr.applicant'].search([('id','=', applicant_id)])

            last_name =''
            first_name =''
            middle_name =''

            if applicant_obj.last_name:
                last_name =applicant_obj.last_name

            if applicant_obj.first_name:
                first_name =applicant_obj.first_name

            if applicant_obj.middle_name:
                middle_name =applicant_obj.middle_name

            applicant_obj.update({'partner_name': last_name + ',' + first_name + ' ' + middle_name,
                                  'name': last_name + ',' + first_name + ' ' + middle_name})

            if post['file_upload']:
                attachment_value = {
                    'name': post['file_upload'].filename,
                    'res_name': applicant_obj.partner_name,
                    'res_model': 'hr.applicant',
                    'res_id': applicant_id,
                    'datas': base64.encodestring(post['file_upload'].read()),
                    'datas_fname': post['file_upload'].filename,
                }
                env['ir.attachment'].create(attachment_value)

        #if post['ufile']:
        #    attachment_value = {
        #        'name': post['ufile'].filename,
        #        'res_name': value['partner_name'],
        #        'res_model': 'hr.applicant',
        #        'res_id': applicant_id,
        #        'datas': base64.encodestring(post['ufile'].read()),
        #        'datas_fname': post['ufile'].filename,
        #    }
        #    env['ir.attachment'].create(attachment_value)
        return request.render("website_hr_recruitment_bahia.thankyou", {})
#============================== THIS WILL ADD NEW FORM FUNCTIONS ETC
    # =================================== Social Media ===================================
    @http.route('/jobs/apply_add_socmedia_details/<int:new_applicant_id>/<int:update_only>', type='http', auth="public", website=True)
    def jobs_apply_add_socmedia_details(self, new_applicant_id,update_only, **kw):
        error = {}
        default = {}

        social_media_obj = http.request.env['hr.socialmedia.config'].sudo().search([('allow_to_add_in_application','=',True)])
        applicant_socialmedia_obj = http.request.env['website.recruitment.socialmedia'].sudo().search([])
        applicant_socialmedia_obj = http.request.env['website.recruitment.socialmedia'].sudo().search([('id','=', new_applicant_id)])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        return request.render("website_hr_recruitment_bahia.apply_add_socialmedia_details", {
            'applicant':applicant_socialmedia_obj,
            'new_applicant_id':new_applicant_id,
            'edit_files':0,
            'update_only':update_only,
            #'job': job,
            'error': error,
            'default': default,
            'socialmedia':social_media_obj,
        })

    @http.route('/jobs/apply_add_socmedia_details_exectute', type='http', auth="public", website=True)
    def jobs_apply_add_socmedia_details_execute(self, **post):
        error = {}
        default = {}

        env = request.env(user=SUPERUSER_ID)

        application_obj = env['website.recruitment.application'].search([('id', '=', post.get('applicant_id'))])
        applicant_socialmedia_obj = http.request.env['website.recruitment.socialmedia'].sudo()

        if int(post.get('edit_file') or 0) != 1:
            applicant_socialmedia_obj_1 = applicant_socialmedia_obj
            res = applicant_socialmedia_obj.create({
                    'applicant_id' : post.get('applicant_id'),
                    'socialmedia_id': int(post.get('socialmedia_site') or 0),
                    'name': post.get('name')  or '',})
        else:
            applicant_socialmedia_obj_1 = applicant_socialmedia_obj.search([('id','=',post.get('child_id'))])

            res = applicant_socialmedia_obj_1.update({
                    'socialmedia_id': int(post.get('socialmedia_site') or 0),
                    'name': post.get('name')  or '',})

        if int(post.get('update_only') or 0) != 1:
            return request.redirect("/jobs/apply_all/%s"  % slug(application_obj))
        else:
            return request.redirect("/jobs/apply_all_update/%s/1"  % post.get('applicant_id'))


    @http.route('/jobs/delete_socmedia_details/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def delete_socmedia_details(self, new_applicant_id,child_id,update_only):
        error = {}
        default = {}
        env = request.env(user=SUPERUSER_ID)
        applicant_educ_bac_obj = http.request.env['website.recruitment.socialmedia'].sudo().search([('id','=',child_id)])
        applicant_educ_bac_obj.unlink()

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')

        application_obj = env['website.recruitment.application'].search([('id', '=', new_applicant_id)])
        if int(update_only or 0) != 1:
            return request.redirect("/jobs/apply_all/%s"  % slug(application_obj))
        else:
            return request.redirect("/jobs/apply_all_update/%s/1"  % new_applicant_id)

    @http.route('/jobs/edit_socmedia_details/<int:new_applicant_id>/<int:child_id>/<int:update_only>', type='http', auth="public", website=True)
    def edit_socmedia_details(self, new_applicant_id,child_id, update_only):
        error = {}
        default = {}
        social_media_obj =  http.request.env['hr.socialmedia.config'].sudo().search([])

        applicant_social_media_obj = http.request.env['website.recruitment.socialmedia'].sudo().search([('id', '=', child_id)])

        if 'website_hr_recruitment_bahia_error' in request.session:
            error = request.session.pop('website_hr_recruitment_bahia_error')
            default = request.session.pop('website_hr_recruitment_bahia_default')
        return request.render("website_hr_recruitment_bahia.apply_add_socialmedia_details", {
            'applicant':applicant_social_media_obj,
            'new_applicant_id':new_applicant_id,
            'edit_files':1,
            'child_id':child_id,
            'update_only':update_only,
            'error': error,
            'default': default,
            'socialmedia':social_media_obj,
        })
    # =================================== End Social Media ===================================
# vim :et:
