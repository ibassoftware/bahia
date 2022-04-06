# -*- coding: utf-8 -*-
from openerp import models, fields,api
from openerp.exceptions import except_orm, Warning, RedirectWarning,ValidationError
import datetime

YEAR = 365
MONTH = 30
#ALT_255 = '            ' # ALR+255 is a Special Characters in ASCII
ALT_255 =''
DATE_NOW = datetime.datetime.now()
INT_ID_NOW = 0
class EmployeeChecklist(models.Model):
    _inherit = "hr.employee.checklist.documents"

    vessel_id = fields.Many2one('hr.vessel', string='Vessel')
    position_id = fields.Many2one('hr.rank', string='Position')
    department_id = fields.Many2one('hr.ship.department', string='Department')


    @api.model
    def createChecklistDocumentList(self, pObjRecord):
        checklistTemplates = self.env['hr.checklist_template'].search([('blank_row','=', False)])
        employeeChecklist = self.env['hr.employee.checklist.documents.list'].search([])
        for checklistTemplate in checklistTemplates:

            if len(checklistTemplate.checklist_temp_param_1) > 0:
                temp_1 = int(checklistTemplate.checklist_temp_param_1[0])
            else:
                temp_1 = None

            if len(checklistTemplate.checklist_temp_param_2) > 0:
                temp_2 = int(checklistTemplate.checklist_temp_param_2[0])
            else:
                temp_2 = None

            if len(checklistTemplate.checklist_temp_param_3) > 0:
                temp_3 = int(checklistTemplate.checklist_temp_param_3[0])
            else:
                temp_3 = None

            if len(checklistTemplate.checklist_temp_param_4) > 0:
                temp_4 = int(checklistTemplate.checklist_temp_param_4[0])
            else:
                temp_4 = None           

            if len(pObjRecord) == 0:
                record_id = self.id
                employee_id = self.employee_id.id
            else:
                record_id = pObjRecord.id
                employee_id = pObjRecord.employee_id.id



            count_Template = self.env['hr.employee.checklist.documents.list'].search_count([('checklist_template_id', '=', checklistTemplate.id),
                                                                             ('employee_checklist_document', '=', record_id)])

            if count_Template == 0:
                employee_checklist_id = employeeChecklist.create({
                    'employee_checklist_document': record_id,
                    'checklist_template_id': checklistTemplate.id,
                    'param_name_1': temp_1,
                    #'param_name_1_value': '',
                    #'param_name_1_check': False,
                    'param_name_2': temp_2,
                    #'param_name_2_value': ALT_255,
                    #'param_name_2_check': False,
                    'param_name_3': temp_3,
                    #'param_name_3_value': '',
                    #'param_name_3_check': False,
                    'param_name_4': temp_4,
                    #'param_name_4_value': '',
                    #'param_name_4_check': False,
                    'param_name_1_value_visible':  checklistTemplate.checklist_temp_param_1_with_value,
                    'param_name_2_value_visible':  checklistTemplate.checklist_temp_param_2_with_value,
                    'param_name_3_value_visible':  checklistTemplate.checklist_temp_param_3_with_value,
                    'param_name_4_value_visible':  checklistTemplate.checklist_temp_param_4_with_value,
                    'param_name_1_check_visible':  checklistTemplate.checklist_temp_param_1_check_value,
                    'param_name_2_check_visible':  checklistTemplate.checklist_temp_param_2_check_value,
                    'param_name_3_check_visible':  checklistTemplate.checklist_temp_param_3_check_value,
                    'param_name_4_check_visible':  checklistTemplate.checklist_temp_param_4_check_value,

                    'has_date_issued': checklistTemplate.checklist_temp_row_with_dateissued,
                    'has_issued_at': checklistTemplate.checklist_temp_row_with_dateissued,
                    'has_date_expiry': checklistTemplate.checklist_temp_param_1_with_dateexpired,
                    'has_changed_by':checklistTemplate.checklist_temp_param_1_with_changeby,
                    'has_change_date': checklistTemplate.checklist_temp_param_1_with_changedate, 
                    })

        employeeChecklist.getDataFromDocuments(record_id, employee_id)    	

    @api.model
    def createChecklistDocumentList_main(self, pObjRecord):
        checklistTemplates = self.env['hr.checklist_template'].search([])
        employeeChecklist = self.env['hr.employee.checklist.documents.list.main'].search([])
        #Write Now for the Sake of Demo 
        #This must be hardcoded
        
        #FOR US VISA
        if len(pObjRecord) == 0:
            record_id = self.id
            employee_id = self.employee_id.id
        else:
            record_id = pObjRecord.id
            employee_id = pObjRecord.employee_id.id

        vals = {'employee_checklist_document': record_id}

        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_US_VISA_MAIN_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_1': temp_1,
                    'param_name_1_value': '',
                    'param_name_1_check': False,
                    'param_name_1_value_visible':  True,
                    'param_name_1_check_visible':  True,
                    })

        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_CONTRACT_SIGNED_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_2': temp_1,
                    'param_name_2_value': '',
                    'param_name_2_check': False,
                    'param_name_2_value_visible':  True,
                    'param_name_2_check_visible':  False,
                    })


        #checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_US_VISA_ISSUED_AT_CONSTANT')])
        #temp_1 = checklistTemplates.id
        #vals.update({
        #            'param_name_3': temp_1,
        #            'param_name_3_value': '',
        #            'param_name_3_check': False,
        #            'param_name_3_value_visible':  True,
        #            'param_name_3_check_visible':  False,
        #            })
        #rec = employeeChecklist.create(vals)
        #rec.getEmployeeDocuments_Temporary(rec)

        #FOR US VISA EXPIRATION DATE
        #vals = {'employee_checklist_document': record_id}
        #checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_US_VISA_EXPIRY_DATE_CONSTANT')])
        #temp_1 = checklistTemplates.id
        #vals.update({
        #            'param_name_2': temp_1,
        #            'param_name_2_value': '',
        #            'param_name_2_check': False,
        #            'param_name_2_value_visible':  True,
        #            'param_name_2_check_visible':  False,
        #            })
        rec = employeeChecklist.create(vals)
        rec.getEmployeeDocuments_Temporary(rec)

        #FOR VISA 2
        vals = {'employee_checklist_document': record_id}
        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_VISA_II_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_1': temp_1,
                    'param_name_1_value': '',
                    'param_name_1_check': False,
                    'param_name_1_value_visible':  True,
                    'param_name_1_check_visible':  True,
                    })   


        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_APPRAISAL_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_2': temp_1,
                    'param_name_2_value': '',
                    'param_name_2_check': False,
                    'param_name_2_value_visible':  True,
                    'param_name_2_check_visible':  False,
                    })

        employeeChecklist.create(vals)     

        #FOR PEME
        vals = {'employee_checklist_document': record_id}

        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_PEME_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_1': temp_1,
                    'param_name_1_value': '',
                    'param_name_1_check': False,
                    'param_name_1_value_visible':  True,
                    'param_name_1_check_visible':  True,
                    })

        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_JOB_DESCRIPTION_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_2': temp_1,
                    'param_name_2_value': '',
                    'param_name_2_check': False,
                    'param_name_2_value_visible':  True,
                    'param_name_2_check_visible':  False,
                    })


        #checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_PEME_CLINIC_CONSTANT')])
        #temp_1 = checklistTemplates.id
        #vals.update({
        #            'param_name_3': temp_1,
        #            'param_name_3_value': '',
        #            'param_name_3_check': False,
        #            'param_name_3_value_visible':  True,
        #            'param_name_3_check_visible':  False,
        #            })
        employeeChecklist.create(vals)   
        # FOR OWWA
        vals = {'employee_checklist_document': record_id}

        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_OWWA_RECEIPT_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_1': temp_1,
                    'param_name_1_value': '',
                    'param_name_1_check': False,
                    'param_name_1_value_visible':  False,
                    'param_name_1_check_visible':  True,
                    })  

        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_COMPA_LEAVE_CONT_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_2': temp_1,
                    'param_name_2_value': '',
                    'param_name_2_check': False,
                    'param_name_2_value_visible':  True,
                    'param_name_2_check_visible':  False,
                    })
                            
        employeeChecklist.create(vals)   
        # FOR PAGIBIG
        vals = {'employee_checklist_document': record_id}

        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_PAGIBIG_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_1': temp_1,
                    'param_name_1_value': '',
                    'param_name_1_check': False,
                    'param_name_1_value_visible':  False,
                    'param_name_1_check_visible':  True,
                    })  
        employeeChecklist.create(vals)   
        # FOR PHILHEALTH
        vals = {'employee_checklist_document': record_id}

        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_PHILHEALTH_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_1': temp_1,
                    'param_name_1_value': '',
                    'param_name_1_check': False,
                    'param_name_1_value_visible':  False,
                    'param_name_1_check_visible':  True,
                    })  
        employeeChecklist.create(vals)   

        # FOR SSS
        vals = {'employee_checklist_document': record_id}

        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_SSS_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_1': temp_1,
                    'param_name_1_value': '',
                    'param_name_1_check': False,
                    'param_name_1_value_visible':  False,
                    'param_name_1_check_visible':  True,
                    })          
        employeeChecklist.create(vals)        

class EmployeeChecklistList(models.Model):
	_inherit = 'hr.employee.checklist.documents.list'

	param_name_1_related = fields.Many2one('hr.checklist', related='checklist_template_id.checklist_temp_param_1', string='Parameter 1')
	param_name_2_related = fields.Many2one('hr.checklist', related='checklist_template_id.checklist_temp_param_2', string='Parameter 2')
	param_name_3_related = fields.Many2one('hr.checklist', related='checklist_template_id.checklist_temp_param_3', string='Parameter 3')
	param_name_4_related = fields.Many2one('hr.checklist', related='checklist_template_id.checklist_temp_param_4', string='Parameter 4')