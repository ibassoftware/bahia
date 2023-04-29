# -*- coding: utf-8 -*-
import importlib
from openerp import models, fields,api
from openerp.exceptions import except_orm, Warning, RedirectWarning,ValidationError

import logging
_logger = logging.getLogger(__name__)

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
    _name = 'hr.employee'
    _inherit = ['hr.employee']
    _description = 'Extension of Employee Information in Recruitment Process'

    @api.multi 
    def get_file_personal_data(self):
        _logger.info("TESST")
        path = os.path.dirname(os.path.realpath(__file__)) 
        filecontent = base64.b64decode(self.legacy_doc_2 or '')
        return {
            'type' : 'ir.actions.act_url',
            'url': '/opt/DataFiles/%s' % (filecontent),
            'target': 'self',
        }
        # return {
        #     'type' : 'ir.actions.act_url',
        #     'url': '/web/binary/download_document?model=hr.employee&field=legacy_doc_2&id=%s&filename=%s' % (self.id, self.filename2),
        #     'target': 'self',
        # }

    #---------------- Functions/Methods
    def getCheckListId(self):

        #checklistTemplates = self.env['hr.checklist_template'].search([])
        #employeeChecklist = self.env['hr.employee_checklist']
        SQL_QUERY ="SELECT id,1 employee_id ,id checklist_template_id"\
                   " FROM hr_checklist_template;"

        self.env.cr.execute(SQL_QUERY)
        checklistTemplates = self.env.cr.fetchall()

        return checklistTemplates

    def generateFile(self,vals):

        dt_tm_filename = DATE_NOW.strftime("%m%d%Y%H%M%S")
        byte_arr = base64.b64encode('Dummy File')
        document_binary = ""
        bln_must_save = False
        if vals.has_key('legacy_doc_1'):
            str_filename = self.filename.rstrip('.pdf') + '_' + dt_tm_filename + '.pdf'
            FILENAME_DIR = "/opt/DataFiles/" + str_filename
            if not isinstance(vals['legacy_doc_1'], bool):
                document_binary = vals['legacy_doc_1']
                byte_arr = base64.b64encode(str_filename)

                vals['legacy_doc_1'] = byte_arr
                #raise Warning(len(vals['legacy_doc_1']))
                with open(FILENAME_DIR, "wb") as f:
                    f.write(base64.b64decode(document_binary))
            else:
                is_exists = os.path.isfile(FILENAME_DIR)
                if is_exists:
                    os.remove(FILENAME_DIR)       

        if vals.has_key('legacy_doc_2'):
            str_filename = self.filename2.rstrip('.pdf') + '_' + dt_tm_filename + '.pdf'
            FILENAME_DIR = "/opt/DataFiles/" + str_filename
            if not isinstance(vals['legacy_doc_2'], bool):
                document_binary = vals['legacy_doc_2']   
                byte_arr = base64.b64encode(str_filename)
                vals['legacy_doc_2'] = byte_arr 
                with open(FILENAME_DIR, "wb") as f:
                    f.write(base64.b64decode(document_binary))    
            else:
                os.remove(FILENAME_DIR)                                              

        if vals.has_key('legacy_doc_3'):
            str_filename = self.filename3.rstrip('.pdf') + '_' + dt_tm_filename + '.pdf'
            FILENAME_DIR = "/opt/DataFiles/" + str_filename
            if not isinstance(vals['legacy_doc_3'], bool):
                document_binary = vals['legacy_doc_3']              
                byte_arr = base64.b64encode(str_filename)
                vals['legacy_doc_3'] = byte_arr
                with open(FILENAME_DIR, "wb") as f:
                    f.write(base64.b64decode(document_binary))        
            else:
                os.remove(FILENAME_DIR)                    
    
    # Overrides

    @api.model
    def create(self, vals):

        #To Check if Contract Nunber Already Exists
        if vals.has_key('employee_contract_number'):
            str_employee_with_contract_number = ""
            employee_model = self.env['hr.employee'].search([('employee_contract_number', '=',vals['employee_contract_number'])])
            if employee_model:
                for employee in employee_model:
                    str_employee_with_contract_number += employee.name + '\n'

                raise Warning("Contract number already exists. \n Employee/s: \n" + str_employee_with_contract_number)

        new_id = super(HrEmployeeExtend, self).create(vals)
        #After Creation of Personnel create a User
        lst_groups = []
        if new_id.employee_contract_number != 'N/A':
            new_loggin_name = new_id.last_name + '_' + str(new_id.employee_contract_number)
        else:
            new_loggin_name = new_id.last_name + '_' + str(new_id.employee_number)
        if isinstance(new_id.middle_name, bool):
            new_user_fullname = new_id.first_name + ' ' + new_id.last_name
        else:
            new_user_fullname = new_id.first_name + ' '+ new_id.middle_name + ' ' + new_id.last_name
        
        model_userinfo = self.env['res.users']
        lst_groups.append(1)
        id_user = model_userinfo.create({
            'name': new_user_fullname,
            'login': new_loggin_name,
            'password':new_loggin_name,
            'groups_id':   [(6,0,[1])],
            })        
        new_id.user_id = id_user.id
        return new_id


    @api.multi
    def write(self, vals):
        #To Check if Contract Nunber Already Exists
        if vals.has_key('employee_contract_number'):

            str_employee_with_contract_number = ""
            employee_model = self.env['hr.employee'].search([('employee_contract_number', '=',vals['employee_contract_number'])])
            if employee_model:
                for employee in employee_model:
                    str_employee_with_contract_number += employee.name + '\n'

                raise Warning("Contract number already exists. \n Employee/s: \n" + str_employee_with_contract_number)
                        
        self.generateFile(vals)
        super(HrEmployeeExtend, self).write(vals)
        checklistTemplates = self.env['hr.checklist_template'].search([])
        employeeChecklist = self.env['hr.employee_checklist'].search([])

        #Check the Value if Contract Number has been updated then Update the UserName and Password
        if vals.has_key('employee_contract_number'):
            model_userinfo = self.env['res.users'].search([('id','=', self.user_id.id)])
            #To Check if Contract Number has a PH
            if self.employee_contract_number.find('PH', 0, len(self.employee_contract_number)) > 0:
                new_loggin_name = self.last_name + '_' + str(self.employee_contract_number[self.employee_contract_number.find('PH', 0, len(self.employee_contract_number)): len(self.employee_contract_number)])
            else:
                if len(self.employee_contract_number) < 4:
                    new_loggin_name = self.last_name + '_' + self.employee_contract_number.zfill(4) 
                else:
                    new_loggin_name = self.last_name + '_' + str(self.employee_contract_number)
            model_userinfo.write({
                'login': new_loggin_name,
                'password':new_loggin_name,                
                })   

        for checklistTemplate in checklistTemplates:
            # CHARACTER IS ALT+255 and Special Character in ASCII
            #ALT_255 = '            '
            ALT_255 = ''
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

            count_Template = self.env['hr.employee_checklist'].search_count([('checklist_template_id', '=', checklistTemplate.id),
                                                                             ('employee_id', '=', self.id)])
            if count_Template == 0:
                employeeChecklist.create({
                    'employee_id': self.id,
                    'checklist_template_id': checklistTemplate.id,
                    'param_name_1': temp_1,
                    'param_name_1_value': '',
                    'param_name_1_check': False,
                    'param_name_2': temp_2,
                    'param_name_2_value': ALT_255,
                    'param_name_2_check': False,
                    'param_name_3': temp_3,
                    'param_name_3_value': '',
                    'param_name_3_check': False,
                    'param_name_1_value_visible':  checklistTemplate.checklist_temp_param_1_with_value,
                    'param_name_2_value_visible':  checklistTemplate.checklist_temp_param_2_with_value,
                    'param_name_3_value_visible':  checklistTemplate.checklist_temp_param_3_with_value})

        #Check first if Employment has been updated for the convinience of optimization
        if vals.has_key('employee_employment'):
            server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
            model_employment_history = self.env['hr.employmenthistory'].search([('employee_employment_id','=',self.id)])
            #raise Warning(self.id)
            #model_employment_history.sorted(key=lambda r: r.date_servicefrom, reverse = True)
            for x in model_employment_history:
                #raise Warning(vals['employee_employment'])
                #raise Warning(x.employee_employment_id)
                for emp_history in vals['employee_employment']:
                    if x.id == emp_history[1]:
                        if emp_history[2] != False:
                            if emp_history[2].has_key('date_serviceto'):
                                if len(emp_history[2]['date_serviceto']) > 0:
                                    if datetime.datetime.strptime(emp_history[2]['date_serviceto'], '%Y-%m-%d')  <= server_date:
                                        model_employment_history.create({
                                            'employee_employment_id' : self.id,
                                            'date_servicefrom' : x.date_serviceto,
                                            'employment_status': 23, # AVAILABLE
                                            'object_code' : 174,
                                            'employment_dept_code': x.employment_dept_code and x.employment_dept_code.id or False,
                                            'employment_rank': x.employment_rank and x.employment_rank.id or False,
                                            } # AVAILABLE
                                            )
                                        break
                    else:
                        pass
                break
