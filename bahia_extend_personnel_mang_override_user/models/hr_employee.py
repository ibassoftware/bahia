# -*- encoding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools.translate import _
import datetime
import logging
_logger = logging.getLogger(__name__)

DATE_NOW = datetime.datetime.now()

class ExtendHrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def create(self, vals):
    	res = super(ExtendHrEmployee, self).create(vals)
    	if res:
    		model_userinfo = self.env['res.users'].search([('id','=', res.user_id.id)])
    		employee_contract_number = res.employee_number
    		if res.employee_contract_number != 'N/A':
    			employee_contract_number = res.employee_contract_number
    		new_loggin_name = res.last_name.upper() + '' + employee_contract_number
    		if model_userinfo:
    			model_userinfo.write({
    				'login': new_loggin_name,
    				'password':new_loggin_name,})
    	return res




    @api.multi
    def write(self, vals):
    	res = super(ExtendHrEmployee, self).write(vals)
    	if res:
    		if vals.has_key('employee_contract_number') or vals.has_key('last_name'):
    			model_userinfo = self.env['res.users'].search([('id','=', self.user_id.id)])
    			new_loggin_name = self.last_name.upper() + '' + self.employee_contract_number
    			model_userinfo.write({
    				'login': new_loggin_name,
    				'password':new_loggin_name,
    				})
    	return True