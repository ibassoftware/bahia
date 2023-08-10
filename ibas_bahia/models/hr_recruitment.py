 # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError, except_orm, Warning


class HRRecruitmentDegree(models.Model):
	_name = 'hr.recruitment.degree'	
	_description = 'HR Recruitment Degree'
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
		if 'name' in vals:
			vals['name'] =  "[" + vals['abbreviation'] + "]" + " " + vals['description']
		else: 
			vals.update({'name': "[" + vals['abbreviation'] + "]" + " " + vals['description']})                   
		new_record = super(hrRecruitment, self).create(vals)
		return new_record  

class HRRecruitmentSource(models.Model):
	_inherit = 'hr.recruitment.source'	

	name = fields.Char()

class HRRecruitmentStage(models.Model):
	_inherit = 'hr.recruitment.stage'	

	department_id = fields.Many2one('hr.department', string='Specific to a Department', help="Stages of the recruitment process may be different per department. If this stage is common to all departments, keep this field empty.")

class HRRecruitmentDegree(models.Model):
	_inherit = 'hr.recruitment.degree'	

	show_in_website_application = fields.Boolean()

class HRJon(models.Model):
	_inherit = 'hr.job'	

	message_last_post = fields.Datetime(string='Last Message Date')
	# survey_id = fields.Many2one('survey', 'Interview Form', help="Choose an interview form for this job position and you will be able to print/answer this interview from all applicants who apply for this job")

