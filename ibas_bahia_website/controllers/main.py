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
			_logger.info("Duplicate application!")
			error = _("Duplicate application! One applicant, one application only.")
			return json.dumps({
				'error': error,
			})
		else:
			# Applicant Image
			image_applicant = kw.get('image_1920')
			image_filename = False
			image_data = False
			image_value = False
			if image_applicant:
				image_filename = kw.get('image_1920').filename
				image_data = image_applicant.read()
				image_value = base64.b64encode(image_data)
				kw['image_1920'] = image_value.decode('ascii')

			# Applicant Date of Birth
			if applicant_date_of_birth:
				kw['date_of_birth'] = applicant_date_of_birth

			# Applicant Family
			applicant_families = kw.get('applicant_families')
			if applicant_families:
				family_data = json.loads(applicant_families)
				family_val = [(0, 0, family_line) for family_line in family_data]
				kw['applicant_families'] = family_val

			# Applicant Education
			applicant_education = kw.get('applicant_education')
			if applicant_education:
				education_data = json.loads(applicant_education)
				education_val = [(0, 0, education_line) for education_line in education_data]
				kw['applicant_education'] = education_val

			# Applicant Record Books
			applicant_document_ids = kw.get('applicant_document_ids')
			if applicant_document_ids:
				record_books_data = json.loads(applicant_document_ids)
				record_books_val = [(0, 0, record_books_line) for record_books_line in record_books_data]
				kw['applicant_document_ids'] = record_books_val

			# References - Employed Relatives
			applicant_employed_relatives_ids = kw.get('applicant_employed_relatives_ids')
			if applicant_employed_relatives_ids:
				employed_relatives_data = json.loads(applicant_employed_relatives_ids)
				employed_relatives_val = [(0, 0, employed_relatives_line) for employed_relatives_line in employed_relatives_data]
				kw['applicant_employed_relatives_ids'] = employed_relatives_val

			# References - Previouse Application
			applicant_previous_application_ids = kw.get('applicant_previous_application_ids')
			if applicant_previous_application_ids:
				applicant_previous_application_data = json.loads(applicant_previous_application_ids)
				applicant_previous_application_val = [(0, 0, applicant_previous_application_line) for applicant_previous_application_line in applicant_previous_application_data]
				kw['applicant_previous_application_ids'] = applicant_previous_application_val

			# References - Previouse Employment
			applicant_previous_employment_ids = kw.get('applicant_previous_employment_ids')
			if applicant_previous_employment_ids:
				applicant_previous_employment_data = json.loads(applicant_previous_employment_ids)
				applicant_previous_employment_val = [(0, 0, applicant_previous_employment_line) for applicant_previous_employment_line in applicant_previous_employment_data]
				kw['applicant_previous_employment_ids'] = applicant_previous_employment_val

			# Applicant Social Media 
			applicant_socialmedia_ids = kw.get('applicant_socialmedia_ids')
			if applicant_socialmedia_ids:
				socialmedia_data = json.loads(kw['applicant_socialmedia_ids'])
				socialmedia_val = [(0, 0, socialmedia_line) for socialmedia_line in socialmedia_data]
				kw['applicant_socialmedia_ids'] = socialmedia_val

			# Job ID
			job_id = kw.get('job_id')
			_logger.info("HEYY")
			_logger.info(job_id)
			if job_id:
				job_rec = request.env['hr.job'].sudo().search([('id','=',job_id)])
				if job_rec:
					_logger.info(job_rec)
					kw['job_id'] = job_rec.id
					kw['department_id'] = job_rec.department_id.id False

			_logger.info(kw)
			id_record = request.env['hr.applicant'].sudo().create(kw)
			# return request.render('ibas_bahia_website.application_thanks', {})
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




	