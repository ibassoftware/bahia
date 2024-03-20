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

	def createEmployeeUser(self):
		for employee in self:
			if not employee.user_id:
				if employee.employee_contract_number != 'N/A':
					new_loggin_name = employee.last_name + '_' + str(employee.employee_contract_number)
				else:
					new_loggin_name = employee.last_name + '_' + str(employee.employee_number)
				if isinstance(employee.middle_name, bool):
					new_user_fullname = employee.first_name + ' ' + employee.last_name
				else:
					new_user_fullname = employee.first_name + ' '+ employee.middle_name + ' ' + employee.last_name

				model_userinfo = self.env['res.users']

				id_user = model_userinfo.create({
				    'name': new_user_fullname,
				    'login': new_loggin_name,
				    'password': new_loggin_name,
				    'groups_id':   [(6,0,[ref('base.group_portal')])],})        
				employee.user_id = id_user.id