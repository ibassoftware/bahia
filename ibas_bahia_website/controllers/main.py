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




