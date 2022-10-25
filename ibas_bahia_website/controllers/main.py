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

import logging
import xlrd
import os, sys, traceback
from collections import OrderedDict


import pytz


_logger = logging.getLogger(__name__)

class WebsitePopUpPrivacyPolicy(http.Controller):

    @http.route(['/page/privacy_policy'], type='http', auth="public", website=True)
    def privacy_policy(self):
        return request.render("ibas_bahia_website.page_policy_popup", {})


class BahiasApplicationForm(http.Controller):

    @http.route('/start-apply', type="http", auth="public", website=True)
    def customer_registration(self, **kw):
        # value = {}
        # value['name'] = 'Applicant'
        # # value['accept_privacy_policy'] = True
        # applicant = request.env['hr.applicant'].sudo().create(value)
        job_rec = request.env['res.users'].sudo().search([])
        nationality_rec = request.env['res.country'].sudo().search([])
        return http.request.render('ibas_bahia_website.application_form_template', {
            'job_rec': job_rec,
            'nationality_rec': nationality_rec,
            # 'applicant': applicant,
        })

    @http.route('/contactus-thank-you', type='http', auth='public', website=True)
    def create_customer(self, **kw):
        print("kw>", kw)
        # if kw.get("customer_password") != kw.get("customer_confirm_password"):
        #     return request.render('fpa_project.registration_error', {})
        # else:
        # request.env['res.partner'].sudo().create(kw)
        request.env['hr.applicant'].sudo().create(kw)
        return request.render('ibas_bahia_website.application_thanks', {})




