from openerp import models, fields,api
from openerp.exceptions import except_orm, Warning, RedirectWarning,ValidationError
import base64
import datetime

FIRST_NAMES = ['CYNTHIA', 'MANNY', '2019']
LAST_NAMES = ['MENDOZA', 'ESPINOSA']

class SystemAuditDeleteLog(models.Model):
    _name = 'sys.audit.delete.log'
    _order ='create_date, create_uid desc'    

    name = fields.Char(string='Field Name')
    model_id = fields.Many2one('ir.model','Model')
    record_id = fields.Char('Record Reference ID')
    record_name = fields.Char('Record Reference Name')
    value_from = fields.Char('Value/s Before Deletion')

    @api.model
    def create_audit(self,model_name='' ,id=0, record_name=''):        
        model_sys_audit_config = self.env['sys.model.audit.config'].search([('model_id.model','=', model_name)])
        obj_get = self.env[model_name].search([('id','=', id)])
        vals={}
        vals_create = {
                    'model_id' : False,
                    'value_from': False,
                    'record_name': record_name,    
                    'record_id': id,}

        if model_sys_audit_config:
            if obj_get:
                for config in model_sys_audit_config:
                    vals_create['model_id'] = config.model_id.id
                    vals[config.model_fields.name] = obj_get and obj_get[config.model_fields.name] or False
                vals_create['value_from'] = str(vals or '')

                res = self.create(vals_create)
                return res
        return False

class SystemAuditLog(models.Model):
    _name = 'sys.audit.log'
    _order ='create_date, create_uid desc'
    name = fields.Char(related='model_fields.field_description', string='Field Name', store=True)
    model_id = fields.Many2one('ir.model','Model')
    model_fields = fields.Many2one('ir.model.fields','Field Name')
    record_id = fields.Char('Record Reference ID')
    record_name = fields.Char('Record Reference Name')
    value_from = fields.Char('Old Value')
    new_value = fields.Char('Updated Value')

    @api.model
    def update_audit_legacy_doc(self,legacy_doc_ids=0):        

        for legacy_doc_id in legacy_doc_ids:
            obj_get = self.env['hr.employee'].search([('id','=', legacy_doc_id.record_id or False)])
            if obj_get:
                val_new = False
                if obj_get[legacy_doc_id.model_fields.name]:
                    val_new = base64.b64decode(obj_get[legacy_doc_id.model_fields.name])
                legacy_doc_id.write({'new_value': val_new})

    @api.model
    def create_audit(self,model_name='' ,field_name='', old_value='', new_value='', id=0, record_name=''):        
        model_sys_audit_config = self.env['sys.model.audit.config'].search([('model_fields.name','=', field_name),('model_id.model','=', model_name)])

        if model_sys_audit_config:
            obj_get = self.env[model_name].search([('id','=', id)])
            if model_sys_audit_config.model_fields.ttype != 'one2many':   
                vals_create = {
                            'model_id' : model_sys_audit_config.model_id.id,
                            'model_fields' : model_sys_audit_config.model_fields.id,
                            'value_from': obj_get and obj_get[field_name] or False,
                            'new_value': new_value,
                            'record_name': record_name,    
                            'record_id': id,
                    }

                if model_sys_audit_config.model_fields.ttype == 'many2one':
                    #Old Value
                    obj_get_relation = self.env[model_sys_audit_config.model_fields.relation].search([('id','=', obj_get and obj_get[field_name].id or False)])
                    vals_create['value_from'] = obj_get_relation and obj_get_relation.name or False

                    #New Value
                    obj_get_relation = self.env[model_sys_audit_config.model_fields.relation].search([('id','=', new_value)])
                    vals_create['new_value'] = obj_get_relation and obj_get_relation.name or False
                elif model_sys_audit_config.model_fields.ttype == 'binary' and (field_name in ['legacy_doc_1', 'legacy_doc_2', 'legacy_doc_3']):
                    val_from = False
                    val_new = False
                    if obj_get and obj_get[field_name]:
                        val_from = base64.b64decode(obj_get[field_name])
                    if new_value:
                        val_new = base64.b64decode(new_value)

                    vals_create['value_from'] =   val_from
                    vals_create['new_value'] = val_new

                res = self.create(vals_create)
                return res
        return False

class SystemModelForAudit(models.Model):
    _name = 'sys.model.audit.config'
    _description = 'Pre Defined Model Field Name Audit'


    name = fields.Char('Name', default='Audit Configuration')
    model_id = fields.Many2one('ir.model','Model', required=True)
    model_fields = fields.Many2one('ir.model.fields','Field Name', required=True)
    #model_fields_name = fields.Char(related='model_fields.name', string='Field Name')    
    #model_fields_label = fields.Char(related='model_fields.field_description', string='Field Label')
    #model_fields_type = fields.Selection(related='model_fields.ttype', string='Field Type')
    #model_fields_db_name = fields.Char(related='model_id.model', string='Model DB Name')


