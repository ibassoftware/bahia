# -*- encoding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools.translate import _
import datetime
import logging
_logger = logging.getLogger(__name__)

DATE_NOW = datetime.datetime.now()

class ExtendHrApplicant(models.Model):
    _inherit = 'hr.applicant'

    @api.model
    def checkAgingApplication(self):
    	RESERVER_POOLING = 3
    	DAYS_TO_MOVE =90
    	REJECTED = 6
    	applicant_obj = self.env['hr.applicant'].search([('stage_id', '=',RESERVER_POOLING)])

    	if applicant_obj:
    		for applicant in applicant_obj:
    			application_date = datetime.datetime.strptime(applicant.write_date, '%Y-%m-%d %H:%M:%S')

    			days_diff = DATE_NOW.date() - application_date.date()
    			if days_diff.days >= DAYS_TO_MOVE:
    				applicant.update({
    						'stage_id': 6
    					})

    	applicant_obj = self.env['hr.applicant'].search([('stage_id', '=',REJECTED)])

    	if applicant_obj:
    		for applicant in applicant_obj:
				applicant.update({
						'active': False
					})

class EducationDegrees(models.Model):
	_inherit='hr.recruitment.degree'

	show_in_website_application = fields.Boolean('Show in Website Application', default=False)
