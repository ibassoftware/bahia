# -*- encoding: utf-8 -*-
from odoo import models, fields, api
#from openerp.osv import fields, osv
from odoo.tools.translate import _

from odoo import SUPERUSER_ID
from odoo import tools
from odoo.modules.module import get_module_resource

from odoo.exceptions import except_orm, Warning, RedirectWarning,ValidationError


SCORE_MARK = [('1', 'Poor'),
			  ('2', 'Satisfactory'),
			  ('3', 'Good'),
			  ('4', 'Very Good'),
			  ('5', 'Excellent'),
			  ]

FINAL_INTERVIEW = [('1', 'HIRABLE'),
				   ('2', 'CAN BE CONSIDERED'),
				   ('3', 'N/A - DID NOT MEET HIRING CRITERIA'),
			  ]

class HrApplicantEvaluation(models.Model):
	_name = 'hr.applicant.evaluation'

	#fields.Char(related="partner_id.email", string="Email", store=True)
	#default_stock_location = fields.Many2one('stock.location',related='warehouse_id.lot_stock_id', string='Default Stock Location')

	name = fields.Char(related="employment_application_id.partner_name",
					   string="Name of Applicant")

	employment_application_id = fields.Many2one('hr.applicant')

	evaluation_date = fields.Date("Date of Evaluation", default=fields.Date.today())

	job_applied_id =  fields.Many2one('hr.job',related='employment_application_id.job_id', 
									  string='Position Applied', 
									  store=True)

	job_approved_id = fields.Many2one('hr.job',
									  'Position Approved')

	#Initial Verification
	has_photo_copies_doc = fields.Boolean('Has Photo Copies of Documents')
	photo_copies_doc = fields.Char('Photo Copies of Documents')
	has_check_poea_wathclist = fields.Boolean('Has POEA Watchlist')
	date_verified = fields.Date("Date Verified")

	#Employment History
	company_name_1 = fields.Char('Company Name')
	company_name_2 = fields.Char('Company Name')

	contact_person_1 = fields.Char('Contact Person')
	contact_person_2 = fields.Char('Contact Person')

	remarks_1 = fields.Text('Remarks')
	remarks_2 = fields.Text('Remarks')
	remarks_3 = fields.Text('Remarks')

	#Interview
	service_minded = fields.Selection(SCORE_MARK, 'Service Minded')
	safety_awareness = fields.Selection(SCORE_MARK, 'Safety Awareness')
	job_familiarity = fields.Selection(SCORE_MARK, 'Job Familiarity')
	technical_skills = fields.Selection(SCORE_MARK, 'Technical Skills')

	pysical_appearance = fields.Selection(SCORE_MARK, 'Physical Appearance')
	politeness = fields.Selection(SCORE_MARK, 'Politeness')
	neatness = fields.Selection(SCORE_MARK, 'Neatness')
	attentiveness = fields.Selection(SCORE_MARK, 'Attentiveness')
	oral_english = fields.Selection(SCORE_MARK, 'Oral English')

	interview_remarks = fields.Text('Remarks')

	marlins_proficiency = fields.Integer('Service Minded (%)')
	listening = fields.Integer('Listening (%)')
	grammar = fields.Integer('Grammar (%)')
	vocabulary = fields.Integer('Vocabulary (%)')	
	time_number = fields.Integer('Time and Number (%)')
	readings = fields.Integer('Readings (%)')
	pronounciation = fields.Integer('Pronounciation (%)')
	assesment_total = fields.Integer('Total (%)')

	overall_english_spoken = fields.Integer('Overall level of English Spoken (%)')


	overall = fields.Integer('Overall (%)')


	other_remarks = fields.Text('Other Remarks')




	interviewed_1_by_id  = fields.Many2one('res.users')
	interviewed_1_by_date = fields.Date("Date")

	verified_by_id  = fields.Many2one('res.users')
	verified_by_date = fields.Date("Date")

	interviewed_2_by_id  = fields.Many2one('res.users')
	interviewed_2_by_date = fields.Date("Date")

	conducted_1_by_id  = fields.Many2one('res.users')
	conducted_1_by_date = fields.Date("Date")

	conducted_2_by_id  = fields.Many2one('res.users')
	conducted_2_by_date = fields.Date("Date")

	conducted_3_by_id  = fields.Many2one('res.users')
	conducted_3_by_date = fields.Date("Date")

	hr_applicant_evaluation_ces_ids = fields.One2many('hr.applicant.evaluation.ces','hr_applicant_evaluation_id', readonly=False,copy=False)

	final_interview = fields.Selection(FINAL_INTERVIEW, 'Rate')


class HrCES(models.Model):
	_name = 'hr.applicant.evaluation.ces'


	hr_applicant_evaluation_id  = fields.Many2one('hr.applicant.evaluation')
	name = fields.Char('Function', required = True)
	score = fields.Integer('Score', required = True)

