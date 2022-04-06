from openerp import models, fields,api
from openerp.exceptions import except_orm, Warning, RedirectWarning,ValidationError

import os
import shutil
import datetime
import tarfile
import time

class ExternalFileBackup(models.Model):
	_name = 'external.file.backup'
	_description ='Seafarer Documents'

	name  = fields.Char('DB Name', required=True)
	dir_file = fields.Char('Directory File Backup', required=True, help='Directory where are the file/s to be backup')
	dir_original_file = fields.Char('Seafarer Document Directory', required=True, help='Directory where are the Save Seafarer Documents')
	date_to_be_backup =fields.Date('Files Date', required=True, help='Dates of the File to be Backup.')

	@api.one
	def manual_backup(self):
		self.create_backup(is_manual=True, backup_path= self.dir_file, file_path= self.dir_original_file, file_creation_date=self.date_to_be_backup)

	@api.model
	def schedule_backup(self):
		obj = self.env.ref('bahia_external_file_backup.bmis_data')
		date_to_be_backup = datetime.datetime.strptime(obj.date_to_be_backup, '%Y-%m-%d')
		self.create_backup(is_manual=False, backup_path= obj.dir_file, file_path= obj.dir_original_file, file_creation_date=obj.date_to_be_backup)
		new_date_to_be_backup =  datetime.datetime.strftime(date_to_be_backup + datetime.timedelta(1), '%Y-%m-%d')
		obj.update({
				'date_to_be_backup' : new_date_to_be_backup})

	@api.model
	def create_backup(self, is_manual=False, backup_path='', file_path='', file_creation_date=''):
		bln_no_records = True
		sys_audit_log_obj = self.env['sys.audit.log'].search([('name', 'in', ['Confidential Reports', 'Personal Data', 'Personal Summary', 'Consent Form'])])
		if sys_audit_log_obj:
			dir_backup =backup_path + '%s_seafarer_file_back_up' % (file_creation_date)#(time.strftime('%Y%m%d_%H_%M_%S')) 
			os.makedirs(dir_backup)
			for rec in sys_audit_log_obj:
				creation_date = datetime.datetime.strptime(rec.create_date, '%Y-%m-%d %H:%M:%S').date()
				date_to_be_backup = datetime.datetime.strptime(file_creation_date, '%Y-%m-%d').date()
				if creation_date == date_to_be_backup:
					bln_no_records = False
					#Check if Files Exists in Saving Directory
					if rec.new_value:
						if os.path.exists(file_path + rec.new_value):
							shutil.copy(file_path + rec.new_value, dir_backup + '/' + rec.new_value)
					#raise Warning(type(rec.create_date))
		try:
			os.removedirs(dir_backup)
		except Exception, e:
			pass
		return True


class ExternalBackupDetail(models.Model):
	_name ='external.file.backup.detail'


	name = fields.Char('DB Name')
	date = fields.Date('Dates')
	backup_path = fields.Char('Backup Path')