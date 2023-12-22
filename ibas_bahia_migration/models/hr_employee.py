# -*- encoding: utf-8 -*-
from odoo import models, fields, api

class HrEmployeeMigration(models.Model):
	_inherit = 'hr.employee'

	# For API use
	def updateEmployeeName(self):
		for employee in self:
			first_name = ''
			middle_name = ''
			last_name = ''

			if employee.first_name == False:
				employee.first_name=''
			else:
				first_name = employee.first_name

			if employee.middle_name == False:
				employee.middle_name=''
			else:
				middle_name = employee.middle_name

			if employee.last_name == False:
				employee.last_name=''
			else:
				last_name = employee.last_name

			if first_name or middle_name or last_name:
				employee.name =  last_name + ", " +  employee.first_name + " " + employee.middle_name
		return True