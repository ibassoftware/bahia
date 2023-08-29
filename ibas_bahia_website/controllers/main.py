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

    @http.route('/job/apply', type="http", auth="public", website=True)
    def start_apply(self, **kw):
        # value = {}
        # value['name'] = 'Applicant'
        # # value['accept_privacy_policy'] = True
        # applicant = request.env['hr.applicant'].sudo().create(value)
        job_rec = request.env['res.users'].sudo().search([])
        nationality_rec = request.env['res.country'].sudo().search([])
        return http.request.render('ibas_bahia_website.apply_template', {
            'job_rec': job_rec,
            'nationality_rec': nationality_rec,
            # 'applicant': applicant,
        })

    @http.route('/job/apply/execute', type='http', auth='public', website=True)
    def apply_execute(self, **kw):
        _logger.info("WOOW")
        

        Applicant = request.env['hr.applicant']

        image_applicant = kw.get('image_1920')
        image_filename = kw.get('image_1920').filename
        image_data = image_applicant.read()

        image_value = False
        if image_applicant:
            _logger.info("image_applicant")
            _logger.info(image_filename)
            image_value = base64.b64encode(image_data)
            kw['image_1920'] = image_value.decode('ascii')

        # _logger.info(image_applicant)
        # _logger.info(image_value)

        _logger.info(kw)
        
        request.env['hr.applicant'].sudo().create(kw)
        return request.render('ibas_bahia_website.application_thanks', {})

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


    