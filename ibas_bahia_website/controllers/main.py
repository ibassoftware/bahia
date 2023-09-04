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

	@http.route('/jobs/apply', type="http", auth="public", website=True)
	def start_apply(self, **kw):
		# value = {}
		# value['name'] = 'Applicant'
		# # value['accept_privacy_policy'] = True
		# applicant = request.env['hr.applicant'].sudo().create(value)
		job_rec = request.env['res.users'].sudo().search([])
		nationality_rec = request.env['res.country'].sudo().search([])
		familyrelation_rec = request.env['hr.familyrelations'].sudo().search([])
		level_rec = request.env['hr.recruitment.degree'].sudo().search([])
		social_media_rec = request.env['hr.socialmedia.config'].sudo().search([])
		return http.request.render('ibas_bahia_website.apply_template', {
			'job_rec': job_rec,
			'nationality_rec': nationality_rec,
			'familyrelation_rec': familyrelation_rec,
			'level_rec': level_rec,
			'social_media_rec': social_media_rec,
		})

	@http.route('/jobs/apply/execute', type='http', auth='public', website=True)
	def apply_execute(self, **kw):
		Applicant = request.env['hr.applicant']

		# Validation: Check for Name, Birthdate and Email Address
		applicant_name = kw.get('name')
		applicant_date_of_birth = kw.get('date_of_birth')
		applicant_email_from = kw.get('email_from')

		duplicate_applicant_id = request.env['hr.applicant'].sudo().search([('name', '=', applicant_name), ('date_of_birth', '=', applicant_date_of_birth)])
		
		if applicant_email_from:
			duplicate_applicant_id = request.env['hr.applicant'].sudo().search([('name', '=', applicant_name), ('date_of_birth', '=', applicant_date_of_birth), ('email_from', '=', applicant_email_from)])
		
		if duplicate_applicant_id:
			return request.render('ibas_bahia_website.application_duplicate', {})
		else:
			# Applicant Image
			image_applicant = kw.get('image_1920')
			image_filename = kw.get('image_1920').filename
			image_data = image_applicant.read()
			image_value = False
			if image_applicant:
				image_value = base64.b64encode(image_data)
				kw['image_1920'] = image_value.decode('ascii')

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

			# Applicant Social Media 
			applicant_socialmedia_ids = kw.get('applicant_socialmedia_ids')
			if applicant_socialmedia_ids:
				socialmedia_data = json.loads(kw['applicant_socialmedia_ids'])
				socialmedia_val = [(0, 0, socialmedia_line) for socialmedia_line in socialmedia_data]
				kw['applicant_socialmedia_ids'] = socialmedia_val

			request.env['hr.applicant'].sudo().create(kw)
			return request.render('ibas_bahia_website.application_thanks', {})

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

		model_jobs = http.request.env['hr.job'].sudo().search([])

		str_url =""

		if 'ibas_bahia_website_error' in request.session:
			error = request.session.pop('ibas_bahia_website_error')
			default = request.session.pop('ibas_bahia_website_default')

		return request.render("ibas_bahia_website.application_form_template", {
			'job': job,
			'error': error,
			'default': default,
			'jobs':model_jobs,
			'url_link': str_url,
		})


	