#            pass                 
        return True

    # End Override Functions

    @api.model
    def _getEmpId(self):

        cr = self._cr
        uid = self._uid
        context =self._context
        obj_sequence = self.pool.get('ir.sequence')
        return obj_sequence.next_by_code(cr, uid, 'hr.employee.sequence', context=context)

    @api.onchange('first_name','middle_name','last_name')
    def getFullname(self):
        if self.first_name == False:
            self.first_name=''
        if self.middle_name == False:
            self.middle_name=''
        if self.last_name == False:
            self.last_name=''
        #self.name_related = self.first_name + " " + self.middle_name + " " + self.last_name
        #self.name = self.first_name + " " + self.middle_name + " " + self.last_name
        self.name_related = self.last_name + ", " +  self.first_name + " " + self.middle_name
        self.name =  self.last_name + ", " +  self.first_name + " " + self.middle_name   

    @api.onchange('employee_employment')
    def computeServiceLenght(self):
        totalyears = 0
        getEmployments = self.employee_employment
        for getEmployment in getEmployments:
            #employmenthistory = self.env['hr.employmenthistory'].search([('id', '=', getEmployments.id)])
            if isinstance(getEmployment.id, models.NewId):
                if getEmployment.date_servicefrom != False and getEmployment.date_serviceto != False:
                    date_from = datetime.datetime.strptime(getEmployment.date_servicefrom ,"%Y-%m-%d")
                    date_to = datetime.datetime.strptime(getEmployment.date_serviceto ,"%Y-%m-%d")
                    no_of_days =(((abs((date_to - date_from).days) * 24) * 60) * 60)
                    self.service_length = self.service_length + no_of_days

    def getEmployeeID(self):
        prim_key = None
        empids = self.env['hr.employee'].search([('employee_number', '=', self.employee_number)])
        if len(empids) >0:
            prim_key = int(empids[0])
        else:
            prim_key = 0
        self.employee_id = prim_key
        return prim_key

    @api.one
    def getdocumentStatus(self):
        server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
        #totaldoc = self.env['hr.employee_documents'].search_count([('date_expiry', '<', server_date),('employee_doc_id','=', self.id)])
        doc_record = self.env['hr.employee_documents'].search([('date_expiry', '<', server_date),('employee_doc_id','=', self.id)])

        for doc in doc_record:
            if not isinstance(doc.document, bool):
                if doc.document.check_for_expiration == True:
                    self.documents_status = True
                    break
                else:
                    self.documents_status = False
            else:
                self.documents_status = False

    @api.one
    def getMedicalStatus(self):
        server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
        totaldoc = self.env['hr.employee_medical_records'].search_count([('date_to', '<', server_date),('employee_med_rec_id','=', self.id)])

        if totaldoc > 0:
            self.medical_status = True
        else:
            self.medical_status = False

    @api.one
    def legacy_doc1_getFilename(self):

        if len(self.employee_number) > 0:
            self.filename = self.employee_number + '_ConfidentialReports.pdf'
        else:
            self.filename = 'filename_ConfidentialReports.pdf'

    @api.one
    def legacy_doc2_getFilename(self):

        if len(self.employee_number) > 0:
            self.filename2 = self.employee_number + '_PersonalData.pdf'
        else:
            self.filename2 = 'filename_PersonalData.pdf'

    @api.one
    def legacy_doc3_getFilename(self):

        if len(self.employee_number) > 0:
            self.filename3 = self.employee_number + '_PersonalSummary.pdf'
        else:
            self.filename3 = 'filename_PersonalSummary.pdf'


    @api.one
    def _checklist_count(self):
        checklist_document_model = self.env['hr.employee.checklist.documents']
        self.checklist_count =  checklist_document_model.search_count([('employee_id', '=', self.id)])


    @api.one
    def _checkLatestEmployment(self):
        server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
        model_hr_employmenthistory = self.env['hr.employmenthistory'].search([('employee_employment_id', '=', self.id),
                                                                              ('date_servicefrom', '<=', server_date),
                                                                              ('date_serviceto', '>=', server_date)])
        if len(model_hr_employmenthistory) > 0:
            model_hr_employmenthistorty_2 = model_hr_employmenthistory.sorted(key=lambda r: r.date_serviceto, reverse = True)
            for employee in model_hr_employmenthistorty_2:
                self.employee_rank = employee.employment_rank.name
                break
            model_hr_employmenthistory = self.env['hr.employmenthistory'].search([('employee_employment_id', '=', self.id)])
            if len(model_hr_employmenthistory) > 0:
                if isinstance(self.employee_rank, bool):
                    for employee in model_hr_employmenthistorty_2:
                        self.employee_rank = employee.employment_rank.name
                        break           
                elif len(self.employee_rank) > 0:
                    for employee in model_hr_employmenthistorty_2:
                        self.employee_rank = employee.employment_rank.name
                        break        

        else:
            model_hr_employmenthistory = self.env['hr.employmenthistory'].search([('employee_employment_id', '=', self.id)])
            if len(model_hr_employmenthistory) > 0:
                model_hr_employmenthistorty_2 = model_hr_employmenthistory.sorted(key=lambda r: r.date_serviceto, reverse = True)
                for employee in model_hr_employmenthistorty_2:
                    self.employee_rank = employee.employment_rank.name
                    break            



    @api.multi
    def createExcelFile(self):
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
        sheet = workbook.add_sheet("Personnel")
        intRow = 0
        #REPORT TITLE
        sheet.write_merge(intRow,intRow+1, 0,10, "Personnel Information", styleHeader)  

        intRow+=2
        #COLUMNS  MAIN INFORMATION   
        sheet.write(intRow, 0,"Employee Number",styleColumns)
        sheet.write(intRow, 1, "First Name",styleColumns)
        sheet.write(intRow, 2, "Last Name",styleColumns)
        sheet.write(intRow, 3, "Middle Name",styleColumns)
        sheet.write(intRow, 4, "Allottee",styleColumns)
        sheet.write(intRow, 5, "Medical Condition",styleColumns)
        sheet.write(intRow, 6, "Shoe size",styleColumns)
        sheet.write(intRow, 7, "Place of birth",styleColumns)
        sheet.write(intRow, 8, "SSS No",styleColumns)
        sheet.write(intRow, 9, "HDMF No",styleColumns)
        sheet.write(intRow, 10, "Philhealth No",styleColumns)
        sheet.write(intRow, 11, "Tin",styleColumns)
        sheet.write(intRow, 12, "AA Register No",styleColumns)
        sheet.write(intRow, 13, "Service Length",styleColumns)
        sheet.write(intRow, 14, "Foclength",styleColumns)
        sheet.write(intRow, 15, "Incentive Length",styleColumns)
        sheet.write(intRow, 16, "Booking ID",styleColumns)
        sheet.write(intRow, 17, "Bank Account Number",styleColumns)
        sheet.write(intRow, 18, "Checklist ID",styleColumns)
        sheet.write(intRow, 19, "CCL Number",styleColumns)
        sheet.write(intRow, 20, "Religion",styleColumns)
        sheet.write(intRow, 21, "Marital Status",styleColumns)
        sheet.write(intRow, 22, "Rank",styleColumns)        
        intRow +=1

        #DETAILS
        sheet.write(intRow, 0, self.employee_number,styleColumns)
        sheet.write(intRow, 1, self.first_name,styleColumns)
        sheet.write(intRow, 2, self.last_name,styleColumns)
        sheet.write(intRow, 3, self.middle_name,styleColumns)
        sheet.write(intRow, 4, self.self_alotte,styleColumns)
        sheet.write(intRow, 5, self.weight,styleColumns)
        sheet.write(intRow, 6, self.height,styleColumns)
        sheet.write(intRow, 7, self.placeof_birth,styleColumns)
        sheet.write(intRow, 8, self.sss_no,styleColumns)
        sheet.write(intRow, 9, self.hdmf_no,styleColumns)
        sheet.write(intRow, 10, self.philhealth_no,styleColumns)
        sheet.write(intRow, 11, self.tin_no,styleColumns)
        sheet.write(intRow, 12, self.aa_reg_no,styleColumns)
        sheet.write(intRow, 13, self.service_length,styleColumns)
        sheet.write(intRow, 14, self.focllength,styleColumns)
        sheet.write(intRow, 15, self.incentive_length,styleColumns)
        sheet.write(intRow, 16, self.booking_id,styleColumns)
        sheet.write(intRow, 17, self.bankacctno,styleColumns)
        sheet.write(intRow, 18, self.checklistID,styleColumns)
        sheet.write(intRow, 19, self.ccl_number,styleColumns)
        sheet.write(intRow, 20, self.religion.name,styleColumns)
        sheet.write(intRow, 21, self.gender,styleColumns)
        sheet.write(intRow, 22, self.employee_rank,styleColumns)      
        intRow +=1     

        #COLUMNS  ADDRESS
        sheet.write_merge(intRow,intRow, 0,20, "ADDRESS")      
        intRow +=1
        for employee_address in self.employee_addresses:
            sheet.write(intRow, 0, employee_address.addresstype.name,styleColumns)
            sheet.write(intRow, 1, employee_address.address_1,styleColumns)
            sheet.write(intRow, 2, employee_address.address_2,styleColumns)
            sheet.write(intRow, 3, employee_address.address_3,styleColumns)
            sheet.write(intRow, 4, employee_address.city,styleColumns)
            sheet.write(intRow, 5, employee_address.province,styleColumns)
            sheet.write(intRow, 6, employee_address.country.name,styleColumns)
            sheet.write(intRow, 7, employee_address.telephone_number,styleColumns)
            sheet.write(intRow, 8, employee_address.mobile_number,styleColumns)
            sheet.write(intRow, 9, employee_address.email_number,styleColumns)          
            intRow +=1

        #COLUMNS  EDUCATION
        intRow +=1
        sheet.write_merge(intRow,intRow, 0,20, "EDUCATION")
        intRow +=1
        for employee_educ in self.employee_education:
            sheet.write(intRow, 0, employee_educ.schooltype.name,styleColumns)
            sheet.write(intRow, 1, employee_educ.name_school,styleColumns)
            sheet.write(intRow, 2, employee_educ.date_from,styleColumns)
            sheet.write(intRow, 3, employee_educ.date_to,styleColumns)
            sheet.write(intRow, 4, employee_educ.school_address,styleColumns)
            sheet.write(intRow, 5, employee_educ.description,styleColumns)          
            intRow +=1

        #COLUMNS  FAMILIES
        intRow +=1
        sheet.write_merge(intRow,intRow, 0,20, "FAMILIES")
        intRow +=1       

        for employee_family in self.employee_families:
            sheet.write(intRow, 0, employee_family.relation_level,styleColumns)
            sheet.write(intRow, 1, employee_family.first_name,styleColumns)
            sheet.write(intRow, 2, employee_family.last_name,styleColumns)
            sheet.write(intRow, 3, employee_family.middle_name,styleColumns)            
            sheet.write(intRow, 4, employee_family.relationship.name,styleColumns)
            sheet.write(intRow, 5, employee_family.address_1,styleColumns)
            sheet.write(intRow, 6, employee_family.address_2,styleColumns)
            sheet.write(intRow, 7, employee_family.address_3,styleColumns)
            sheet.write(intRow, 8, employee_family.is_beneficiary,styleColumns)
            sheet.write(intRow, 9, employee_family.is_allottee,styleColumns)
            sheet.write(intRow, 10, employee_family.is_living,styleColumns)
            sheet.write(intRow, 11, employee_family.occupation,styleColumns) 
            sheet.write(intRow, 12, employee_family.bank_details,styleColumns)
            sheet.write(intRow, 13, employee_family.telephone_number,styleColumns)
            sheet.write(intRow, 14, employee_family.mobile_number,styleColumns)
            sheet.write(intRow, 15, employee_family.email_number,styleColumns)
            sheet.write(intRow, 16, employee_family.city,styleColumns)
            sheet.write(intRow, 17, employee_family.province,styleColumns)
            sheet.write(intRow, 18, employee_family.country_id.name,styleColumns)
            sheet.write(intRow, 19, employee_family.gender,styleColumns)
            sheet.write(intRow, 20, employee_family.birthday,styleColumns)
            sheet.write(intRow, 21, employee_family.placeof_birth,styleColumns)
            intRow +=1  


        #COLUMNS  DOCUMENT
        intRow +=1
        sheet.write_merge(intRow,intRow, 0,20, "DOCUMENTS")
        intRow +=1      

        for employee_document in self.employee_documents:
            sheet.write(intRow, 0, employee_document.document.name,styleColumns)
            sheet.write(intRow, 1, employee_document.document_number,styleColumns)
            sheet.write(intRow, 2, employee_document.date_issued,styleColumns)
            sheet.write(intRow, 3, employee_document.date_expiry,styleColumns)            
            sheet.write(intRow, 4, employee_document.issuing_authority,styleColumns)
            sheet.write(intRow, 5, employee_document.place_ofissue,styleColumns)
            sheet.write(intRow, 6, employee_document.expired,styleColumns)
            intRow +=1           


        #COLUMNS  MEDICAL RECORDS
        intRow +=1
        sheet.write_merge(intRow,intRow, 0,20, "MEDICAL RECORDS")
        intRow +=1        
        for emloyee_med in self.emloyee_medical:
            sheet.write(intRow, 0, emloyee_med.medical_type.name,styleColumns)
            sheet.write(intRow, 1, emloyee_med.medical_clinic.name,styleColumns)
            sheet.write(intRow, 2, emloyee_med.date_from,styleColumns)
            sheet.write(intRow, 3, emloyee_med.date_to,styleColumns)            
            sheet.write(intRow, 4, emloyee_med.expired,styleColumns)
            intRow +=1           

        #COLUMNS  LICENSES
        intRow +=1
        sheet.write_merge(intRow,intRow, 0,20, "LICENSES")
        intRow +=1        

        for employee_license in self.employee_licenses:
            sheet.write(intRow, 0, employee_license.licensetype.name,styleColumns)
            sheet.write(intRow, 1, employee_license.license.name,styleColumns)
            sheet.write(intRow, 2, employee_license.doc_number,styleColumns)
            sheet.write(intRow, 3, employee_license.country.name,styleColumns)            
            sheet.write(intRow, 4, employee_license.date_issued,styleColumns)
            sheet.write(intRow, 5, employee_license.date_expiry,styleColumns)
            sheet.write(intRow, 6, employee_license.place_issue,styleColumns)
            sheet.write(intRow, 7, employee_license.authority_issue,styleColumns)
            sheet.write(intRow, 8, employee_license.remarks,styleColumns)
            intRow +=1 


        #COLUMNS  EMPLOYMENT HISTORY      
        intRow +=1
        sheet.write_merge(intRow,intRow, 0,20, "EMPLOYMENT HISTORY")
        intRow +=1        

        #HEADER
        sheet.write(intRow, 0, "Departure Date",styleColumns)
        sheet.write(intRow, 1, "Service from",styleColumns)
        sheet.write(intRow, 2, "Service to",styleColumns)
        sheet.write(intRow, 3, "Vessel",styleColumns)            
        sheet.write(intRow, 4, "Vessel Category",styleColumns)
        sheet.write(intRow, 5, "Vessel Department",styleColumns)
        sheet.write(intRow, 6, "Rank",styleColumns)
        sheet.write(intRow, 7, "Status", styleColumns)
        sheet.write(intRow, 8, "Remarks",styleColumns)
        sheet.write(intRow, 9, "Sign On",styleColumns)
        sheet.write(intRow, 10, "Sign Off",styleColumns)
        sheet.write(intRow, 11, "Service range",styleColumns)        
        intRow +=1        


        #DETAILS
        for employee_emp in self.employee_employment:
            sheet.write(intRow, 0, employee_emp.date_departure,styleColumns)
            sheet.write(intRow, 1, employee_emp.date_servicefrom,styleColumns)
            sheet.write(intRow, 2, employee_emp.date_serviceto,styleColumns)
            sheet.write(intRow, 3, employee_emp.object_code.name,styleColumns)            
            sheet.write(intRow, 4, employee_emp.object_code_category.name,styleColumns)
            sheet.write(intRow, 5, employee_emp.employment_dept_code.name,styleColumns)
            sheet.write(intRow, 6, employee_emp.employment_rank.name,styleColumns)
            sheet.write(intRow, 7, employee_emp.employment_status.name,styleColumns)
            sheet.write(intRow, 8, employee_emp.remarks,styleColumns)
            sheet.write(intRow, 9, employee_emp.place_signOn.name,styleColumns)
            sheet.write(intRow, 10, employee_emp.place_signOff.name,styleColumns)
            sheet.write(intRow, 11, employee_emp.service_range,styleColumns)
            intRow +=1             

        sheet.write_merge(intRow+1,intRow+1, 8,9, "Total Service Length")    
        sheet.write(intRow+1, 11, self.total_years_of_service,styleColumns)
        fp = StringIO()
        workbook.save(fp)
        fp.seek(0)
        data_read = fp.read()
        fp.close()
        byte_arr = base64.b64encode(data_read)
        mode_ir_attachment = self.env['ir.attachment']

        count_if_exist = mode_ir_attachment.search_count([('name','=', self.employee_number + ' Employee Information.xls')])
        if count_if_exist >0:
            model_file_ir_attachment = mode_ir_attachment.search([('name','=', self.employee_number + ' Employee Information.xls')])
            model_file_ir_attachment.write({'datas': byte_arr})
        else:
           mode_ir_attachment.create({
            'name': self.employee_number + ' Employee Information.xls',
            'type': 'binary',
            'datas': byte_arr,
            'description': 'Generated by Employee Information'
            })

        model_file_ir_attachment = mode_ir_attachment.search([('name','=', self.employee_number + ' Employee Information.xls')])
        return {
            'type' : 'ir.actions.act_url',
            #'url':   '/web/binary/saveas?model=ir.attachment&field=datas&filename_field=self.file_name&id=%s' % ( model_file_ir_attachment.id ),
            'url':   '/web/binary/saveas?model=ir.attachment&field=datas&filename_field=%s&id=%s' % ( model_file_ir_attachment.datas_fname,model_file_ir_attachment.id ),
            'target': 'self',
        }        





    # End Functions/Methods


    #-------- Attributes/Fields
    employee_number = fields.Char('Employee Number',select = True, default = _getEmpId)
    first_name = fields.Char('First name', required = True)
    last_name = fields.Char('Last name', required = True)
    middle_name = fields.Char('Middle name')
    self_alotte = fields.Boolean('Self Allottee?', default = True)
    weight = fields.Char('Medical Condition')
    height = fields.Char('Shoe Size')
    placeof_birth = fields.Char('Place of birth')
    sss_no = fields.Char('SSS No')
    hdmf_no = fields.Char('HDMF No')
    philhealth_no = fields.Char('Philhealth No')
    tin_no = fields.Char('Tin')
    aa_reg_no = fields.Char('AA Registry No')
    service_length = fields.Integer('Service Length')
    focllength = fields.Integer('Foclength')
    incentive_length = fields.Integer('Incentive Length')
    booking_id = fields.Char('Booking ID')
    bankacctno = fields.Text('Bank account number')
    checklistID = fields.Char('Checklist ID')
    ccl_number = fields.Char('CCL Number')
    religion = fields.Many2one('hr.religion', 'Religion')
    marital =  fields.Selection([('single', 'Single'), 
                                  ('married', 'Married'), 
                                  ('widower', 'Widower'), 
                                  ('divorced', 'Divorced'), 
                                  ('seperated', 'Seperated'), 
                                  ('live_in_partner', 'Live-in-partner')], 'Marital Status')
    employee_rank = fields.Text('Rank',store = False,compute ='_checkLatestEmployment')

    pcn = fields.Char('PCN')
    legacy_doc_1 = fields.Binary('Confidential Reports', filters='*.pdf,*.docx,*.doc')
    legacy_doc_2 = fields.Binary('Personal Data', filters='*.pdf,*.docx,*.doc')
    legacy_doc_3 = fields.Binary('Personal Summary', filters='*.pdf,*.docx,*.doc')
    employee_addresses = fields.One2many('hr.employeeaddress','employee_address_id', readonly=False,copy=False)
    employee_education = fields.One2many('hr.employeducation','employee_education_id', readonly=False,copy=False)
    employee_families = fields.One2many('hr.employee_families','employee_family_relationship_id', readonly=False,copy=False)
    employee_documents = fields.One2many('hr.employee_documents','employee_doc_id', readonly=False,copy=False)
    emloyee_medical = fields.One2many('hr.employee_medical_records','employee_med_rec_id', readonly=False,copy=False)
    employee_licenses = fields.One2many('hr.employeelicenses','employee_licenses_id', readonly=False,copy=False)
    employee_employment = fields.One2many('hr.employmenthistory','employee_employment_id', readonly=False,copy=False)
    employee_checklists = fields.One2many('hr.employee_checklist','employee_id', readonly=False,copy=False)

    employee_checklists_documents = fields.One2many('hr.employee.checklist.documents','employee_id', readonly=False,copy=False)
    
    employee_id = fields.Integer('employee_id', readonly=False,copy=False,store =False, compute='getEmployeeID')
    documents_status = fields.Boolean('Document status', readonly = True,store = False,compute ='getdocumentStatus')
    medical_status = fields.Boolean('Medical documents', readonly = True,store = False,compute ='getMedicalStatus')
    filename = fields.Char('file name', readonly = True,store = False,compute ='legacy_doc1_getFilename')
    filename2 = fields.Char('file name', readonly = True,store = False,compute ='legacy_doc2_getFilename')
    filename3 = fields.Char('file name', readonly = True,store = False,compute ='legacy_doc3_getFilename')
    description = fields.Text('Description')
    checklist_count =  fields.Integer('Checklist', store = False, compute = "_checklist_count")

    confidential_file = fields.Char('Confidential File')
    personal_file = fields.Char('Personal File')
    personalsummary_file = fields.Char('File Personnal Summary')
    image_file = fields.Char('Image File Summary')

    employee_contract_number = fields.Char('Employee Contract Number', required=True, default='N/A')
    total_years_of_service = fields.Char('Service Length',store = False,compute ='getYearMonthDay')    

    @api.one
    def getYearMonthDay(self):

        str_service_range = ''
        int_year    = 0
        int_month   = 0
        int_day     = 0

        int_final_year  = 0
        int_final_month = 0
        int_final_day   = 0


        str_final_year  = ''
        str_final_month = ''
        str_final_day   = ''

        for employment_history in self.employee_employment:
            str_service_range = employment_history.service_range
            str_service_range = str_service_range.split()
            if employment_history.employment_status.status_id == 'ACT':
                int_year = int(str_service_range[0].replace('Y',''))
                int_month = int(str_service_range[1].replace('M',''))
                int_day = int(str_service_range[2].replace('D',''))
                int_final_year +=int_year
                int_final_month +=int_month
                int_final_day +=int_day

        if int_final_day > 30:
            int_final_month += int(int_final_day/30)
            int_final_day = (float(int_final_day)/30)  - int(int_final_day/30.00) 
            if int_final_day > 0:
                int_final_day = 30 * int_final_day

        if int_final_month > 12:
            int_final_year += int_final_month/12.00
            str_final_year = str(int_final_year)

            int_final_year = int(str_final_year.split('.')[0])
            int_final_month =  float('.' + str_final_year.split('.')[1])
            if int_final_month > 0:
                int_final_month = int(round(12 * int_final_month))

        self.total_years_of_service = str(int_final_year) + 'Y ' + str(int_final_month) + 'M ' +  str(int_final_day).split('.')[0]  + 'D'    

