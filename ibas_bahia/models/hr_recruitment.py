 # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError, except_orm, Warning


class hrRecruitment(models.Model):
	_name = 'hr.recruitment.degree'	
	_inherit = 	'hr.recruitment.degree' 

	@api.onchange('abbreviation', 'description')
	def onchangeName(self):
		if not isinstance( self.abbreviation, bool) and not isinstance( self.description, bool):
			self.name = "[" + self.abbreviation + "]" + " " + self.description

	type_code = fields.Char('Type Code', required=True)
	type_name = fields.Char('Type Name', required=True)
	description = fields.Char('Description', required=True)
	abbreviation = fields.Char('Abbreviation', required=True)

	@api.model
	def create(self, vals):
		if vals.has_key('name'):
			vals['name'] =  "[" + vals['abbreviation'] + "]" + " " + vals['description']
		else: 
			vals.update({'name': "[" + vals['abbreviation'] + "]" + " " + vals['description']})                   
		new_record = super(hrRecruitment, self).create(vals)
		return new_record  
