# -*- coding: utf-8 -*-
import importlib
from openerp import models, fields,api
class HrEmployeeExtend(models.Model):
	_inherit = 'hr.employee'

	employee_e_register_number = fields.Char('E-Registration Number')
	employee_e_reg_num_username = fields.Char('User Name')
	employee_e_reg_num_password = fields.Char('Password')


#class hrsignonoffReportMenu(models.Model):
#	 _inherit = 'hr.signonoff.report.menu'
	
#	is_with_remarks = fields.Boolean('With Remarks', default = False)



