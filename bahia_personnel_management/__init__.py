# -*- encoding: utf-8 -*-
import sys

# Mock deprecated openerp.addons.web.http module
import openerp.http
sys.modules['openerp.addons.web.http'] = openerp.http
http = openerp.http

# from . import controllers

import hr_parameter_model
import hr_recruitment_seabased
import user_defined_exception
import hr_recruitment
import reports