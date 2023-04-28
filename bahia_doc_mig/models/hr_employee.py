# -*- coding: utf-8 -*-
import importlib
from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class HrEmployeeExtend(models.Model):
    _inherit = 'hr.employee'

    @api.multi 
    def get_file_personal_data(self):
    	_logger.info("TESST")
    	return {
    		'type' : 'ir.actions.act_url',
    		'url': '/web/binary/download_document?model=hr.employee&field=legacy_doc_2&id=%s&filename=filename2'%(self.id),
    		'target': 'self',
    	}