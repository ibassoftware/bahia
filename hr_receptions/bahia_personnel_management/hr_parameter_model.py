# -*- coding: utf-8 -*-
from openerp import models, fields,api
from openerp.exceptions import except_orm, Warning, RedirectWarning,ValidationError

DATA_TYPE = [
('text', 'Text'),
('date', 'Date'),
('Integer', 'Integer')

]



CHECKLIST_DOCUMENT_TYPE = [
('none', 'None'),
('document', 'Document'),
('license', 'License'),
('medical', 'Medical')

]


RETRIEVE_RECORD_IN_HISTORY = [
('none', 'None'),
('latest_doc', 'Latest Doc.'),
('oldest_doc', 'Old Doc.'),
]
#Abstract Implementation

class ParameterModel(models.AbstractModel):
    _name ='hr.abs.parameter'
    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')


#Models
class AddressType(models.Model):
    _name = 'hr.addresstype'
    name = fields.Char('Address Type', required = True)
    description = fields.Text('Description')

    _sql_constraints = [
        ('hr_addresstype_name',
        'UNIQUE (name)',
        'Address Type must be unique!')]



class EducationType(models.Model):
    _name = 'hr.educationtype'
    name = fields.Char('Education')
    description = fields.Text('Description')

class DocumentType(models.Model):
    _name = 'hr.documenttype'
    abbreviation = fields.Char('Code', required =True)
    name = fields.Char('Document name', required=True)
    check_for_expiration = fields.Boolean('Check Expiration', default= False)
    description = fields.Text('Full Description')

    _sql_constraints = [
        ('hr_documenttype_name',
        'UNIQUE (abbreviation)',
        'Code must be unique!')]

class FamilyRelations(models.Model):
    _name = 'hr.familyrelations'
    code = fields.Char('Code', required =True)
    name = fields.Char('Relationship', required=True)
    description = fields.Text('Description')

    _sql_constraints = [
        ('hr_familyrelations_name',
        'UNIQUE (code,name)',
        'Family relation must be unique!')]

class MedicalRecordType(models.Model):
    _name = 'hr.medicalrecord'
    code = fields.Char('Code', required =True)
    name = fields.Char('Medical', required =True)
    description = fields.Text('Description')

    _sql_constraints = [
        ('hr_medicalrecord_name',
        'UNIQUE (code,name)',
        'Medical record type must be unique!')]

class LicenseType(models.Model):
    _name ='hr.licensetype'

    @api.model
    def _getClassID(self):

        cr = self._cr
        uid = self._uid
        context =self._context
        obj_sequence = self.pool.get('ir.sequence')
        return obj_sequence.next_by_code(cr, uid, 'hr.licensetype.sequence', context=context)

    #id_name = fields.Integer('Class ID', default=_getClassID)
    id_name = fields.Char('Class ID', default=_getClassID)
    name = fields.Char('Class Name', required =True)


    _sql_constraints = [
        ('hr_medicalrecord_name_uniq',
        'UNIQUE (id_name)',
        'License type must be unique')]

class License(models.Model):
    _name = 'hr.license'
    id_class_name = fields.Integer('Class ID')
    license_name = fields.Many2one('hr.licensetype','Class Name', required=True)
    name = fields.Char('Doc Abbreviation', required=True)
    doc_description = fields.Text('Doc Full Description')

    _sql_constraints = [
        ('hr_license_name_uniq',
        'UNIQUE (id_class_name,name)',
        'License must be unique')]

class MedicalClinic(models.Model):
    _name = 'hr.clinic'
    _inherit = 'hr.documenttype'
    _sql_constraints = [
        ('hr_clinic_name_uniq',
        'UNIQUE (abbreviation,name)',
        'Clinic name must be unique!')]

class LengthOfExpiration(models.Model):
    _name = 'hr.lengthofexpiration'
    _inherit = 'hr.familyrelations'
    days = fields.Integer('Days before Expiration')

    _sql_constraints = [
        ('hr_lengthofexp_name_uniq',
        'UNIQUE (abbreviation,name)',
        'Length of expiration must be unique!')]

class PortInformation(models.Model):
    _name = 'hr.port'
    _inherit = 'hr.abs.parameter'

    _sql_constraints = [
        ('hr_port_name_uniq',
        'UNIQUE (code, name)',
        'Port must be unique!')]

