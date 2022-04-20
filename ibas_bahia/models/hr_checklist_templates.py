from openerp import models, fields,api
from openerp.exceptions import except_orm, Warning, RedirectWarning,ValidationError

class CheckListTemplate(models.Model):
	_name='hr.checklist_template.main'
	name = fields.Char('Checklist Name')
	#department_id = fields.Many2one('hr.ship.department', 'Ship Department')
	department_ids = fields.Many2many('hr.ship.department','checklist_department_rel','checklist_main_id','department_id', 'Ship Department')
	allow_to_fill_by_dep = fields.Boolean('Auto Fill Employee Checklist by Department?')
	checklist_template_ids = fields.One2many('hr.checklist_template','checklist_template_main_id', string='Checklist Template Details')

# class CheckListTemplateList(models.Model):
# 	_inherit = 'hr.checklist_template'