class HrEmployeeAddresses(models.Model):
    _name = 'hr.employeeaddress'
    employee_address_id = fields.Many2one('hr.employee','Employee Addresses')
    addresstype = fields.Many2one('hr.addresstype','Address Type')
    address_1 = fields.Char('Address 1')
    address_2 = fields.Char('Address 2')
    address_3 = fields.Char('Address 3')
    city = fields.Char('City')
    province = fields.Char('Province')
    country = fields.Many2one('res.country', 'Country')
    telephone_number = fields.Char('Landline number')
    mobile_number = fields.Char('Mobile number')
    email_number = fields.Char('E-mail')

class HrEmployeeEducation(models.Model):
    _name = 'hr.employeducation'
    employee_education_id = fields.Many2one('hr.employee')
    schooltype = fields.Many2one('hr.recruitment.degree','Degree')
    name_school = fields.Char('School/College University')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    school_address = fields.Char('Place')
    description = fields.Text('Remarks')

    @api.onchange('date_to')
    def checkDate(self):
        if self.date_to < self.date_from:
            raise ValidationError('Date to is less than the Date from.')

    @api.constrains('date_to','date_from')
    def checkConstrainDate(self):
        if self.date_to < self.date_from:
            raise ValidationError('Date to is less than the Date from.')