class Companies(models.Model):
    _name = 'hr.companies'
    _inherit = 'hr.abs.parameter'

    _sql_constraints = [
        ('hr_company_name_uniq',
        'UNIQUE (code, name)',
        'Port must be unique!')]

class VesselCategory(models.Model):
    _name = 'hr.vesselcategory'
    category = fields.Char('Category', required=True)
    name = fields.Char('Name', required=True)
    vessel_cat_ids = fields.Many2many('hr.ship.department','department_vessel_rel', 'vessel_cat_id','department_id', 'Vessel Category')

    _sql_constraints = [
        ('hr_vesselcat_name_uniq',
        'UNIQUE (category,name)',
        'Vessel category must be unique!')]

class Vessel(models.Model):
    _name = 'hr.vessel'
    _inherit ='hr.abs.parameter'
    company_code = fields.Many2one('hr.companies', 'Company', required =True)
    vessel_category = fields.Many2one('hr.vesselcategory','Category', required =True)

    _sql_constraints = [
        ('hr_vessel_name_uniq',
        'UNIQUE (code,name,vessel_category,company_code)',
        'Vessel must be unique!')]

class RankType(models.Model):
    _name = 'hr.ranktype'
    _inherit = 'hr.abs.parameter'
    rate = fields.Float('Incentive Rate',digits=(18,2))

    _sql_constraints = [
        ('hr_ranktype_name_uniq',
        'UNIQUE (code,name)',
        'Rank type must be unique!')]

class Rank(models.Model):
    _name = 'hr.rank'
    rank_identification = fields.Char('Rank ID')
    rank = fields.Char('Rank')
    name= fields.Char('Name')
    rank_type = fields.Many2one('hr.ranktype', 'Rank Type')
    rank_department_ids = fields.Many2many('hr.ship.department', 'rank_department_table','rank_department_id','department_id','Departments')


    _sql_constraints = [
        ('hr_rank_name_uniq',
        'UNIQUE (rank_identification,name,rank_type)',
        'Rank must be unique!')]

    
    #rank_ids = fields.Many2many('hr.ranktype','rank_type_rel', 'rank_id','ship_code_id')

class ShipDepartment(models.Model):
    _name = 'hr.ship.department'
    ship_dept_code = fields.Char('Code', required=True)
    name = fields.Char('Name')
    department = fields.Char('Department', required=True)

    #department_rank_ids = fields.Many2many('ranktype','dep_rank_rel','department_rank_id','rank_department_id')
    department_ids = fields.Many2many('hr.vesselcategory','department_vessel_rel', 'department_id','vessel_cat_id', 'Vessel Category')

    _sql_constraints = [
        ('hr_shipdep_name_uniq',
        'UNIQUE (ship_dept_code,name,department_ids)',
        'Ship Department must be unique!')]

    @api.onchange('department', 'ship_dept_code')
    def onchangeName(self):
        if not isinstance( self.ship_dept_code, bool) and not isinstance( self.department, bool):
            #raise Warning("[" + self.ship_dept_code + "]" + " " + self.department)
            self.name = "[" + self.ship_dept_code + "]" + " " + self.department

    # Overrides
    @api.model
    def create(self, vals):

        if vals.has_key('name'):
                vals['name'] =  "[" + vals['ship_dept_code'] + "]" + " " + vals['department']
        else: 
            vals.update({'name': "[" + vals['ship_dept_code'] + "]" + " " + vals['department']})                   
        new_record = super(ShipDepartment, self).create(vals)
        return new_record  

    @api.multi
    def write(self, vals):
        #if vals.has_key('name'):
        #        vals['name'] =  "[" + vals['ship_dept_code'] + "]" + " " + vals['department']
        #else:
        #         vals['name'] =  "[" + vals['ship_dept_code'] + "]" + " " + vals['department']
        name_value = ''
        if not vals.has_key('name'):

                if vals.has_key('ship_dept_code'):
                    name_value = "[" + vals['ship_dept_code']  + "]" + " "
                else:
                    name_value = "[" + self.ship_dept_code  + "]" + " "

                if vals.has_key('department'):
                    name_value += vals['department']
                else:
                    name_value += self.department
                vals.update({'name': name_value})   
                #raise Warning(self.ship_dept_code)

        super(ShipDepartment, self).write(vals)        
        return True        

