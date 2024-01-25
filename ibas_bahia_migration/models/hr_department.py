# -*- encoding: utf-8 -*-
from odoo import models, fields, api

class HrEmployeeDepartment(models.Model):
	_inherit = 'hr.department'

	def compute_complete_name(self):
		for record in self:
			record._compute_complete_name()
		return True