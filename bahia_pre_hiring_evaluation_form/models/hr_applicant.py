# -*- encoding: utf-8 -*-
from openerp import models, fields, api
#from openerp.osv import fields, osv
from openerp.tools.translate import _

from openerp import SUPERUSER_ID
from openerp import tools
from openerp.modules.module import get_module_resource
from openerp.osv import fields as osv_fields, osv as osv_osv


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    @api.one
    def _interview_form_count(self):
		interview_form_model = self.env['hr.applicant.evaluation']
		self.interview_count =  interview_form_model.search_count([('employment_application_id', '=', self.id)])
		
    interview_count =  fields.Integer('Interview Form', store = False, compute = "_interview_form_count")


