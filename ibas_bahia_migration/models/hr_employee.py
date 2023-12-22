# -*- encoding: utf-8 -*-
from odoo import models, fields, api

class HrEmployeeMigration(models.Model):
	_inherit = 'hr.employee'

	# For API use
	def updateEmployeeName(self):
		for employee in self:
			if employee.first_name == False:
				employee.first_name=''
			if employee.middle_name == False:
				employee.middle_name=''
			if employee.last_name == False:
				employee.last_name=''			
			employee.name =  employee.last_name + ", " +  employee.first_name + " " + employee.middle_name