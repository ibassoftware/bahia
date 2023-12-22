# -*- encoding: utf-8 -*-
from odoo import models, fields, api

class DataMigration(models.TransientModel):
	_name ='hr.config.data.migration'

	name = fields.Char('Name', default='Data Migration Name')

	def changeEmployeeName(self):
		employee_model = self.env['hr.employee'].search([])
		
		for employee in employee_model:
			if employee.first_name == False:
				employee.first_name=''
			if employee.middle_name == False:
				employee.middle_name=''
			if employee.last_name == False:
				employee.last_name=''			
			employee.name =  employee.last_name + ", " +  employee.first_name + " " + employee.middle_name   
