# -*- coding: utf-8 -*-
from openerp import models,fields,api
from openerp import tools
from openerp.report import report_sxw
import datetime
import base64
from openerp.exceptions import except_orm, Warning, RedirectWarning,ValidationError


#FOR EXCEL FILE
import xlwt
from cStringIO import StringIO

PASSPORT_CODE = 'P'
SSRIB_CODE = 'S'
ACTIVE_ON_BOARD = '00001'

YEAR = 365
MONTH = 30
SECOND_PER_MINUTE = 60
MINUTE_PER_HOUR = 60
HOUR_PER_DAY = 24
FIFTY_MINUTES_TO_SECOND = 3540
DATE_NOW = datetime.datetime.now()

import os
from ftplib import FTP
import ftplib
import logging
_logger = logging.getLogger(__name__)



HOST = 'mybahiashipping.com'
USER = 'datagenesis'
PASSWORD = 'datagen=2016'

PDF_DIRECTORY = '/backend/_lib/file/doc/'
PICTURE_DIRECTORY = '/backend/_lib/file/img/'
APPLICANT_DIRECTORY = '/backend/_lib/file/img/' # Sub Folder per Applicant must be seen in Applicant Column


PATH_TO_PASTE_PDF_DIRECTORY =  '/opt/DataFiles/'
#NOTE THIS WILL BE A TEMPORARY FILE DIRECTORY 
#DUE TO ODOO IS ATTACHING ITS FILE IN THE DATABASE
PATH_TO_PASTE_PICTURE_DIRECTORY =  '/opt/PICTURE/'
PATH_TO_PASTE_APPLICANT_DIRECTORY =  '/opt/RESUME/'
NO_PDF_FILE = '/opt/NO_PDF_FILE/'


