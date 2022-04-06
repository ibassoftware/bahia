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


#class HrEmployeeExtend(models.Model):
#	_inherit = 'hr.employee'
#
#	@api.multi
#	def write(self, vals):
#		res = super(HrEmployeeExtend, self).write(vals)
#		if res:
#			values = {'status': 'draft','title': u'Be notified about','message': "Do not forget to send notification in 21.04.17",'partner_ids': [(6, 0, [1])]}
#			self.env['popup.notification'].create(values)
#		return res

class seafarerDocuments(models.Model):
	_inherit ='hr.employee_documents'

	#@api.one
	#def fileUpload(self):
		#f self.document:
		#	self.filename = self.document.name
		#else:
		#	self.filename = 'No Document Type'
		#if len(self.document_number) > 0:
		#	self.filename += ' ' + self.document_number + ' .jpg' 
		#else:
	#		self.filename += ' None.jpg'
	#	self.filename="FFFFFF.jpg"


	#filename = fields.Char(string='file name',store=False, readonly = True,compute ='fileUpload')
	filename = fields.Char(string='file name')
	file_upload = fields.Binary('Document File')

class HrEmployeeMedicalRecords(models.Model):
	_inherit = 'hr.employee_medical_records'
	filename = fields.Char(string='file name')
	file_upload = fields.Binary('Document File')

class HrEmployeeLicenses(models.Model):
	_inherit = 'hr.employeelicenses'
	filename = fields.Char(string='file name')
	file_upload = fields.Binary('Document File')