class Status(models.Model):
    _name = 'hr.employment.status'
    status_id = fields.Char('Status ID')
    name = fields.Text('Description', required=True)

    _sql_constraints = [
        ('hr_empstat_name_uniq',
        'UNIQUE (status_id,name)',
        'Rank must be unique!')]

class CheckList(models.Model):
    _name= 'hr.checklist'
    checklist_code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    link_selection = fields.Selection(CHECKLIST_DOCUMENT_TYPE, 'Document Link', default ='none')
    link_document_type = fields.Many2one('hr.documenttype', 'Document Type')
    link_license_type = fields.Many2one('hr.license', 'License Type')
    link_medical_type = fields.Many2one('hr.medicalrecord', 'Medical Type')
    retrieve_history_records = fields.Selection(RETRIEVE_RECORD_IN_HISTORY, 'Retrieving of Records', default ='latest_doc')

    _sql_constraints = [
        ('hr_chekclist_name_uniq',
        'UNIQUE (checklist_code,name)',
        'Checklist must be unique!')]


    @api.onchange('link_selection')
    def onchange_selection(self):
        self.link_document_type = None
        self.link_license_type = None    
        self.link_medical_type = None  
        self.retrieve_history_records  = 'latest_doc'
        #if self.link_selection  == 'none':
        #    self.link_document_type = None
        #    self.link_license_type = None
        #elif self.link_selection  == 'license':
        #    self.link_document_type = None
        #    self.link_license_type = None


class religion(models.Model):
    _name= 'hr.religion'
    religion_code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('hr_religion_code_uniq',
        'UNIQUE (religion_code)',
        'Checklist must be unique!')]


class ChecklistTemplate(models.Model):
    _name = 'hr.checklist_template'
    _order =  'csequence'
    checklist_temp_code = fields.Char('Code')
    name = fields.Char('Name')
    checklist_temp_param_1 = fields.Many2one('hr.checklist', 'Parameter 1')
    checklist_temp_param_1_with_value = fields.Boolean('With Value')
    checklist_temp_param_1_data_type = fields.Selection(DATA_TYPE, 'Data Type')
    checklist_temp_param_1_colspan = fields.Integer('Column Span')
    checklist_temp_param_1_check_value = fields.Boolean('Allow Check', default = True)



    checklist_temp_param_2 = fields.Many2one('hr.checklist', 'Parameter 2')
    checklist_temp_param_2_with_value = fields.Boolean('With Value')
    checklist_temp_param_2_data_type = fields.Selection(DATA_TYPE, 'Data Type')
    checklist_temp_param_2_colspan = fields.Integer('Column Span')
    checklist_temp_param_2_check_value = fields.Boolean('Allow Check', default = True)


    checklist_temp_param_3 = fields.Many2one('hr.checklist', 'Parameter 3')
    checklist_temp_param_3_with_value = fields.Boolean('With Value')
    checklist_temp_param_3_data_type = fields.Selection(DATA_TYPE, 'Data Type')
    checklist_temp_param_3_colspan = fields.Integer('Column Span')
    checklist_temp_param_3_check_value = fields.Boolean('Allow Check', default = True)

    checklist_temp_param_4 = fields.Many2one('hr.checklist', 'Parameter 4')
    checklist_temp_param_4_with_value = fields.Boolean('With Value')
    checklist_temp_param_4_data_type = fields.Selection(DATA_TYPE, 'Data Type')
    checklist_temp_param_4_colspan = fields.Integer('Column Span')
    checklist_temp_param_4_check_value = fields.Boolean('Allow Check', default = True)

    checklist_temp_row_with_dateissued = fields.Boolean('With Value', default = True)
    checklist_temp_param_1_with_dateexpired = fields.Boolean('With Value', default = True)
    checklist_temp_param_1_with_changeby = fields.Boolean('With Value', default = True)
    checklist_temp_param_1_with_changedate = fields.Boolean('With Value', default = True)
    csequence = fields.Integer("Sequence", default = 0)


    @api.model
    def create(self, vals):
        if vals['csequence'] == False:
            raise Warning('No Checklist template sequence define.')

        if vals['name'] == False:
            raise Warning('No Checklist template name define.')
        #raise Warning(vals)
        new_record = super(ChecklistTemplate, self).create(vals)

        return new_record

    _sql_constraints = [
        ('hr_chekclist_name_uniq',
        'UNIQUE (name,name)',
        'Template name must be unique!')]