class DataMigration(models.TransientModel):
	_name ='hr.config.data.migration'


	name = fields.Char('Name', default = 'Data Migration Name')


	@api.one
	def updateApplicantsNumber(self):
		applicant_model = self.env['hr.applicant'].search([])
		applicants_model  = applicant_model.sorted(key=lambda r: r.create_date, reverse=True)
		str_sequence = ''
		obj_sequence = self.env['ir.sequence'].search([('code','=', 'hr.applicant.sequence')])
		int_sequence = obj_sequence.number_next_actual

		for applicant in applicants_model:
			str_sequence = str(int_sequence).zfill(obj_sequence.padding)
			applicant.write({'application_number' : str_sequence})
			int_sequence +=1
		obj_sequence.write({'number_next_actual' : int_sequence})

	@api.one
	def changeEmployeeUserName(self):
		employee_model = self.env['hr.employee'].search([])
		i =1
		if len(employee_model) > 0:
			for employee in employee_model:
					# To Check if Employee Information has a User ID
					_logger.info('Updating %(emp)d out of %(tot)d' %{

						'emp' : i,
						'tot' : len (employee_model)

						})
					if employee.user_id:
						if employee.user_id.share == True:
							new_loggin_name = ''
							contract_number = employee.employee_number
							if employee.employee_contract_number !='N/A':
								contract_number = employee.employee_contract_number
							new_loggin_name = employee.last_name + '' + contract_number
							model_userinfo = self.env['res.users'].search([('id','=', employee.user_id.id)])
							model_userinfo.write({'login': new_loggin_name,'password':new_loggin_name,})

					#contract_number = ''
					#if not isinstance(employee.user_id,bool):
					#	if len(employee.user_id) > 0:
					#		if not isinstance(employee.employee_contract_number, bool):
					#			if len(employee.employee_contract_number) > 0:
					#				model_userinfo = self.env['res.users'].search([('id','=', employee.user_id.id)])
					#				#To Check if Contract Number has a PH
					#				if employee.employee_contract_number.find('PH', 0, len(employee.employee_contract_number)) > 0:
					#					new_loggin_name = employee.last_name + '_' + str(employee.employee_contract_number[employee.employee_contract_number.find('PH', 0, len(employee.employee_contract_number)): len(employee.employee_contract_number)])
					#				else:
					#					if len(employee.employee_contract_number) < 4:
					#						new_loggin_name = employee.last_name + '_' + employee.employee_contract_number.zfill(4) #str(employee.employee_contract_number[len(employee.employee_contract_number) -4 : len(employee.employee_contract_number)])
					#					else:
					#						new_loggin_name = employee.last_name + '_' + str(employee.employee_contract_number)#str(employee.employee_contract_number[len(employee.employee_contract_number) -4 : len(employee.employee_contract_number)])
					#				model_userinfo.write({'login': new_loggin_name,'password':new_loggin_name,})
					i +=1

									
	@api.one
	def changeEmployeeNameWithEmployeeNumber(self):
		employee_id_change = [32414,32416,38432,42991,25865,44980,42813,44994,38155,47096,25885,24565,24491,43105,24703,49127,33004,49329,46874,26269,26060,38153,25982,24602,45095,25995,24603,46317,42847,38200,38176,46391]
		employee_model = self.env['hr.employee'].search([('id', 'in', employee_id_change)])
		
		for employee in employee_model:
			if employee.first_name == False:
				employee.first_name=''
			if employee.middle_name == False:
				employee.middle_name=''
			if employee.last_name == False:
				employee.last_name=''			
			employee.name_related =  "[" + employee.employee_number +"] "   + employee.last_name + ", " +  employee.first_name + " " + employee.middle_name
			employee.name =  "[" + employee.employee_number +"] " + employee.last_name + ", " +  employee.first_name + " " + employee.middle_name   




	@api.one
	def changeEmployeeName(self):
		employee_model = self.env['hr.employee'].search([])
		
		for employee in employee_model:
			if employee.first_name == False:
				employee.first_name=''
			if employee.middle_name == False:
				employee.middle_name=''
			if employee.last_name == False:
				employee.last_name=''			
			employee.name_related = employee.last_name + ", " +  employee.first_name + " " + employee.middle_name
			employee.name =  employee.last_name + ", " +  employee.first_name + " " + employee.middle_name   

	@api.one
	def createFamilySorting(self):
		employee_model = self.env['hr.employee'].search([])
		
		for employee in employee_model:
			employee_families_model = self.env['hr.employee_families'].search([('employee_family_relationship_id','=', employee.id)])
			employee_families  = employee_families_model.sorted(key=lambda r: r.write_date)
			count =1
			for employee_family in employee_families:
				employee_family.relation_level = count			
				count +=1

	@api.one
	def creatLink(self):
		employee_model = self.env['hr.employee'].search([])
		for employee in employee_model:
			if not isinstance(employee.personal_file, bool):
				byte_arr = base64.b64encode(employee.personal_file)
				employee.write({
					'legacy_doc_2': byte_arr
					})				
			if not isinstance(employee.personalsummary_file, bool):
				byte_arr = base64.b64encode(employee.personalsummary_file)
				employee.write({
					'legacy_doc_3': byte_arr
					})				
			if not isinstance(employee.confidential_file, bool):
				byte_arr = base64.b64encode(employee.confidential_file)
				employee.write({
					'legacy_doc_1': byte_arr
					})

			#if not isinstance(employee.image_file, bool):
			#	byte_arr = base64.b64encode(employee.image)			

	@api.one 
	def updatePicture(self):
		#employee_model = self.env['hr.employee'].search([('id','=','23796')])
		employee_model = self.env['hr.employee'].search([])
		_logger.info('Start Updating Pics')
		for employee in employee_model:					
				if not isinstance(employee.image_file, bool):
					#cHECK IF FILE EXISTS
					_logger.info('Check File Exists ' + PATH_TO_PASTE_PICTURE_DIRECTORY + employee.image_file.strip(' '))
					is_exists = os.path.isfile(PATH_TO_PASTE_PICTURE_DIRECTORY + employee.image_file.strip(' '))
					#raise Warning(employee.image_file)
					if is_exists:
						_logger.info('Start Downloading the Image ' + PATH_TO_PASTE_PICTURE_DIRECTORY + employee.image_file.strip(' '))
						with open(PATH_TO_PASTE_PICTURE_DIRECTORY + employee.image_file.strip(' '), "rb") as f:
							text = f.read()
							byte_arr = base64.b64encode(text)
							#raise Warning(len(text))
							f.close()
						employee.write({
								'image': byte_arr,
							})
						_logger.info('Successfully Downloaded the Image ' + PATH_TO_PASTE_PICTURE_DIRECTORY + employee.image_file.strip(' '))

				else:
					_logger.info('No Picture define in ' + str(employee.employee_number))

	@api.one
	def generateData(self):
		employee_model = self.env['hr.employee'].search([])
		#employee_model = self.env['hr.employee'].search([('id','=',31571)])
	
		if len(employee_model) > 0:
			
			#Personal File
			for employee in employee_model:
				ftp = FTP(HOST,USER, PASSWORD)				
				try:

					if not isinstance(employee.personal_file, bool):
						split_file = employee.personal_file.split('.')

						if len(split_file[0]) >=4:						
								file_name_from_ftp =  employee.personal_file.replace(split_file[0],str(split_file[0]).zfill(11))     
						else:
								file_name_from_ftp =  employee.personal_file.replace(split_file[0],str(split_file[0]).zfill(10))  

						#ftp.cwd(PDF_DIRECTORY + file_name_from_ftp)
						ftp.cwd(PDF_DIRECTORY)
						local_filename = os.path.join(r"/opt/DataFiles/", employee.personal_file)
						lf = open(local_filename, "wb")
						res = ftp.retrbinary("RETR " + file_name_from_ftp, lf.write) #, 8*1024
						if not res.startswith('226 Transfer complete'):
							local_filename = os.path.join(r"/opt/DataFiles/NO_PDF_FILE/", "NO_PDF_FILE.txt")
							ef = open(local_filename, "wb")	
							ef.write("file from " + PDF_DIRECTORY + file_name_from_ftp + " has not been downloaded to " + "/opt/DataFiles/", employee.personal_file)
							ef.close()	

							local_filename = os.path.join(r"/opt/DataFiles/NO_PDF_FILE/", "QUERY_FOR_PDF_FILE.txt")	
							ef = open(local_filename, "wb")	
							ef.write(employee.employee_number)
							ef.close()	



						lf.close()
			
				except ftplib.error_perm:
					#local_filename = os.path.join(r"/opt/DataFiles/", employee.image_file)
					lf = open(NO_PDF_FILE + file_name_from_ftp + '.txt', "wb")
					lf.close()
					continue

	
			ftp.quit()

			#For Personal Summary
			for employee in employee_model:
				ftp = FTP(HOST,USER, PASSWORD)				
				try:
					if not isinstance(employee.personalsummary_file, bool):
						#Get the Personal Summary
						split_file = employee.personalsummary_file.split('.')
						if len(split_file[0]) >=4:	
								file_name_from_ftp =  employee.personalsummary_file.replace(split_file[0],str(split_file[0]).zfill(11))     
						else:
								file_name_from_ftp =  employee.personalsummary_file.replace(split_file[0],str(split_file[0]).zfill(10)) 

						ftp.cwd(PDF_DIRECTORY)
						local_filename = os.path.join(r"/opt/DataFiles/", employee.personalsummary_file)
						lf = open(local_filename, "wb")
						res = ftp.retrbinary("RETR " + file_name_from_ftp, lf.write)
						if not res.startswith('226 Transfer complete'):
							local_filename = os.path.join(r"/opt/DataFiles/NO_PDF_FILE/", "NO_PDF_FILE.txt")
							ef = open(local_filename, "wb")	
							ef.write("file from " + PDF_DIRECTORY + file_name_from_ftp + " has not been downloaded to " + "/opt/DataFiles/", employee.personalsummary_file)
							ef.close()	

							local_filename = os.path.join(r"/opt/DataFiles/NO_PDF_FILE/", "QUERY_FOR_PDF_FILE.txt")	
							ef = open(local_filename, "wb")	
							ef.write(employee.employee_number)
							ef.close()										
						lf.close()					
			
				except ftplib.error_perm:
					#local_filename = os.path.join(r"/opt/DataFiles/", employee.image_file)
					lf = open(NO_PDF_FILE + file_name_from_ftp + '.txt', "wb")
					lf.close()
					continue
	
			ftp.quit()		

			#For Confidential
			for employee in employee_model:
				ftp = FTP(HOST,USER, PASSWORD)				
				try:
					#Get the Confidential 
					if not isinstance(employee.confidential_file, bool):
						split_file = employee.confidential_file.split('.')
						if len(split_file[0]) ==4:	
								file_name_from_ftp =  employee.confidential_file.replace(split_file[0],str(split_file[0]).zfill(11))
						elif len(split_file[0]) < 4:
								file_name_from_ftp =  employee.confidential_file.replace(split_file[0],str(split_file[0]).zfill(10))
						elif len(split_file[0]) >4 and len(split_file[0]) <=11:	
								file_name_from_ftp =  employee.confidential_file
						else:
								file_name_from_ftp =  employee.confidential_file    

						ftp.cwd(PDF_DIRECTORY)
						local_filename = os.path.join(r"/opt/DataFiles/", employee.confidential_file)
						lf = open(local_filename, "wb")
						res = ftp.retrbinary("RETR " + file_name_from_ftp, lf.write)
						if not res.startswith('226 Transfer complete'):
							local_filename = os.path.join(r"/opt/DataFiles/NO_PDF_FILE/", "NO_PDF_FILE.txt")
							ef = open(local_filename, "wb")	
							ef.write("file from " + PDF_DIRECTORY + file_name_from_ftp + " has not been downloaded to " + "/opt/DataFiles/", employee.confidential_file)
							ef.close()	

							local_filename = os.path.join(r"/opt/DataFiles/NO_PDF_FILE/", "QUERY_FOR_PDF_FILE.txt")	
							ef = open(local_filename, "wb")	
							ef.write(employee.employee_number)
							ef.close()										
						lf.close()		
			
				except ftplib.error_perm:
					#local_filename = os.path.join(r"/opt/DataFiles/", employee.image_file)
					lf = open(NO_PDF_FILE + file_name_from_ftp + '.txt', "wb")
					lf.close()
					continue
	
			ftp.quit()



			#For Image
			for employee in employee_model:
				ftp = FTP(HOST,USER, PASSWORD)				
				try:
					#Get Employee Image
					#ftp.cwd(PDF_DIRECTORY + employee.confidential_file)
					if not isinstance(employee.image_file, bool):
						split_file = employee.image_file.split('.')
						if len(split_file[0]) >=4:	
								file_name_from_ftp =  employee.image_file.replace(split_file[0],str(split_file[0]).zfill(11))     
						else:
								file_name_from_ftp =  employee.image_file.replace(split_file[0],str(split_file[0]).zfill(10))     

						ftp.cwd(PICTURE_DIRECTORY)
						PATH_TO_PASTE_PICTURE_DIRECTORY
						local_filename = os.path.join(r"/opt/PICTURE/", employee.image_file)
						lf = open(local_filename, "wb")
						res = ftp.retrbinary("RETR " + file_name_from_ftp, lf.write)
						if not res.startswith('226 Transfer complete'):
							local_filename = os.path.join(r"/opt/PICTURE/", "NO_PICTURE_FILE.txt")
							ef = open(local_filename, "wb")	
							ef.write("file from " + PICTURE_DIRECTORY + file_name_from_ftp + " has not been downloaded to " + PATH_TO_PASTE_PICTURE_DIRECTORY, employee.image_file)
							ef.close()	

							local_filename = os.path.join(r"/opt/PICTURE/", "NO_PICTURE_FILE_DIR.txt")	
							ef = open(local_filename, "wb")	
							ef.write(employee.employee_number + ",")
							ef.close()										
						lf.close()							
			
				except ftplib.error_perm:
					#local_filename = os.path.join(r"/opt/DataFiles/", employee.image_file)
					lf = open(NO_PDF_FILE + file_name_from_ftp + '.txt', "wb")
					lf.close()
					continue
	
			ftp.quit()			


		else:
			raise Warning('No Employees Define.')