class HrEmployeeFamilies(models.Model):
    _name = 'hr.employee_families'
    _order = 'employee_family_relationship_id,relation_level'


    @api.model
    def getLastLevel(self):
        return 1

    # Overrides
    @api.model
    def create(self, vals):
        count_employee_families = self.env['hr.employee_families'].search_count([('employee_family_relationship_id', '=', vals['employee_family_relationship_id']),
                                                                            ('relation_level', '=', vals['relation_level'])])
        #if count_employee_families > 0:
        #    raise Warning('Relation Level has already define in Employee families.')
        new_record = super(HrEmployeeFamilies, self).create(vals)
        return new_record    

    @api.multi
    def write(self, vals):
        count_employee_families = self.env['hr.employee_families'].search_count([('employee_family_relationship_id', '=', self.employee_family_relationship_id.id),
                                                                            ('relation_level', '=', self.relation_level)])
        #if count_employee_families > 0:
        #    raise Warning('Relation Level has already define in Employee families.')
        super(HrEmployeeFamilies, self).write(vals)
        return True            

    employee_family_relationship_id = fields.Many2one('hr.employee')
    relation_level = fields.Integer('Level', default = getLastLevel)
    relationship = fields.Many2one('hr.familyrelations','Relationship')
    address_1 = fields.Char('Address 1')
    address_2 = fields.Char('Address 2')
    address_3 = fields.Char('Address 3')
    is_beneficiary = fields.Boolean('Beneficiary', default = True)
    is_allottee = fields.Boolean('Allottee', default = True)
    is_living = fields.Boolean('Living', default = True)
    occupation = fields.Char('Occupation')
    bank_details = fields.Text('Bank Details')
    telephone_number = fields.Char('Landline number')
    mobile_number = fields.Char('Mobile number')
    email_number = fields.Char('E-mail')
    city = fields.Char('City')
    province = fields.Char('Province')
    country_id = fields.Many2one('res.country', 'Nationality')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')
    birthday = fields.Date("Date of Birth")
    full_name = fields.Char('Name', readonly=True)
    first_name = fields.Char('First name') #required = True
    last_name = fields.Char('Last name') #required = True
    middle_name = fields.Char('Middle name') #required = True
    placeof_birth = fields.Char('Place of birth')

class HrEmployeeDocuments(models.Model):
    _name = 'hr.employee_documents'

    _order = 'date_expiry,date_expiry,document'

    employee_doc_id =  fields.Many2one('hr.employee')
    document = fields.Many2one('hr.documenttype','Document Type')
    document_number = fields.Char('Document ID')
    date_issued = fields.Date('Date Issued',default = DATE_NOW)
    date_expiry = fields.Date('Date Expiry',default = DATE_NOW)
    issuing_authority = fields.Char('Issuing Authority')
    place_ofissue = fields.Char('Place of Issue')
    expired = fields.Char('Expired?',store = False,compute ='checkDocExpiration')

    @api.one
    def checkDocExpiration(self):

        if not isinstance(self.document, bool):
            server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")

            if self.document.check_for_expiration == True:
                if (self.date_expiry == False):
                    self.expired = 'NOT'
                else:
                    dt_date_expiry = datetime.datetime.strptime(self.date_expiry ,"%Y-%m-%d")
                    if dt_date_expiry < server_date:
                        self.expired = 'EXP'
                    else:
                        self.expired = 'NOT'
            else:
                self.expired = 'NOT'
        else:
            self.expired = 'NOT'

    @api.onchange('date_expiry')
    def checkDate(self):        
        if self.date_expiry < self.date_issued:
            raise ValidationError('Date expiry is less than the Date issued.')

    @api.constrains('date_issued','date_expiry' )
    def checkConstrainDate(self):
        if self.date_expiry < self.date_issued:
            raise ValidationError('Date expiry is less than the Date issued.')

    #@api.constrains('document')
    #def checkDocumentExists(self):
        #raise Warning(int(self.employee_doc_id[0]))
    #    if len(self.document) > 0:
    #        totaldoc = self.env['hr.employee_documents'].search_count([('document', '=', int(self.document)),
    #                                                                   ('employee_doc_id','=', int(self.employee_doc_id[0]))])
    #        if totaldoc > 0:
    #            raise Warning('Selected documents already exists.')

    #@api.one
    #@api.onchange('document')
    #def checkDocumentsExists(self):
    #    if not isinstance(self.id, models.NewId):
            #raise Warning(int(self.employee_doc_id))
    #        totaldoc = self.env['hr.employee_documents'].search_count([('document', '=', self.document),('employee_doc_id','=', int(self.employee_doc_id)),
    #                                                                    ('expired', '=', 'NOT')])
    #        if totaldoc > 0:
    #            raise ValidationError('Selected documents has already exists.')

class HrEmployeeMedicalRecords(models.Model):
    _name = 'hr.employee_medical_records'
    employee_med_rec_id = fields.Many2one('hr.employee')
    medical_type = fields.Many2one('hr.medicalrecord','Medical')
    medical_clinic = fields.Many2one('hr.clinic','Clinic')
    date_from = fields.Date('Date From') #,required = True
    date_to = fields.Date('Date To') #,required = True
    expired = fields.Char('Expired?',store = False,compute ='checkDocExpiration')

    @api.constrains('date_from','date_to')
    def checkConstrainDate(self):

        if not isinstance(self.date_from,bool):
            if len(self.date_from) > 0:
                if self.date_to < self.date_from:
                    pass
                    #raise ValidationError('Date to is less than the Date from.')

    @api.one
    def checkDocExpiration(self):
        self.expired = 'NOT'
        #server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
        #dt_date_expiry = datetime.datetime.strptime(self.date_to ,"%Y-%m-%d")
        #if self.date_to == False:
        ##    self.expired = 'NOT'
        #else:
        #    if dt_date_expiry < server_date:
        #        self.expired = 'EXP'
        #    else:
        #        self.expired = 'NOT'
        #ZAPATA ERROR

    @api.onchange('date_to')
    def checkDate(self):

        if not isinstance(self.date_from,bool):
            if len(self.date_from) > 0:
                if self.date_to < self.date_from:
                    raise ValidationError('Date to is less than the Date from.')

    #@api.constrains('medical_type')
    #def checkMedicalType(self):
        #raise Warning(int(self.employee_doc_id[0]))
    #    if len(self.medical_type) > 0:
    #        if self.env['hr.employee_medical_records'].search_count([ ('employee_med_rec_id','=', int(self.employee_med_rec_id[0]))]) > 0:
    #            totaldoc = self.env['hr.employee_medical_records'].search_count([('medical_type', '=', int(self.medical_type)),
    #                                                                       ('employee_med_rec_id','=', int(self.employee_med_rec_id[0]))])
    #            if totaldoc > 0:
    #                raise ValidationError('Selected Medical documents already exists.')

