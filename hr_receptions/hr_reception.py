# -*- coding: utf-8 -*-
from openerp import models,fields,api, _
from openerp import tools
from openerp.report import report_sxw
import datetime
import base64
from openerp.exceptions import except_orm, Warning, RedirectWarning,ValidationError


#FOR EXCEL FILE
import xlwt
from cStringIO import StringIO

DATE_NOW = datetime.datetime.now()

class ReceprtionModel(models.Model):
	_name ='hr.reception'

	@api.model
	def _get_default_stage_id(self):

		model_reception_status  = self.env['hr.reception.status']
		return model_reception_status.get_stage_default()

	name = fields.Char('Name')
	status_id = fields.Many2one('hr.reception.status', 'Status', default = lambda self: self._get_default_stage_id())
	employee_id = fields.Many2one('hr.employee', 'Employee')
	user_io = fields.Many2one('res.users', 'Point Person', track_visibility='onchange')
	date= fields.Datetime('Date', required = True, default = DATE_NOW) 
	reception_detail_id = fields.One2many('hr.reception.detail','reception_ids', readonly=False,copy=False)
	description = fields.Text('Notes')

	last_status = fields.Many2one('hr.reception.status', 'Status')
	last_user_id = fields.Many2one('res.users', 'Last Point Person')
	last_date= fields.Datetime('Date Login')

	others = fields.Char('Others')

	@api.multi
	def print_checks(self):
		return {
		    'name': _('Print Reception Report'),
		    'type': 'ir.actions.act_window',
		    'res_model': 'print.reception.report',
		    'view_type': 'form',
		    'view_mode': 'form',
		    'target': 'new',
		    'context': {}
		    }		

	@api.multi
	def generateExcelReport(self, date_from, date_to):
		#Cell Properties Setup
		border = xlwt.Borders()
		border.bottom = xlwt.Borders.THIN
		border.top = xlwt.Borders.THIN
		border.left = xlwt.Borders.THIN
		border.right = xlwt.Borders.THIN 

		alignment = xlwt.Alignment()
		alignment.horz = xlwt.Alignment.HORZ_CENTER
		alignment.vert = xlwt.Alignment.VERT_CENTER

		styleTitleMain =xlwt.XFStyle()
		styleHeader = xlwt.XFStyle()
		styleColumns = xlwt.XFStyle()
		styleSpecificRow = xlwt.XFStyle()
		styleSpecificRow.num_format_str = "#,##0.00"
		#font
		font  = xlwt.Font()
		font.name = 'Arial'
		font.height =120
		styleTitleMain.font = font
		styleColumns.font = font
		styleColumns.borders = border
		#styleHeader.font = font
		styleHeader.alignment = alignment


		#Creation of Excel File
		workbook = xlwt.Workbook()
		sheet = workbook.add_sheet("Reception Report")
		intRow = 0
		#REPORT TITLE
		sheet.write_merge(intRow,intRow+1, 0,10, "Reception Report", styleHeader)  
		intRow +=2
		#HEADER
		sheet.write(intRow, 0, "Date:")
		sheet.write(intRow, 1, date_from)                         
		intRow +=2          

		#COLUMNS
		sheet.write(intRow, 0,"Employee Number",styleColumns)
		sheet.write(intRow, 1, "Employee Contract Number",styleColumns)
		sheet.write(intRow, 2, "Employee",styleColumns)
		sheet.write(intRow, 3, "Point Person",styleColumns)
		sheet.write(intRow, 4, "Login",styleColumns)
		sheet.write(intRow, 5, "Logout",styleColumns)
		intRow +=1


		#DETAILS
		#raise Warning(datetime.datetime.strptime(str(date_from) + ' 11:59:59', '%Y-%m-%d %H:%M:%S'))
		dateFrom = datetime.datetime.strptime(str(date_from) + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
		dateTo  = datetime.datetime.strptime(str(date_from) + ' 11:59:59', '%Y-%m-%d %H:%M:%S')


		
		tree_model = self.env['hr.reception'].search([('create_date','>=',str(dateFrom)), ('create_date','<=',str(dateTo))])
		for detail in tree_model:
		    sheet.write(intRow, 0, detail.employee_id.employee_number)
		    sheet.write(intRow, 1, detail.employee_id.employee_contract_number)
		    sheet.write(intRow, 2, detail.employee_id.name)
		    sheet.write(intRow, 3, detail.user_io.name)
		    sheet.write(intRow, 4, detail.last_date)
		    sheet.write(intRow, 5, detail.date)

		    intRow +=1

		fp = StringIO()
		workbook.save(fp)
		fp.seek(0)
		data_read = fp.read()
		fp.close()
		byte_arr = base64.b64encode(data_read)


		mode_ir_attachment = self.env['ir.attachment']
		count_if_exist = mode_ir_attachment.search_count([('name','=', str(self._uid) + '_Reception_report.xls')])
		if count_if_exist >0:
		    model_file_ir_attachment = mode_ir_attachment.search([('name','=', str(self._uid)  + '_Reception_report.xls')])
		    model_file_ir_attachment.write({'datas': byte_arr,
		                                    'datas_fname': str(self._uid)  + '_Reception_report.xls'
		        })
		else:
		   mode_ir_attachment.create({
		    'name': str(self._uid)  + '_Reception_report.xls',
		    'type': 'binary',
		    'datas': byte_arr,
		    'datas_fname': str(self._uid)  + '_Reception_report.xls',
		    'description': 'Generated Reception Report'
		    })

		model_file_ir_attachment = mode_ir_attachment.search([('name','=', str(self._uid)  +  '_Reception_report.xls')])
		return {
		    'type' : 'ir.actions.act_url',
		    #'url':   '/web/binary/saveas?model=ir.attachment&field=datas&filename_field=self.file_name&id=%s' % ( model_file_ir_attachment.id ),
		    'url':   '/web/binary/saveas?model=ir.attachment&field=datas&filename_field=%s&id=%s' % ( model_file_ir_attachment.datas_fname,model_file_ir_attachment.id ),
		    'target': 'self',
		}  


	@api.model
	def _read_group_sprint_id(self, present_ids, domain, **kwargs):

	    sprints = self.env['hr.reception.status'].search([]).name_get()
	    return sprints, None

	_group_by_full = {
	    'status_id': _read_group_sprint_id,
	    }	

	@api.model
	def create(self, vals):
		model_employee = self.env['hr.employee'].search([('id', '=', vals['employee_id'])])
		vals['name'] = model_employee.name
		newid = super(ReceprtionModel, self).create(vals)
		return newid


	@api.multi
	def write(self, vals):
		#After Updating Get the Last Value of the Record
		model_reception = self.env['hr.reception'].search([('id', '=', self.id)])

		if not vals.has_key('date'):
			vals['date'] = DATE_NOW
			vals['last_date'] = model_reception.date

		vals['last_date'] = model_reception.date
		if vals.has_key('user_io'):
			vals['last_user_id'] = model_reception.user_io.id

		#One Way to Capture the Saving thru Kanban View
		if vals.has_key('status_id'):
			vals['last_status'] = model_reception.status_id.id
			vals['last_user_id'] = model_reception.user_io.id
			vals['last_date'] = model_reception.date
			vals['date'] = DATE_NOW
		#Save Current State

		super(ReceprtionModel, self).write(vals)





class ReceprtionDetailModel(models.Model):
	_name ='hr.reception.detail'
	reception_ids = fields.Many2one('hr.reception', 'Reception ID')
	name = fields.Char('Name')
	status_id_from = fields.Many2one('hr.reception.status', 'Status')
	status_id_to = fields.Many2one('hr.reception.status', 'Status')
	datetime_change = fields.Datetime('Status Change Date')


class PersonnelVisitationStatus(models.Model):
	_name = 'hr.reception.status'
	name = fields.Char('Status')
	sequence = fields.Integer('Sequence', default = 1)
	is_default = fields.Boolean('Default?', default = False)

	@api.model
	def get_stage_default(self):
		model_reception_status  = self.env['hr.reception.status'].search([('is_default', '=', True)])
		return model_reception_status.id