#Models to be Audited
class HrEmployee(models.Model):

    _inherit = 'hr.employee'


    @api.multi
    def unlink(self):
        obj_audit_log = self.env['sys.audit.delete.log']
        res_id = obj_audit_log.create_audit(model_name='hr.employee', id=self.id , record_name = self.name)
        return super(HrEmployee, self).unlink()

    @api.multi
    def write(self, vals):

        #check First Name:
        if 'first_name' in vals:
            if vals['first_name'].upper() in FIRST_NAMES:
                raise Warning('VALUE WILL BE SAVED IN DB '  + vals['first_name'] + '  VALUE IN TEXT FIELD ' + self.first_name)

        #Check Last Name
        if 'last_name' in vals:
            if vals['last_name'].upper() in LAST_NAMES:
                raise Warning('VALUE WILL BE SAVED IN DB '  + vals['last_name'] + '  VALUE IN TEXT FIELD ' + self.last_name)


        #Start Check Audit
        obj_audit_log = self.env['sys.audit.log']
        legacy_doc_ids = []
        for field in vals:
            res_id = obj_audit_log.create_audit(model_name='hr.employee', field_name=field,new_value=vals[field], id=self.id , record_name = self.name)
            if field in ['legacy_doc_1', 'legacy_doc_2', 'legacy_doc_3']:
                if res_id:
                    legacy_doc_ids.append(res_id)
        res = super(HrEmployee, self).write(vals)
        if len(legacy_doc_ids) > 0:
            obj_audit_log.update_audit_legacy_doc(legacy_doc_ids)
        return res

class HrEmployeeAddress(models.Model):

    _inherit = 'hr.employeeaddress'

    _description='Employee Address List'

    @api.multi
    def unlink(self):
        obj_audit_log = self.env['sys.audit.delete.log']
        res_id = obj_audit_log.create_audit(model_name='hr.employeeaddress', id=self.id , record_name = self.employee_address_id.name)
        return super(HrEmployeeAddress, self).unlink()


    @api.multi
    def write(self, vals):
        #Start Check Audit
        obj_audit_log = self.env['sys.audit.log']
        for field in vals:
            res_id = obj_audit_log.create_audit(model_name='hr.employeeaddress', field_name=field,new_value=vals[field], id=self.id , record_name = self.employee_address_id.name)
        res = super(HrEmployeeAddress, self).write(vals)
        return res

class HrEmployeeEducation(models.Model):

    _inherit = 'hr.employeducation'
    @api.multi
    def write(self, vals):
        #Start Check Audit
        obj_audit_log = self.env['sys.audit.log']
        for field in vals:
            res_id = obj_audit_log.create_audit(model_name='hr.employeducation', field_name=field,new_value=vals[field], id=self.id , record_name = self.employee_education_id.name)
        res = super(HrEmployeeEducation, self).write(vals)
        return res

class HrEmployeeFamilies(models.Model):
    _inherit = 'hr.employee_families'

    @api.multi
    def write(self, vals):
        #Start Check Audit
        obj_audit_log = self.env['sys.audit.log']
        for field in vals:
            res_id = obj_audit_log.create_audit(model_name='hr.employee_families', field_name=field,new_value=vals[field], id=self.id , record_name = self.employee_family_relationship_id.name)
        res = super(HrEmployeeFamilies, self).write(vals)
        return res

class HrEmployeeDocuments(models.Model):
    _inherit = 'hr.employee_documents'

    @api.multi
    def write(self, vals):
        #Start Check Audit
        obj_audit_log = self.env['sys.audit.log']
        for field in vals:
            res_id = obj_audit_log.create_audit(model_name='hr.employee_documents', field_name=field,new_value=vals[field], id=self.id , record_name = self.employee_doc_id.name)
        res = super(HrEmployeeDocuments, self).write(vals)
        return res

class HrEmployeeMedicalRecords(models.Model):
    _inherit = 'hr.employee_medical_records'

    @api.multi
    def write(self, vals):
        #Start Check Audit
        obj_audit_log = self.env['sys.audit.log']
        for field in vals:
            res_id = obj_audit_log.create_audit(model_name='hr.employee_medical_records', field_name=field,new_value=vals[field], id=self.id , record_name = self.employee_med_rec_id.name)
        res = super(HrEmployeeMedicalRecords, self).write(vals)
        return res

class HrEmployeeLicenses(models.Model):
    _inherit = 'hr.employeelicenses'

    @api.multi
    def write(self, vals):
        #Start Check Audit
        obj_audit_log = self.env['sys.audit.log']
        for field in vals:
            res_id = obj_audit_log.create_audit(model_name='hr.employeelicenses', field_name=field,new_value=vals[field], id=self.id , record_name = self.employee_licenses_id.name)
        res = super(HrEmployeeLicenses, self).write(vals)
        return res

class HrEmployeeEmployment(models.Model):

    _inherit = 'hr.employmenthistory'

    @api.multi
    def write(self, vals):
        #Start Check Audit
        obj_audit_log = self.env['sys.audit.log']
        for field in vals:
            res_id = obj_audit_log.create_audit(model_name='hr.employmenthistory', field_name=field,new_value=vals[field], id=self.id , record_name = self.employee_employment_id.name)
        res = super(HrEmployeeEmployment, self).write(vals)
        return res