class HrEmployeeLicenses(models.Model):
    _name = 'hr.employeelicenses'

    employee_licenses_id = fields.Many2one('hr.employee')
    licensetype = fields.Many2one('hr.licensetype','License Type', required=True)
    license = fields.Many2one('hr.license','License') #, required=True
    doc_number = fields.Char('Document Number', required=True)
    country = fields.Many2one('res.country', 'Country', required=True)
    #old
    #date_issued = fields.Date('Issue', required=True)
    #date_expiry = fields.Date('Expiry', required=True)
    date_issued = fields.Date('Issue')
    date_expiry = fields.Date('Expiry')    
    place_issue = fields.Char('Place Issue', required=True)
    authority_issue = fields.Char('Authority Issue')
    remarks = fields.Text('Remarks')

    #@api.constrains('date_issued','date_expiry')
    #def checkConstrainDate(self):
    #    if self.date_expiry < self.date_issued:
    #        raise ValidationError('Date expiry is less than the Date issued.')

    #@api.onchange('date_expiry')
    #def checkDate(self):
    #    if self.date_expiry < self.date_issued:
    #        raise ValidationError('Date expiry is less than the Date issued.')

    #@api.one
    #@api.onchange('licensetype')
    #def getlicense(self):
    #    if len(self.licensetype) > 0:
    #        mdlLicense= self.env['hr.license'].search([('license_name', '=', int(self.licensetype[0]))])
            #raise Warning(mdlLicense.ids)
    #        self.license = mdlLicense.ids

    #@api.onchange('license')
    #def getlicense(self):
    #    if len(self.licensetype) > 0:
    #        mdlLicense= self.env['hr.license'].search([('license_name', '=', int(self.licensetype[0]))])
            #raise Warning(mdlLicense.ids)
    #        return mdlLicense.ids

class HrEmployeeEmployment(models.Model):
    YEAR = 365
    MONTH = 30
    
    _name = 'hr.employmenthistory'
    _order =  'employee_employment_id, date_servicefrom desc'


    employee_employment_id = fields.Many2one('hr.employee')
    date_departure =fields.Date('Departure Date')
    date_servicefrom =fields.Date('Service from')
    date_serviceto =fields.Date('Service to')
    object_name = fields.Char('Object')
    object_code = fields.Many2one('hr.vessel','Vessel') #, required =True
    object_code_category = fields.Many2one('hr.vesselcategory','Vessel Category')
    employment_dept_code = fields.Many2one('hr.ship.department','Department') #, required =True
    employment_rank = fields.Many2one('hr.rank','Rank')
    employment_status = fields.Many2one('hr.employment.status','Status')
    remarks = fields.Text('Remarks')
    place_signOn = fields.Many2one('hr.port', 'Sign On')
    place_signOff = fields.Many2one('hr.port', 'Sign Off')
    service_range = fields.Char('Service range',store = False,compute ='getYearMonthDay')

    @api.onchange('object_code')
    def _changeCategory(self):
        self.object_code_category = self.object_code.vessel_category


    @api.one
    def getYearMonthDay(self):

        if self.date_servicefrom == False or self.date_serviceto == False:
            self.service_range = '0Y 0M 0D'
        else:
            date_from = datetime.datetime.strptime(self.date_servicefrom ,"%Y-%m-%d")
            date_to = datetime.datetime.strptime(self.date_serviceto ,"%Y-%m-%d")
            no_of_days = abs((date_to - date_from).days) + 1
            # Get Years of Service


            #raise Warning(no_of_days)
            no_of_years = abs(no_of_days/365)
            no_of_days =  no_of_days - (no_of_years * 365)
            no_of_months = abs(no_of_days/30)
            no_of_days = no_of_days - (no_of_months * 30)
            no_of_day = no_of_days

            self.service_range = str(no_of_years) + 'Y ' + str(no_of_months) + 'M ' +  str(no_of_day)  + 'D'

    #@api.onchange('date_servicefrom')
    #def checkDate(self):
    #    if self.date_servicefrom < self.date_departure:
    #        raise ValidationError('Date service from is less than the Departure date.')

    #@api.onchange('date_serviceto')
    #def checkDate(self):
    #   if self.date_serviceto < self.date_servicefrom:
    #        raise ValidationError('Date service to is less than the Date service from.')

    #@api.constrains('date_servicefrom')
    #def checkConstrainDate(self):
    #    if self.date_servicefrom < self.date_departure:
    #        raise ValidationError('Date service from is less than the Date departure.')

    #@api.constrains('date_serviceto')
    #def checkConstrainDate(self):
    #    if self.date_serviceto < self.date_servicefrom:
    #        raise ValidationError('Date service to is less than the Date service from.')
#OLD
class EmployeeCheckList(models.Model):
    _name = 'hr.employee_checklist'
    employee_id = fields.Many2one('hr.employee')
    checklist_template_id = fields.Many2one('hr.checklist_template')

    param_name_1 = fields.Many2one('hr.checklist', 'Parameter 1')
    param_name_2 = fields.Many2one('hr.checklist', 'Parameter 2')
    param_name_3 = fields.Many2one('hr.checklist', 'Parameter 3')

    param_name_1_value = fields.Char("Parameter 1 value")
    param_name_2_value = fields.Char("Parameter 2 value")
    param_name_3_value = fields.Char("Parameter 3 value")

    param_name_1_check = fields.Boolean("Parameter 1 Checked?")
    param_name_2_check = fields.Boolean("Parameter 2 Checked?")
    param_name_3_check = fields.Boolean("Parameter 3 Checked?")

    param_name_1_value_visible = fields.Boolean("Parameter 1 Value visible?")
    param_name_2_value_visible = fields.Boolean("Parameter 2 Value visible?")
    param_name_3_value_visible = fields.Boolean("Parameter 3 Value visible?")

    issued_at = fields.Char("Issued at")
    date_issued = fields.Date("Date issued")
    date_expiry = fields.Date("Date Expiry")

    @api.onchange('date_expiry')
    def checkDate(self):
        if self.date_expiry < self.date_issued:
            raise ValidationError('Date expiry is less than the Date issued.')

