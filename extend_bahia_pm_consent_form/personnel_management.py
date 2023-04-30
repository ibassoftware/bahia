# -*- coding: utf-8 -*-
import importlib
from openerp import models, fields,api
from openerp.exceptions import except_orm, Warning, RedirectWarning,ValidationError

import datetime
import os
import sys
import base64

#FOR EXCEL FILE
import xlwt
from cStringIO import StringIO

YEAR = 365
MONTH = 30
#ALT_255 = '            ' # ALR+255 is a Special Characters in ASCII
ALT_255 =''
DATE_NOW = datetime.datetime.now()
INT_ID_NOW = 0

class HrEmployeeExtend(models.Model):
	_inherit = ['hr.employee']

	@api.multi 
	def download_file_consent_form(self):
		return {
			'type' : 'ir.actions.act_url',
			'url': '/web/binary/download_doc_pdf?model=hr.employee&field=legacy_doc_4&id=%s&filename=%s' % (self.id, self.filename4),
			'target': 'self',
		}

	def generateFile(self,vals):
		dt_tm_filename = DATE_NOW.strftime("%m%d%Y%H%M%S")
		byte_arr = base64.b64encode('Dummy File')
		document_binary = ""
		bln_must_save = False	
		res = super(HrEmployeeExtend, self).generateFile(vals)

		if vals.has_key('legacy_doc_4'):
			str_filename = self.filename4.rstrip('.pdf') + '_' + dt_tm_filename + '.pdf'
			FILENAME_DIR = "/opt/DataFiles/" + str_filename
			if not isinstance(vals['legacy_doc_4'], bool):
				document_binary = vals['legacy_doc_4']
				byte_arr = base64.b64encode(str_filename)
				vals['legacy_doc_4'] = byte_arr
				with open(FILENAME_DIR, "wb") as f:
					f.write(base64.b64decode(document_binary))
			else:
				os.remove(FILENAME_DIR)
		return res

	@api.one
	def legacy_doc4_getFilename(self):
		if len(self.employee_number) > 0:
			self.filename4 = self.employee_number + '_ConsentForm.pdf'
		else:
			self.filename4 = 'filename_ConsentForm.pdf'

	@api.multi
	def write(self,vals):
		if vals.has_key('legacy_doc_4'):
			if vals['legacy_doc_4']:
				vals['has_consentform'] = True
			else:
				vals['has_consentform'] = False
		#else:
		#	vals['has_consentform'] = False

		res = super(HrEmployeeExtend, self).write(vals)
		return res


	@api.one
	def updateWithConsentForm(self):
		if self.has_consentform:
			self.write({'has_consentform':False})
		else:
			self.write({'has_consentform':True})

	legacy_doc_4 = fields.Binary('Consent Form', filters='*.pdf,*.docx,*.doc')
	filename4 = fields.Char('file name', readonly = True,store = False,compute ='legacy_doc4_getFilename')
	has_consentform = fields.Boolean('With Consent Form', default=False)
