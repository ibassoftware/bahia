  # -*- coding: utf-8 -*-
from datetime import datetime #, timedelta
import werkzeug
from werkzeug.exceptions import Forbidden, NotFound

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request

from odoo.addons.http_routing.models.ir_http import slug

import base64
import uuid 
from cryptography.fernet import Fernet

import xlrd
import os, sys, traceback
from collections import OrderedDict


import pytz
import json

import logging
_logger = logging.getLogger(__name__)

class WebsitePopUpPrivacyPolicy(http.Controller):

	@http.route(['/page/privacy_policy'], type='http', auth="public", website=True)
	def privacy_policy(self):
		model_jobs = http.request.env['hr.job'].sudo().search([])

		return request.render("ibas_bahia_website.page_policy_popup", {
			'jobs':model_jobs,
			'with_jobs': 0,
		})

class BahiasApplicationForm(http.Controller):

	@http.route('/start-apply', type="http", auth="public", website=True)
	def start_apply(self, **kw):
		job_rec = request.env['hr.job'].sudo().search([])
		nationality_rec = request.env['res.country'].sudo().search([])
		familyrelation_rec = request.env['hr.familyrelations'].sudo().search([])
		level_rec = request.env['hr.recruitment.degree'].sudo().search([])
		documenttype_rec = request.env['hr.documenttype'].sudo().search([])
		social_media_rec = request.env['hr.socialmedia.config'].sudo().search([])
		return http.request.render('ibas_bahia_website.apply_template', {
			'job_rec': job_rec,
			'nationality_rec': nationality_rec,
			'familyrelation_rec': familyrelation_rec,
			'level_rec': level_rec,
			'documenttype_rec': documenttype_rec,
			'social_media_rec': social_media_rec,
		})

	@http.route('/jobs/apply', type="http", auth="public", website=True)
	def jobs_start_apply(self, **kw):
		job_rec = request.env['hr.job'].sudo().search([])
		nationality_rec = request.env['res.country'].sudo().search([])
		familyrelation_rec = request.env['hr.familyrelations'].sudo().search([])
		level_rec = request.env['hr.recruitment.degree'].sudo().search([])
		documenttype_rec = request.env['hr.documenttype'].sudo().search([])
		social_media_rec = request.env['hr.socialmedia.config'].sudo().search([])
		return http.request.render('ibas_bahia_website.apply_template', {
			'job_rec': job_rec,
			'nationality_rec': nationality_rec,
			'familyrelation_rec': familyrelation_rec,
			'level_rec': level_rec,
			'documenttype_rec': documenttype_rec,
			'social_media_rec': social_media_rec,
		})

	@http.route('/jobs/apply/execute/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
	def apply_execute(self, model_name, **kw):
		_logger.info("Apply execute")

		Applicant = request.env['hr.applicant']

		# Validation: Check for Name, Birthdate and Email Address
		applicant_name = kw.get('name')
		applicant_date_of_birth = kw.get('date_of_birth')
		if applicant_date_of_birth:
			applicant_date_of_birth = datetime.strptime(applicant_date_of_birth, '%m/%d/%Y').date()
		applicant_email_from = kw.get('email_from')

		duplicate_applicant_id = request.env['hr.applicant'].sudo().search([('name', '=', applicant_name), ('date_of_birth', '=', applicant_date_of_birth), ('email_from', '=', applicant_email_from)])
		
		if duplicate_applicant_id:
			error = _("Duplicate application! One applicant, one application only.")
			return json.dumps({
				'error': error,
			})
		else:
			# Is Created From Website
			kw['is_created_website'] = True

			# Applicant Name
			name = kw.get('name')
			if name:
				kw['partner_name'] = name

			# Applicant Image
			image_applicant = kw.get('image_1920[0][0]')
			image_filename = False
			image_data = False
			image_value = False
			if image_applicant:
				image_filename = kw.get('image_1920[0][0]').filename
				image_data = image_applicant.read()
				image_value = base64.b64encode(image_data)
				kw['image_1920'] = image_value.decode('ascii')
				kw.pop('image_1920[0][0]')

			# Applicant Date of Birth
			if applicant_date_of_birth:
				kw['date_of_birth'] = applicant_date_of_birth

			# Applicant Family
			applicant_families = kw.get('applicant_families')
			if applicant_families:
				family_val = []
				family_data = json.loads(applicant_families)
				if family_data:
					for family_line in family_data:
						relationship = family_line.get('relationship')
						first_name = family_line.get('first_name')
						last_name = family_line.get('last_name')
						gender = family_line.get('gender')
						date_of_birth = family_line.get('date_of_birth')
						placeof_birth = family_line.get('placeof_birth')

						if date_of_birth:
							is_valid_date = False
							date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
							start_date = datetime(1900, 1, 1).date()
							end_date = datetime(2090, 12, 31).date()
							if date_of_birth >= start_date and date_of_birth <= end_date:
								is_valid_date = True
							if not is_valid_date:
								error = _("Incorrect Data Format for Previous Application Family - Date of Birth. Please use format for dates: mm/dd/yyyy.")
								return json.dumps({
									'error': error,
								})

						if not relationship or not first_name or not last_name or not gender:
							error = _("Missing required fields for applicant family details!")
							return json.dumps({
								'error': error,
							})
						else:
							family_line_data = {
								'relationship': relationship,
								'first_name': first_name,
								'last_name': last_name,
								'gender': gender,
								'date_of_birth': date_of_birth,
								'placeof_birth': placeof_birth,
							}
							family_val.append((0, 0, family_line_data))

				kw['applicant_families'] = family_val

			# Applicant Education
			applicant_education = kw.get('applicant_education')
			if applicant_education:
				education_val = []
				education_data = json.loads(applicant_education)
				if education_data:
					for education_line in education_data:
						schooltype = education_line.get('schooltype')
						name_school = education_line.get('name_school')
						description = education_line.get('description')
						date_from = education_line.get('date_from')
						date_to = education_line.get('date_to')
						school_address = education_line.get('school_address')

						if date_from:
							is_valid_date = False
							date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
							start_date = datetime(1900, 1, 1).date()
							end_date = datetime(2090, 12, 31).date()
							if date_from >= start_date and date_from <= end_date:
								is_valid_date = True
							if not is_valid_date:
								error = _("Incorrect Data Format for Applicant Education - Date From. Please use format for dates: mm/dd/yyyy.")
								return json.dumps({
									'error': error,
								})

						if date_to:
							is_valid_date = False
							date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
							start_date = datetime(1900, 1, 1).date()
							end_date = datetime(2090, 12, 31).date()
							if date_to >= start_date and date_to <= end_date:
								is_valid_date = True
							if not is_valid_date:
								error = _("Incorrect Data Format for Applicant Education - Date To. Please use format for dates: mm/dd/yyyy.")
								return json.dumps({
									'error': error,
								})

						if not schooltype or not name_school or not description or not date_from or not date_to or not school_address:
							error = _("Missing required fields for applicant education details!")
							return json.dumps({
								'error': error,
							})
						else:
							education_line_data = {
								'schooltype': schooltype,
								'name_school': name_school,
								'description': description,
								'date_from': date_from,
								'date_to': date_to,
								'school_address': school_address,
							}
							education_val.append((0, 0, education_line_data))
				kw['applicant_education'] = education_val

			# Applicant Record Books
			applicant_document_ids = kw.get('applicant_document_ids')
			if applicant_document_ids:
				record_books_val = []
				record_books_data = json.loads(applicant_document_ids)
				if not record_books_data:
					error = _("Record Books is required! Please add Passport and Seamans Book")
					return json.dumps({
						'error': error,
					})
				else:
					for record_books_line in record_books_data:
						document = record_books_line.get('document')
						document_number = record_books_line.get('document_number')
						date_issued = record_books_line.get('date_issued')
						date_expiry = record_books_line.get('date_expiry')
						issuing_authority = record_books_line.get('issuing_authority')
						place_ofissue = record_books_line.get('place_ofissue')

						if date_issued:
							is_valid_date = False
							date_issued = datetime.strptime(date_issued, '%Y-%m-%d').date()
							start_date = datetime(1900, 1, 1).date()
							end_date = datetime(2090, 12, 31).date()
							if date_issued >= start_date and date_issued <= end_date:
								is_valid_date = True
							if not is_valid_date:
								error = _("Incorrect Data Format for Applicant Record Books - Date Issued. Please use format for dates: mm/dd/yyyy.")
								return json.dumps({
									'error': error,
								})
							
						if date_expiry:
							is_valid_date = False
							date_expiry = datetime.strptime(date_expiry, '%Y-%m-%d').date()
							start_date = datetime(1900, 1, 1).date()
							end_date = datetime(2090, 12, 31).date()
							if date_expiry >= start_date and date_expiry <= end_date:
								is_valid_date = True
							if not is_valid_date:
								error = _("Incorrect Data Format for Applicant Record Books - Date Expiry. Please use format for dates: mm/dd/yyyy.")
								return json.dumps({
									'error': error,
								})

						if not document or not document_number or not date_issued or not date_expiry or not issuing_authority or not place_ofissue:
							error = _("Missing required fields for applicant record books details!")
							return json.dumps({
								'error': error,
							})
						else:
							record_books_line_data = {
								'document': document,
								'document_number': document_number,
								'date_issued': date_issued,
								'date_expiry': date_expiry,
								'issuing_authority': issuing_authority,
								'place_ofissue': place_ofissue,
							}
							record_books_val.append((0, 0, record_books_line_data))

				kw['applicant_document_ids'] = record_books_val

			# References - Employed Relatives
			applicant_employed_relatives_ids = kw.get('applicant_employed_relatives_ids')
			if applicant_employed_relatives_ids:
				employed_relatives_val = []
				employed_relatives_data = json.loads(applicant_employed_relatives_ids)
				if employed_relatives_data:
					for employed_relatives_line in employed_relatives_data:
						name_of_crew = employed_relatives_line.get('name_of_crew')
						position_and_principal = employed_relatives_line.get('position_and_principal')
						relationship = employed_relatives_line.get('relationship')
						
						if not name_of_crew or not position_and_principal or not relationship:
							error = _("Missing required fields for applicant employed relative details!")
							return json.dumps({
								'error': error,
							})
						else:
							employed_relatives_line_data = {
								'name_of_crew': name_of_crew,
								'position_and_principal': position_and_principal,
								'relationship': relationship,
							}
							employed_relatives_val.append((0, 0, employed_relatives_line_data))
				kw['applicant_employed_relatives_ids'] = employed_relatives_val

			# References - Previous Application
			applicant_previous_application_ids = kw.get('applicant_previous_application_ids')
			if applicant_previous_application_ids:
				applicant_previous_application_val = []
				applicant_previous_application_data = json.loads(applicant_previous_application_ids)
				if applicant_previous_application_data:
					for applicant_previous_application_line in applicant_previous_application_data:
						date_applied = applicant_previous_application_line.get('date_applied')
						job_applied_id = applicant_previous_application_line.get('job_applied_id')

						if date_applied:
							is_valid_date = False
							date_applied = datetime.strptime(date_applied, '%Y-%m-%d').date()
							start_date = datetime(1900, 1, 1).date()
							end_date = datetime(2090, 12, 31).date()
							if date_applied >= start_date and date_applied <= end_date:
								is_valid_date = True
							if not is_valid_date:
								error = _("Incorrect Data Format for Previous Application - Date. Please use format for dates: mm/dd/yyyy.")
								return json.dumps({
									'error': error,
								})
						
						if not date_applied or not job_applied_id:
							error = _("Missing required fields for applicant previous application details!")
							return json.dumps({
								'error': error,
							})
						else:
							applicant_previous_application_line_data = {
								'date_applied': date_applied,
								'job_applied_id': job_applied_id,
							}
							applicant_previous_application_val.append((0, 0, applicant_previous_application_line_data))
				kw['applicant_previous_application_ids'] = applicant_previous_application_val

			# References - Previous Employment
			applicant_previous_employment_ids = kw.get('applicant_previous_employment_ids')
			if applicant_previous_employment_ids:
				applicant_previous_employment_val = []
				applicant_previous_employment_data = json.loads(applicant_previous_employment_ids)
				if not applicant_previous_employment_data:
					error = _("Employment History is required!")
					return json.dumps({
						'error': error,
					})
				else:
					for applicant_previous_employment_line in applicant_previous_employment_data:
						rank_position = applicant_previous_employment_line.get('rank_position')
						manning_agency = applicant_previous_employment_line.get('manning_agency')
						employer_principal = applicant_previous_employment_line.get('employer_principal')
						address_contact_info_manning_agen = applicant_previous_employment_line.get('address_contact_info_manning_agen')
						vessel_name = applicant_previous_employment_line.get('vessel_name')
						vessel_type = applicant_previous_employment_line.get('vessel_type')
						grt = applicant_previous_employment_line.get('grt')
						date_from = applicant_previous_employment_line.get('date_from')
						date_to = applicant_previous_employment_line.get('date_to')
						duties_and_responsibility = applicant_previous_employment_line.get('duties_and_responsibility')


						if date_from:
							is_valid_date = False
							date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
							start_date = datetime(1900, 1, 1).date()
							end_date = datetime(2090, 12, 31).date()
							if date_from >= start_date and date_from <= end_date:
								is_valid_date = True
							if not is_valid_date:
								error = _("Incorrect Data Format for Employment History - Date From. Please use format for dates: mm/dd/yyyy.")
								return json.dumps({
									'error': error,
								})

						if date_to:
							is_valid_date = False
							date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
							start_date = datetime(1900, 1, 1).date()
							end_date = datetime(2090, 12, 31).date()
							if date_to >= start_date and date_to <= end_date:
								is_valid_date = True
							if not is_valid_date:
								error = _("Incorrect Data Format for Employment History - Date To. Please use format for dates: mm/dd/yyyy.")
								return json.dumps({
									'error': error,
								})

						if not rank_position or not manning_agency or not employer_principal or not address_contact_info_manning_agen or not vessel_name or not vessel_type or not grt or not date_from or not date_to or not duties_and_responsibility:
							error = _("Missing required fields for applicant employment history!")
							return json.dumps({
								'error': error,
							})
						else:
							applicant_previous_employment_line_data = {
								'rank_position': rank_position,
								'manning_agency': manning_agency,
								'employer_principal': employer_principal,
								'address_contact_info_manning_agen': address_contact_info_manning_agen,
								'vessel_name': vessel_name,
								'vessel_type': vessel_type,
								'grt': grt,
								'date_from': date_from,
								'date_to': date_to,
								'duties_and_responsibility': duties_and_responsibility,
							}
							applicant_previous_employment_val.append((0, 0, applicant_previous_employment_line_data))
				kw['applicant_previous_employment_ids'] = applicant_previous_employment_val				

			# Applicant Social Media 
			applicant_socialmedia_ids = kw.get('applicant_socialmedia_ids')
			if applicant_socialmedia_ids:
				socialmedia_val = []
				socialmedia_data = json.loads(kw['applicant_socialmedia_ids'])
				if socialmedia_data:
					for socialmedia_line in socialmedia_data:
						socialmedia_id = socialmedia_line.get('socialmedia_id')
						name = socialmedia_line.get('name')
						
						if not socialmedia_id or not name:
							error = _("Missing required fields for applicant social media details!")
							return json.dumps({
								'error': error,
							})
						else:
							socialmedia_line_data = {
								'socialmedia_id': socialmedia_id,
								'name': name,
							}
							socialmedia_val.append((0, 0, socialmedia_line_data))
				kw['applicant_socialmedia_ids'] = socialmedia_val

			# Job ID
			job_id = kw.get('job_id')
			if job_id:
				job_rec = request.env['hr.job'].sudo().search([('id','=',job_id)])
				if job_rec:
					kw['job_id'] = job_rec.id
					kw['department_id'] = job_rec.department_id.id or False

			# _logger.info(kw)
			id_record = request.env['hr.applicant'].sudo().create(kw)
			return json.dumps({'id': id_record.id})

	@http.route('/jobs/apply/add-family', type='http', auth='public', website=True)
	def apply_add_family(self, **kw):
		return

	@http.route('/contactus-thank-you', type='http', auth='public', website=True)
	def contactus_thank_you(self, **kw):
		print("kw>", kw)
		
		return request.render('ibas_bahia_website.application_thanks', {})

	@http.route('/jobs/apply/<model("hr.job"):job>', type='http', auth="public", website=True)
	def jobs_apply(self, job):
		error = {}
		default = {}
		attachment = http.request.env['ir.attachment'].sudo().search([('name', '=', 'Application-Form-rev2.docx')])

		model_jobs = request.env['hr.job'].sudo().search([])
		job_rec = request.env['hr.job'].sudo().search([])
		nationality_rec = request.env['res.country'].sudo().search([])
		familyrelation_rec = request.env['hr.familyrelations'].sudo().search([])
		level_rec = request.env['hr.recruitment.degree'].sudo().search([])
		documenttype_rec = request.env['hr.documenttype'].sudo().search([])
		social_media_rec = request.env['hr.socialmedia.config'].sudo().search([])

		str_url =""

		if 'ibas_bahia_website_error' in request.session:
			error = request.session.pop('ibas_bahia_website_error')
			default = request.session.pop('ibas_bahia_website_default')

		return request.render("ibas_bahia_website.apply_template", {
			'job': job,
			'error': error,
			'default': default,
			'jobs':model_jobs,
			'url_link': str_url,
			'job_rec': job_rec,
			'nationality_rec': nationality_rec,
			'familyrelation_rec': familyrelation_rec,
			'level_rec': level_rec,
			'social_media_rec': social_media_rec,
		})

	def check_date_format(self, date_string):
		format = "%m/%d/%Y"

		res = True
		try:
			res = bool(datetime.strptime(test_str, format))
		except ValueError:
			res = False




	