class EmployeeChecklist(models.Model):
    _name = "hr.employee.checklist.documents"
    _inherit = 'mail.thread'
    _order =  'checklist_no, name'



    employee_id = fields.Many2one('hr.employee')

    checklist_no = fields.Integer('Checklist No.', store=True) #, compute = "readonly_values"
    name = fields.Char('Name', store=True) # , compute = "readonly_values"
    employee_number = fields.Char('Employee Number', store=True, compute = "readonly_values")
    joining_date = fields.Date('Joining Date')
    vessel_information = fields.Char('Vessel', store=True, compute = "readonly_values")
    position_information = fields.Char('Position', store=True, compute = "readonly_values")
    medical_date = fields.Char('Date of Med')
    visa_date = fields.Char('Date of Visa')
    contact_number = fields.Char('Contact Number')
    signoff_date = fields.Date('Date Signoff')
    reported_date = fields.Date('Date Reported') 

    employee_checklists_documents_list = fields.One2many('hr.employee.checklist.documents.list','employee_checklist_document', readonly=False,copy=False)
    employee_checklists_documents_list_main = fields.One2many('hr.employee.checklist.documents.list.main','employee_checklist_document', readonly=False,copy=False)

    #Other Data
    us_visa_boolean = fields.Boolean('US Visa', default= False)
    us_visa_latest_document = fields.Char('US Visa Document ID')
    us_visa_previous_document = fields.Char('US Visa Previous Document ID')
    us_visa_IssuedAt_document = fields.Char('US Visa Previous Document ID')    
    us_visa_expiring_date = fields.Date('Expiring Date')


    us_visa2_boolean = fields.Boolean('VISA II', default= False)
    us_visa2_latest_document = fields.Char('VISA II ID')
    us_visa2_previous_document = fields.Char('VISA II Previous Document ID')
    us_visa2_IssuedAt_document = fields.Char('VISA II Previous Document ID')    
    us_visa2_expiring_date = fields.Date('Expiring Date')

    peme_boolean = fields.Boolean('PEME', default= False)
    peme_latest_document = fields.Char('Peme')
    peme_schedule_date = fields.Date('Schedule')
    clinic = fields.Char('Clinic')


    def getUseridName(self):
        return self.env['res.users'].search([('id','=', self._uid)]).name


    #Remove all edited and updated records and get 
    #all the records again
    @api.one 
    def regenerateChecklistDocuments(self):
        server_date = DATE_NOW.strftime("%d/%m/%Y")
        model_list_document_main =self.env['hr.employee.checklist.documents.list'].search([('employee_checklist_document', '=', self.id)])
        model_list_document =self.env['hr.employee.checklist.documents.list.main'].search([('employee_checklist_document', '=', self.id)])

        model_checklist_document = self.env['hr.employee.checklist.documents'].search([('id', '=', self.id)])
        #Remove first all the Data
        model_list_document_main.unlink()
        model_list_document.unlink()
        self.createChecklistDocumentList(model_checklist_document)
        self.createChecklistDocumentList_main(model_checklist_document)

        for document in self.employee_checklists_documents_list:
            model_res_users = self.env['res.users'].search([('id', '=', self._uid)])
            document.change_by = model_res_users.name
            document.change_date = server_date

        message ="""<span>Regenerate Checklist</span>
                    <div><b>Triggered by</b>: %(user)s </div>
                    """ %{'user': self.getUseridName()}
        self.message_post(body=message)


    @api.one
    def updateChecklist(self):
        self.createChecklistDocumentList('')

        message ="""<span>Automated updating of Checklist</span>
                    <div><b>Triggered by</b>: %(user)s </div>
                    """ %{'user': self.getUseridName()}
        self.message_post(body=message)        


    def readonly_values_2(self, vals):
        values = {}
        server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
        employee_info_model = self.env['hr.employee'].search([('id', '=', vals['employee_id'])])
        values.update({'name': employee_info_model.last_name + ", " + employee_info_model.first_name })
        values.update({'employee_number': employee_info_model.employee_number})

        employment_history_model = self.env['hr.employmenthistory'].search([('employee_employment_id', '=', employee_info_model.id), 
                                                                            ('date_serviceto', '>=', server_date)], limit = 1)

        total_checklist_document = self.env['hr.employee.checklist.documents'].search_count([('employee_id', '=', employee_info_model.id)])
        if total_checklist_document  == 0:
            values.update({'checklist_no': 1})
        else:
            values.update({'checklist_no': total_checklist_document + 1})

        values.update({'vessel_information': employment_history_model.object_code.name})
        values.update({'position_information': employment_history_model.employment_rank.name})
        return values

    def readonly_values(self):

        self.name = self.employee_id.last_name + ", " + self.employee_id.first_name
        self.employee_number = self.employee_id.employee_number
        #Get the Employment History
        server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")
        employment_history_model = self.env['hr.employmenthistory'].search([('employee_employment_id', '=', self.employee_id.id), 
                                                                            ('date_serviceto', '>=', server_date)], limit = 1)


        # Get the Checklist Number
        total_checklist_document = self.env['hr.employee.checklist.documents'].search_count([('employee_id', '=', self.employee_id.id)])
        if self.checklist_no == 0:
            if total_checklist_document == 0:
                self.checklist_no = 1
            else:
                self.checklist_no = total_checklist_document + 1

        #Get the Vessel Information
        if isinstance(self.vessel_information, bool):
            self.vessel_information = employment_history_model.object_code.name
        elif len(self.vessel_information) == 0:
            self.vessel_information = employment_history_model.object_code.name
            
        #Get the Position
        if isinstance(self.position_information, bool):
            self.position_information = employment_history_model.employment_rank.name
        elif len(self.position_information) == 0:
            self.position_information = employment_history_model.employment_rank.name

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.readonly_values()

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

        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_US_VISA_PREVIOUS_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_2': temp_1,
                    'param_name_2_value': '',
                    'param_name_2_check': False,
                    'param_name_2_value_visible':  True,
                    'param_name_2_check_visible':  False,
                    })


        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_US_VISA_ISSUED_AT_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_3': temp_1,
                    'param_name_3_value': '',
                    'param_name_3_check': False,
                    'param_name_3_value_visible':  True,
                    'param_name_3_check_visible':  False,
                    })
        rec = employeeChecklist.create(vals)
        rec.getEmployeeDocuments_Temporary(rec)
        #FOR US VISA EXPIRATION DATE
        vals = {'employee_checklist_document': record_id}
        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_US_VISA_EXPIRY_DATE_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_2': temp_1,
                    'param_name_2_value': '',
                    'param_name_2_check': False,
                    'param_name_2_value_visible':  True,
                    'param_name_2_check_visible':  False,
                    })
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

        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_SCHEDULE_PEME_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_2': temp_1,
                    'param_name_2_value': '',
                    'param_name_2_check': False,
                    'param_name_2_value_visible':  True,
                    'param_name_2_check_visible':  False,
                    })


        checklistTemplates = self.env['hr.checklist'].search([('checklist_code', '=', 'CODE_PEME_CLINIC_CONSTANT')])
        temp_1 = checklistTemplates.id
        vals.update({
                    'param_name_3': temp_1,
                    'param_name_3_value': '',
                    'param_name_3_check': False,
                    'param_name_3_value_visible':  True,
                    'param_name_3_check_visible':  False,
                    })
        employeeChecklist.create(vals)

    @api.model
    def createChecklistDocumentList(self, pObjRecord):
        checklistTemplates = self.env['hr.checklist_template'].search([])
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
                #Get First all the Documents Needed OLd new and How the Field has been setup by the User in 
                #Checklist Template
                #raise Warning('1111111')
                employee_checklist_id = employeeChecklist.create({
                    'employee_checklist_document': record_id,
                    'checklist_template_id': checklistTemplate.id,
                    'param_name_1': temp_1,
                    'param_name_1_value': '',
                    'param_name_1_check': False,
                    'param_name_2': temp_2,
                    'param_name_2_value': ALT_255,
                    'param_name_2_check': False,
                    'param_name_3': temp_3,
                    'param_name_3_value': '',
                    'param_name_3_check': False,
                    'param_name_4': temp_4,
                    'param_name_4_value': '',
                    'param_name_4_check': False,
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

    # Overrides
    @api.model
    def create(self, vals):
        readony_fields = self.readonly_values_2(vals)
        for readonly_field in readony_fields:
            vals.update({readonly_field: readony_fields[readonly_field]})
        new_record = super(EmployeeChecklist, self).create(vals)

        if not new_record.employee_checklists_documents_list:
            self.createChecklistDocumentList(new_record)
        if not new_record.employee_checklists_documents_list_main:
            self.createChecklistDocumentList_main(new_record)
        return new_record    


    @api.multi
    def write(self, vals):
        server_date = DATE_NOW.strftime("%d/%m/%Y")


        super(EmployeeChecklist, self).write(vals)

        if vals.has_key('employee_checklists_documents_list'):
            checklist_documents = vals['employee_checklists_documents_list']
            for checklist_document in checklist_documents:
                #To Check if Row is being Updated
                #if Updated Add the Value in Change by and Date Updated
                if checklist_document[2]:
                    model_list_document_main =self.env['hr.employee.checklist.documents.list'].search([('employee_checklist_document', '=', self.id),
                                                                                                       ('id','=', checklist_document[1])])

                    model_list_document_main.write({
                        'change_by': self.getUseridName(),
                        'change_date': server_date
                        })







        #self.createChecklistDocumentList('')
        return True


class EmployeeChecklist_list(models.Model):
    _name = "hr.employee.checklist.documents.list"

    checklist_template_id = fields.Many2one('hr.checklist_template')
    employee_checklist_document = fields.Many2one('hr.employee.checklist.documents')       


    param_name_1 = fields.Many2one('hr.checklist', 'Parameter 1')
    param_name_2 = fields.Many2one('hr.checklist', 'Parameter 2')
    param_name_3 = fields.Many2one('hr.checklist', 'Parameter 3')
    param_name_4 = fields.Many2one('hr.checklist', 'Parameter 4')

    param_name_1_value = fields.Char("Parameter 1 value")
    param_name_2_value = fields.Char("Parameter 2 value")
    param_name_3_value = fields.Char("Parameter 3 value")
    param_name_4_value = fields.Char("Parameter 4 value")

    param_name_1_check = fields.Boolean("Parameter 1 Checked?")
    param_name_2_check = fields.Boolean("Parameter 2 Checked?")
    param_name_3_check = fields.Boolean("Parameter 3 Checked?")
    param_name_4_check = fields.Boolean("Parameter 4 Checked?")

    param_name_1_value_visible = fields.Boolean("Parameter 1 Value visible?")
    param_name_2_value_visible = fields.Boolean("Parameter 2 Value visible?")
    param_name_3_value_visible = fields.Boolean("Parameter 3 Value visible?")
    param_name_4_value_visible = fields.Boolean("Parameter 4 Value visible?")


    param_name_1_check_visible = fields.Boolean("Parameter 1 Check visible?")
    param_name_2_check_visible = fields.Boolean("Parameter 2 Check visible?")
    param_name_3_check_visible = fields.Boolean("Parameter 3 Check visible?")
    param_name_4_check_visible = fields.Boolean("Parameter 4 Check visible?")

    has_date_issued = fields.Boolean("Date Issued Enable?")
    has_issued_at = fields.Boolean("Issued At Enable?")
    has_date_expiry = fields.Boolean("Date Expiry Enable?")            
    has_changed_by = fields.Boolean("Change by Enable")            
    has_change_date = fields.Boolean("Date Change Enable?")            

    issued_at = fields.Char("Issued at")
    date_issued = fields.Date("Date issued")
    date_expiry = fields.Date("Date Expiry")
    change_by = fields.Char("Change By")
    change_date = fields.Char("Change Date")



    #Override Functions

    #@api.multi
    #def write(self, vals):
    #    raise Warning('YAHOO')
    #    super(EmployeeChecklist_list, self).write(vals)







    @api.model
    def getEmployeeMedicalRecord(self, pchecklist, pfield_name, pemployee_id):
        model_employee_medical = self.env['hr.employee_medical_records'].search([('employee_med_rec_id', '=', pemployee_id)])
        model_employee_medical_ret =  model_employee_medical.search([('medical_type', '=',pchecklist.param_name_1.link_medical_type.id)])
        if pfield_name == 'param_name_1':
            parameter_field = pchecklist.param_name_1
            str_parameter_value = 'param_name_1_value'
            str_parameter_check = 'param_name_1_check'
        elif pfield_name == 'param_name_2':
            parameter_field = pchecklist.param_name_2
            str_parameter_value = 'param_name_2_value'
            str_parameter_check = 'param_name_2_check'            
        elif pfield_name == 'param_name_3':
            parameter_field = pchecklist.param_name_3
            str_parameter_value = 'param_name_3_value'
            str_parameter_check = 'param_name_3_check'  

        write_values = {}
        if not isinstance(parameter_field, bool):
            if len(parameter_field) > 0:
                #Get Document Properties

                if parameter_field.link_selection == 'medical':
                    model_employee_medical_ret =  model_employee_medical.search([('medical_type', '=',pchecklist.param_name_1.link_medical_type.id),
                                                                                 ('employee_med_rec_id', '=', pemployee_id)])
                    if parameter_field.retrieve_history_records == 'latest_doc':
                        for license  in model_employee_medical_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                            write_values.update({str_parameter_check: 1})
                            break
                    elif parameter_field.retrieve_history_records == 'oldest_doc':
                        int_counter_record = 0
                        if len(model_employee_medical_ret) > 1:
                             for license  in model_employee_medical_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                                if int_counter_record >= 1:
                                    write_values.update({str_parameter_check: 1})
                                    break         
                                int_counter_record +=1     
        return write_values  


    @api.model
    def getEmployeeLicenses(self, pchecklist, pfield_name, pemployee_id):
        model_employee_license = self.env['hr.employeelicenses'].search([('employee_licenses_id', '=', pemployee_id)])
        model_employee_license_ret =  model_employee_license.search([('license', '=',pchecklist.param_name_1.link_license_type.id)])
        if pfield_name == 'param_name_1':
            parameter_field = pchecklist.param_name_1
            str_parameter_value = 'param_name_1_value'
            str_parameter_check = 'param_name_1_check'
        elif pfield_name == 'param_name_2':
            parameter_field = pchecklist.param_name_2
            str_parameter_value = 'param_name_2_value'
            str_parameter_check = 'param_name_2_check'            
        elif pfield_name == 'param_name_3':
            parameter_field = pchecklist.param_name_3
            str_parameter_value = 'param_name_3_value'
            str_parameter_check = 'param_name_3_check'  


        write_values = {}
        if not isinstance(parameter_field, bool):
            if len(parameter_field) > 0:
                #Get Document Properties

                if parameter_field.link_selection == 'license':
                    #raise Warning(checklist.param_name_1.link_document_type.id)
                    #Check what Kind of Kind of Records will be retrieve e.g. Old or New Records
                    #model_employee_document_ret =  model_employee_document.search([('document', '=',checklist.param_name_1.link_document_type.id),
                    #                                                                ('date_issued' ,'<=', server_date),
                    #                                                                ('date_expiry' ,'>=', server_date)])
                    #model_employee_document_ret =  model_employee_license.search([('license', '=',parameter_field.link_license_type.id)])
                    model_employee_license_ret =  model_employee_license.search([('license', '=',parameter_field.link_license_type.id),
                                                                                 ('employee_licenses_id', '=', pemployee_id)])
                    if parameter_field.retrieve_history_records == 'latest_doc':
                        for license  in model_employee_license_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                            write_values.update({str_parameter_value: license.doc_number,
                                                 str_parameter_check: 1})
                            break
                    elif parameter_field.retrieve_history_records == 'oldest_doc':
                        int_counter_record = 0
                        if len(model_employee_license_ret) > 1:
                             for license  in model_employee_license_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                                if int_counter_record >= 1:
                                    write_values.update({str_parameter_value: license.doc_number,
                                                         str_parameter_check: 1})
                                    break         
                                int_counter_record +=1     
        return write_values               

    @api.model
    def getEmployeeDocuments(self, pchecklist, pfield_name, pemployee_id):
        model_employee_document = self.env['hr.employee_documents'].search([('employee_doc_id', '=', pemployee_id)])
        model_employee_document_ret =  model_employee_document.search([('document', '=',pchecklist.param_name_1.link_document_type.id)])
        


        if pfield_name == 'param_name_1':
            parameter_field = pchecklist.param_name_1
            str_parameter_value = 'param_name_1_value'
            str_parameter_check = 'param_name_1_check'
        elif pfield_name == 'param_name_2':
            parameter_field = pchecklist.param_name_2
            str_parameter_value = 'param_name_2_value'
            str_parameter_check = 'param_name_2_check'            
        elif pfield_name == 'param_name_3':
            parameter_field = pchecklist.param_name_3
            str_parameter_value = 'param_name_3_value'
            str_parameter_check = 'param_name_3_check'  

        write_values = {}
        if not isinstance(parameter_field, bool):
            if len(parameter_field) > 0:
                #Get Document Properties

                if parameter_field.link_selection == 'document':
                    #raise Warning(checklist.param_name_1.link_document_type.id)
                    #Check what Kind of Kind of Records will be retrieve e.g. Old or New Records
                    #model_employee_document_ret =  model_employee_document.search([('document', '=',checklist.param_name_1.link_document_type.id),
                    #                                                                ('date_issued' ,'<=', server_date),
                    #                                                                ('date_expiry' ,'>=', server_date)])
                    model_employee_document_ret =  model_employee_document.search([('employee_doc_id', '=', pemployee_id),
                                                                                   ('document', '=',parameter_field.link_document_type.id)])
                    #raise Warning(len(model_employee_document_ret))
                    #raise Warning(checklist.param_name_1.link_document_type.name)
                    if parameter_field.retrieve_history_records == 'latest_doc':
                        for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                            write_values.update({str_parameter_value: document.document_number,                                                
                                                 str_parameter_check: 1,})

                            if pchecklist.checklist_template_id.checklist_temp_row_with_dateissued:
                                write_values.update({'issued_at': document.place_ofissue,
                                                     'date_issued': document.date_issued})

                            if pchecklist.checklist_template_id.checklist_temp_param_1_with_dateexpired:
                                write_values.update({'date_expiry': document.date_expiry})


                            break
                    elif parameter_field.retrieve_history_records == 'oldest_doc':
                        int_counter_record = 0
                        if len(model_employee_document_ret) > 1:
                             for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                                if int_counter_record >= 1:

                                    write_values.update({str_parameter_value: document.document_number,
                                                         str_parameter_check: 1,
                                                         'param_name_2_value':document.date_expiry})
                                    break         
                                int_counter_record +=1     
        return write_values               

    @api.model
    def getDataFromDocuments(self, pchecklist_document_id, employee_id):
        model_checklist_document_list = self.env[self._name].search([('employee_checklist_document', '=', pchecklist_document_id)])
        
        if len(model_checklist_document_list) > 0:

            server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")

            for checklist in model_checklist_document_list:
                write_values = {}
                write_values_final = {}    
                write_values = self.getEmployeeDocuments(checklist, 'param_name_1',employee_id)
                write_values_final.update(write_values)
                write_values = self.getEmployeeDocuments(checklist, 'param_name_2',employee_id)
                write_values_final.update(write_values)                   
                write_values = self.getEmployeeDocuments(checklist, 'param_name_3',employee_id)
                write_values_final.update(write_values)

                write_values = self.getEmployeeLicenses(checklist, 'param_name_1',employee_id)
                write_values_final.update(write_values)
                write_values = self.getEmployeeLicenses(checklist, 'param_name_2',employee_id)
                write_values_final.update(write_values)
                write_values = self.getEmployeeLicenses(checklist, 'param_name_3',employee_id)
                write_values_final.update(write_values)

                write_values = self.getEmployeeMedicalRecord(checklist, 'param_name_1',employee_id)
                write_values_final.update(write_values)
                write_values = self.getEmployeeMedicalRecord(checklist, 'param_name_2',employee_id)
                write_values_final.update(write_values)
                write_values = self.getEmployeeMedicalRecord(checklist, 'param_name_3',employee_id)
                write_values_final.update(write_values)                
                checklist.write(write_values_final)              

                #if not isinstance(checklist.param_name_1, bool):
                #    if len(checklist.param_name_1) > 0:
                        #Get Document Properties
                #        if checklist.param_name_1.link_selection == 'document':
                            #raise Warning(checklist.param_name_1.link_document_type.id)
                            #Check what Kind of Kind of Records will be retrieve e.g. Old or New Records
                            #model_employee_document_ret =  model_employee_document.search([('document', '=',checklist.param_name_1.link_document_type.id),
                            #                                                                ('date_issued' ,'<=', server_date),
                            #                                                                ('date_expiry' ,'>=', server_date)])
                #            model_employee_document_ret =  model_employee_document.search([('document', '=',checklist.param_name_1.link_document_type.id)])

                            #raise Warning(checklist.param_name_1.link_document_type.name)
                #            if checklist.param_name_1.retrieve_history_records == 'latest_doc':
                #                for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                #                    write_values.update({'param_name_1_value': document.document_number,
                #                                         'param_name_1_check': 1})
                #                    break
                #            elif checklist.param_name_1.retrieve_history_records == 'oldest_doc':
                #                int_counter_record = 0
                #                if len(model_employee_document_ret) > 1:
                #                     for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                #                        if int_counter_record >= 1:
                #                            write_values.update({'param_name_1_value': document.document_number,
                #                                                 'param_name_1_check': 1})
                #                            break         
                #                        int_counter_record +=1                          

                #if not isinstance(checklist.param_name_3, bool):
                #    if len(checklist.param_name_3) > 0:
                        #Get Document Properties
                #        if checklist.param_name_3.link_selection == 'document':
                            #Check what Kind of Kind of Records will be retrieve e.g. Old or New Records
                #            model_employee_document_ret =  model_employee_document.search([('document', '=',checklist.param_name_1.link_document_type.id)])

                #            if checklist.param_name_3.retrieve_history_records == 'latest_doc':

                #                for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                #                    write_values.update({'param_name_3_value': document.document_number,
                #                                         'param_name_3_check': 1})
                #                    break
                #            elif checklist.param_name_1.retrieve_history_records == 'oldest_doc':
                #                int_counter_record = 0
                #                if len(model_employee_document_ret) > 1:
                #                     for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                #                        if int_counter_record >= 1:
                #                            write_values.update({'param_name_3_value': document.document_number,
                #                                                 'param_name_3_check': 1})
                #                            break         
                #                        int_counter_record +=1     
              
class EmployeeChecklist_list(models.Model):
    _name = "hr.employee.checklist.documents.list.main"

    checklist_template_id = fields.Many2one('hr.checklist_template')
    employee_checklist_document = fields.Many2one('hr.employee.checklist.documents')       


    param_name_1 = fields.Many2one('hr.checklist', 'Parameter 1')
    param_name_2 = fields.Many2one('hr.checklist', 'Parameter 2')
    param_name_3 = fields.Many2one('hr.checklist', 'Parameter 3')
    param_name_4 = fields.Many2one('hr.checklist', 'Parameter 4')

    param_name_1_value = fields.Char("Parameter 1 value")
    param_name_2_value = fields.Char("Parameter 2 value")
    param_name_3_value = fields.Char("Parameter 3 value")
    param_name_4_value = fields.Char("Parameter 4 value")

    param_name_1_check = fields.Boolean("Parameter 1 Checked?")
    param_name_2_check = fields.Boolean("Parameter 2 Checked?")
    param_name_3_check = fields.Boolean("Parameter 3 Checked?")
    param_name_4_check = fields.Boolean("Parameter 4 Checked?")

    param_name_1_value_visible = fields.Boolean("Parameter 1 Value visible?")
    param_name_2_value_visible = fields.Boolean("Parameter 2 Value visible?")
    param_name_3_value_visible = fields.Boolean("Parameter 3 Value visible?")
    param_name_4_value_visible = fields.Boolean("Parameter 4 Value visible?")


    param_name_1_check_visible = fields.Boolean("Parameter 1 Check visible?")
    param_name_2_check_visible = fields.Boolean("Parameter 2 Check visible?")
    param_name_3_check_visible = fields.Boolean("Parameter 3 Check visible?")
    param_name_4_check_visible = fields.Boolean("Parameter 4 Check visible?")

    has_date_issued = fields.Boolean("Date Issued Enable?")
    has_issued_at = fields.Boolean("Issued At Enable?")
    has_date_expiry = fields.Boolean("Date Expiry Enable?")            
    has_changed_by = fields.Boolean("Change by Enable")            
    has_change_date = fields.Boolean("Date Change Enable?")            

    issued_at = fields.Char("Issued at")
    date_issued = fields.Date("Date issued")
    date_expiry = fields.Date("Date Expiry")
    change_by = fields.Char("Change By")
    change_date = fields.Char("Change Date")


    @api.model
    def getEmployeeDocuments_Temporary(self,pemployee_id):
        model_employee_document = self.env['hr.employee_documents'].search([('employee_doc_id', '=', pemployee_id.employee_checklist_document.employee_id.id)])

        if len(pemployee_id) > 0:
            #Get Document Properties
            model_employee_document_ret =  model_employee_document.search([('document', '=',pemployee_id.param_name_1.link_document_type.id),
                                                                          ('employee_doc_id', '=', pemployee_id.employee_checklist_document.employee_id.id)])
            if pemployee_id.param_name_1.retrieve_history_records == 'latest_doc':
                for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):

                    pemployee_id.param_name_1_value = document.document_number
                    pemployee_id.param_name_1_check = 1
                    #pemployee_id.write()
                    break


            model_employee_document_ret =  model_employee_document.search([('document', '=',pemployee_id.param_name_2.link_document_type.id),
                                                                           ('employee_doc_id', '=', pemployee_id.employee_checklist_document.employee_id.id)])
            if pemployee_id.param_name_2.retrieve_history_records == 'oldest_doc':
                int_counter_record = 0
                if len(model_employee_document_ret) > 1:
                     for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                        if int_counter_record >= 1:
                            pemployee_id.param_name_2_value = document.document_number
                            pemployee_id.param_name_2_check = 1
                            #pemployee_id.write()   
                            break   
                        int_counter_record +=1     

            model_employee_document_ret =  model_employee_document.search([('document', '=',pemployee_id.param_name_3.link_document_type.id),
                                                                            ('employee_doc_id', '=', pemployee_id.employee_checklist_document.employee_id.id)])
            if pemployee_id.param_name_3.retrieve_history_records == 'latest_doc':
                for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):

                    pemployee_id.param_name_3_value = document.place_ofissue
                    pemployee_id.param_name_3_check = 1
                    #pemployee_id.write()
                    break

            if pemployee_id.param_name_2.checklist_code  == 'CODE_US_VISA_EXPIRY_DATE_CONSTANT':
                date_exp = ''
                model_employee_document_ret =  model_employee_document.search([('document', '=',pemployee_id.param_name_2.link_document_type.id),
                                                                                ('employee_doc_id', '=', pemployee_id.employee_checklist_document.employee_id.id)])
                if pemployee_id.param_name_2.retrieve_history_records == 'latest_doc':
                    for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                        if not isinstance(pemployee_id.date_expiry, bool):
                            date_exp = datetime.datetime.strptime(pemployee_id.date_expiry ,"%Y-%m-%d")
                            pemployee_id.param_name_2_value = date_exp.strptime('%m/%d/%y')
                            pemployee_id.param_name_2_check = 1

                        break                



                              

    @api.model
    def getEmployeeMedicalRecord(self, pchecklist, pfield_name, pemployee_id):
        model_employee_medical = self.env['hr.employee_medical_records'].search([('employee_med_rec_id', '=', pemployee_id)])
        model_employee_medical_ret =  model_employee_medical.search([('medical_type', '=',pchecklist.param_name_1.link_medical_type.id)])
        if pfield_name == 'param_name_1':
            parameter_field = pchecklist.param_name_1
            str_parameter_value = 'param_name_1_value'
            str_parameter_check = 'param_name_1_check'
        elif pfield_name == 'param_name_2':
            parameter_field = pchecklist.param_name_2
            str_parameter_value = 'param_name_2_value'
            str_parameter_check = 'param_name_2_check'            
        elif pfield_name == 'param_name_3':
            parameter_field = pchecklist.param_name_3
            str_parameter_value = 'param_name_3_value'
            str_parameter_check = 'param_name_3_check'  

        write_values = {}
        if not isinstance(parameter_field, bool):
            if len(parameter_field) > 0:
                #Get Document Properties

                if parameter_field.link_selection == 'medical':
                    if parameter_field.retrieve_history_records == 'latest_doc':
                        for license  in model_employee_medical_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                            write_values.update({str_parameter_check: 1})
                            break
                    elif parameter_field.retrieve_history_records == 'oldest_doc':
                        int_counter_record = 0
                        if len(model_employee_medical_ret) > 1:
                             for license  in model_employee_medical_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                                if int_counter_record >= 1:
                                    write_values.update({str_parameter_check: 1})
                                    break         
                                int_counter_record +=1     
        return write_values  


    @api.model
    def getEmployeeLicenses(self, pchecklist, pfield_name, pemployee_id):
        model_employee_license = self.env['hr.employeelicenses'].search([('employee_licenses_id', '=', pemployee_id)])
        model_employee_license_ret =  model_employee_license.search([('license', '=',pchecklist.param_name_1.link_license_type.id)])
        if pfield_name == 'param_name_1':
            parameter_field = pchecklist.param_name_1
            str_parameter_value = 'param_name_1_value'
            str_parameter_check = 'param_name_1_check'
        elif pfield_name == 'param_name_2':
            parameter_field = pchecklist.param_name_2
            str_parameter_value = 'param_name_2_value'
            str_parameter_check = 'param_name_2_check'            
        elif pfield_name == 'param_name_3':
            parameter_field = pchecklist.param_name_3
            str_parameter_value = 'param_name_3_value'
            str_parameter_check = 'param_name_3_check'  


        write_values = {}
        if not isinstance(parameter_field, bool):
            if len(parameter_field) > 0:
                #Get Document Properties

                if parameter_field.link_selection == 'license':
                    if parameter_field.retrieve_history_records == 'latest_doc':
                        for license  in model_employee_license_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                            write_values.update({str_parameter_value: license.doc_number,
                                                 str_parameter_check: 1})
                            break
                    elif parameter_field.retrieve_history_records == 'oldest_doc':
                        int_counter_record = 0
                        if len(model_employee_license_ret) > 1:
                             for license  in model_employee_license_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                                if int_counter_record >= 1:
                                    write_values.update({str_parameter_value: license.doc_number,
                                                         str_parameter_check: 1})
                                    break         
                                int_counter_record +=1     
        return write_values               

    @api.model
    def getEmployeeDocuments(self, pchecklist, pfield_name, pemployee_id):
        model_employee_document = self.env['hr.employee_documents'].search([('employee_doc_id', '=', pemployee_id)])
        model_employee_document_ret =  model_employee_document.search([('document', '=',pchecklist.param_name_1.link_document_type.id)])

        if pfield_name == 'param_name_1':
            parameter_field = pchecklist.param_name_1
            str_parameter_value = 'param_name_1_value'
            str_parameter_check = 'param_name_1_check'
        elif pfield_name == 'param_name_2':
            parameter_field = pchecklist.param_name_2
            str_parameter_value = 'param_name_2_value'
            str_parameter_check = 'param_name_2_check'            
        elif pfield_name == 'param_name_3':
            parameter_field = pchecklist.param_name_3
            str_parameter_value = 'param_name_3_value'
            str_parameter_check = 'param_name_3_check'  

        write_values = {}
        if not isinstance(parameter_field, bool):
            if len(parameter_field) > 0:
                #Get Document Properties

                if parameter_field.link_selection == 'document':
                    model_employee_document_ret =  model_employee_document.search([('document', '=',parameter_field.link_document_type.id),

                                                                                    ])

                    #raise Warning(checklist.param_name_1.link_document_type.name)
                    if parameter_field.retrieve_history_records == 'latest_doc':
                        for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                            write_values.update({str_parameter_value: document.document_number,
                                                 str_parameter_check: 1})
                            break
                    elif parameter_field.retrieve_history_records == 'oldest_doc':
                        int_counter_record = 0
                        if len(model_employee_document_ret) > 1:
                             for document  in model_employee_document_ret.sorted(key=lambda r: r.date_expiry, reverse = True):
                                if int_counter_record >= 1:
                                    write_values.update({str_parameter_value: document.document_number,
                                                         str_parameter_check: 1})
                                    break         
                                int_counter_record +=1     
        return write_values               

    @api.model
    def getDataFromDocuments(self, pchecklist_document_id, employee_id):
        model_checklist_document_list = self.env[self._name].search([('employee_checklist_document', '=', pchecklist_document_id)])
        
        if len(model_checklist_document_list) > 0:

            server_date = datetime.datetime.strptime(DATE_NOW.strftime("%Y-%m-%d") ,"%Y-%m-%d")

            for checklist in model_checklist_document_list:
                write_values = {}
                write_values_final = {}    
                write_values = self.getEmployeeDocuments(checklist, 'param_name_1',employee_id)
                write_values_final.update(write_values)
                write_values = self.getEmployeeDocuments(checklist, 'param_name_2',employee_id)
                write_values_final.update(write_values)                   
                write_values = self.getEmployeeDocuments(checklist, 'param_name_3',employee_id)
                write_values_final.update(write_values)

                write_values = self.getEmployeeLicenses(checklist, 'param_name_1',employee_id)
                write_values_final.update(write_values)
                write_values = self.getEmployeeLicenses(checklist, 'param_name_2',employee_id)
                write_values_final.update(write_values)
                write_values = self.getEmployeeLicenses(checklist, 'param_name_3',employee_id)
                write_values_final.update(write_values)

                write_values = self.getEmployeeMedicalRecord(checklist, 'param_name_1',employee_id)
                write_values_final.update(write_values)
                write_values = self.getEmployeeMedicalRecord(checklist, 'param_name_2',employee_id)
                write_values_final.update(write_values)
                write_values = self.getEmployeeMedicalRecord(checklist, 'param_name_3',employee_id)
                write_values_final.update(write_values)                
                checklist.write(write_values_final) 
