# -*- coding: utf-8 -*-
from odoo import models,fields,api
from odoo import tools
# from openerp.report import report_sxw
# from .. import hr_parameter_model
# from .. import hr_recruitment_seabased
import datetime
import base64
from odoo.exceptions import except_orm, Warning, RedirectWarning,ValidationError


#FOR EXCEL FILE
import xlwt
from io import StringIO
from io import BytesIO

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


#COLUMNS FOR SORTING

WITH_REMARKS_COLUMNS = [
('employee_number','Employee Number'),
('ccl_number','CCL Number'),
('employment_dept_code','Ship Department'),
('employment_rank','Rank'),
('last_name','Last Name'),
('first_name','First Name'),
('birth_date','Birth Date'),
('employment_status','Status'),
('date_servicefrom','Service from'),
('date_serviceto','Service to'),
('remarks','Remarks'),
#('total_years_of_service','Total Years Service'),
]


WITH_REMARKS_COLUMNS_RELATIVE = [
('employee_number','Employee Number'),
('ccl_number','CCL Number'),
('employment_dept_code','Ship Department'),
('employment_rank','Rank'),
('last_name','Last Name'),
('first_name','First Name'),
('birth_date','Birth Date'),
('employment_status','Status'),
('date_servicefrom','Service from'),
('date_serviceto','Service to'),
#('total_years_of_service','Total Years Service'),
]



DISEMBARKATION = [
('employee_number','Employee Number'),
('ccl_number','CCL Number'),
('last_name','Last Name'),
('first_name','First Name'),
('employment_dept_code','Ship Department'),
('employment_rank','Rank'),
('placeof_birth','Place of Birth'),
('country_id','Nationality'),
('gender','Gender'),
('date_depart','Depart Date'),
('date_servicefrom','Sign On Date'),
('date_serviceto','Sign Off Date'),
('place_signoff','Place signoff'),
]


EMBARKATION = [
('employee_number','Employee Number'),
('ccl_number','CCL Number'),
('last_name','Last Name'),
('first_name','First Name'),
('employment_dept_code','Ship Department'),
('employment_rank','Rank'),
('placeof_birth','Place of Birth'),
('country_id','Nationality'),
('gender','Gender'),
('date_depart','Depart Date'),
('date_servicefrom','Sign On Date'),
('date_serviceto','Sign Off Date'),
('place_signoff','Place signoff'),]


SIGNONSIGNOFF = [
('employee_number','Employee Number'),
('ccl_number','CCL Number'),
('employment_rank','Rank'),
('last_name','Last Name'),
('first_name','First Name'),
('birth_date','Birth Date'),
('employment_status','Status'),
('date_servicefrom','Service from'),
('date_serviceto','Service to'),
('object_code','Vessel'),
('remarks','Remarks'),
]


SORTING_TYPE = [
('asc','Ascending'), 
('desc','Descending'),
]


SQL_QUERY = " SELECT (DOCUMENT_NUMBER::CHAR(120)), (DATE_ISSUED::DATE), (DATE_EXPIRY::DATE) FROM HR_EMPLOYEE_DOCUMENTS" \
            " WHERE ('%(my_date)s'::date) BETWEEN DATE_ISSUED and DATE_EXPIRY" \
            " AND EMPLOYEE_DOC_ID = %(employee_id)d" \
            " AND DOCUMENT = (SELECT ID FROM hr_documenttype WHERE ABBREVIATION = '%(my_abbrv)s')" \
            " ORDER BY DATE_EXPIRY DESC" \
            " LIMIT 1"

SQL_QUERY_EMPLOYMENT_HISTORY =  " SELECT OBJECT_CODE FROM HR_EMPLOYMENTHISTORY"\
                                " WHERE ('%(my_date)s'::date) BETWEEN DATE_SERVICEFROM AND DATE_SERVICETO"\
                                " AND EMPLOYMENT_STATUS = (SELECT ID FROM HR_EMPLOYMENT_STATUS WHERE STATUS_ID = '%(statusid)s')"\
                                " AND EMPLOYEE_EMPLOYMENT_ID = %(employee_id)d"\
                                " ORDER BY DATE_SERVICETO DESC"\
                                " LIMIT 1"

#--------------------- UI VIEW/MENUS/FORM


# ----- MAIN VIEW FORM
#--- Personnel Active on Board
class hrPersonnelActiveOnBoardwithRemarksMenu(models.Model):
    _name = 'hr.personnel.withrmks.menu'    
    _description = 'Crew List Active on Board'    

    vessel = fields.Many2one('hr.vessel','Vessel')
    date_search = fields.Date('Date')
    employment_status = fields.Many2one('hr.employment.status', 'Employment Status')

    sort_by = fields.Selection(WITH_REMARKS_COLUMNS, 'Sorted by')
    sorting_type = fields.Selection(SORTING_TYPE, 'Sorted Type', default= SORTING_TYPE[0][0])
    is_with_remarks = fields.Boolean('With Remarks', default = False)    
    #sorting_by = fields.Selection([('rank', 'Rank'), 
    #                               ('last_name', 'Last Name'),
    #                               ('first_name', 'First Name'),
    #                               ('Middle', 'Last Name')], string ='Report Type', default = 'signon', required=True)


    def unlinkRecords(self):
        model_person_tree = self.env['hr.personnel.withrmks.main'].search([('create_uid', '=', self._uid)])
        model_person_tree.unlink()                
        model_person_tree = self.env['hr.personnel.withrmks.tree'].search([('create_uid', '=', self._uid)])
        model_person_tree.unlink()     


    @api.onchange('vessel')
    def _onchangevessel(self):
        self.unlinkRecords()

    @api.onchange('sort_by', 'sorting_type')   
    def _onchangesort_by(self):
        self.unlinkRecords()


    # @api.one
    def genReport(self):
        report = self.env['report'].get_pdf(records = self,report_name = "bahia_personnel_management.report_personnel_active_on_board_w_remarks"), 'pdf'
        return self.env['report'].get_action('bahia_personnel_management.report_personnel_active_on_board_w_remarks')


    def GenerateReport(self):
        #raise Warning(context)
        context = {}
        employee = self.env["hr.personnel.withrmks.menu"].browse(self.id)  
        #sraise Warning(employee.vessel)   
        partial_id = self.env["hr.personnel.withrmks.main"].create({
            # 'attendance_detail_id': 1,
            'vessel': employee.vessel.id,
            'date_search' : employee.date_search,
            'employment_status' : employee.employment_status.id,
            'sort_by': employee.sort_by,
            'sorting_type': employee.sorting_type,
            'is_with_remarks': employee.is_with_remarks,
            })

        x = self.env["hr.personnel.withrmks.main"].createReport({'id_main': partial_id.id,})

        

        return {
            'name': "Crew List Active on Board",
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'hr.personnel.withrmks.main',
            'res_id': partial_id.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'domain': '[]',
            'context': context
        }   

#--- Disembarkation Report
class hrDisembarkationReportMenu(models.Model):
    _name = 'hr.disembarkation.menu'
    _description = 'Disembarkation Report'

    vessel = fields.Many2one('hr.vessel','Vessel', required =True)
    date_search = fields.Date('Date')

    sort_by = fields.Selection(DISEMBARKATION, 'Sorted by')
    sorting_type = fields.Selection(SORTING_TYPE, 'Sorted Type', default= SORTING_TYPE[0][0])    


    @api.onchange('vessel', 'sort_by', 'sorting_type')
    def _onchangevessel(self):
        model_person_tree = self.env['hr.disembarkation.main'].search([('create_uid', '=', self._uid)])
        model_person_tree.unlink()                
        model_person_tree = self.env['hr.disembarkation.tree'].search([('create_uid', '=', self._uid)])
        model_person_tree.unlink()        


    def GenerateReport(self):
        context = {}
        employee = self.env["hr.disembarkation.menu"].browse(self.id)  
        #sraise Warning(employee.vessel)   
        partial_id = self.env["hr.disembarkation.main"].create({
            # 'attendance_detail_id': 1,
            'vessel': employee.vessel.id,
            'date_search' : employee.date_search,
            'sort_by': employee.sort_by,
            'sorting_type': employee.sorting_type,                        
        })

        x = self.env["hr.disembarkation.main"].createReport({'id_main': partial_id.id,})

        
        return {
            'name': "Disembarkation Report",
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'hr.disembarkation.main',
            'res_id': partial_id.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current', #current
            'domain': '[]',
            'context': context
        }                

#--- Embarkation Report
class hrEmbarkationReportMenu(models.Model):
    _name = 'hr.embarkation.menu'
    _description = 'Embarkation Report'

    vessel = fields.Many2one('hr.vessel','Vessel', required =True)
    date_search = fields.Date('Date')

    sort_by = fields.Selection(EMBARKATION, 'Sorted by')
    sorting_type = fields.Selection(SORTING_TYPE, 'Sorted Type', default= SORTING_TYPE[0][0])        

    @api.onchange('vessel','sort_by', 'sorting_type')
    def _onchangevessel(self):
        model_person_tree = self.env['hr.embarkation.main'].search([('create_uid', '=', self._uid)])
        model_person_tree.unlink()                
        model_person_tree = self.env['hr.embarkation.tree'].search([('create_uid', '=', self._uid)])
        model_person_tree.unlink()        


    def GenerateReport(self):
        context = {}
        employee = self.env["hr.embarkation.menu"].browse(self.id)  
        #sraise Warning(employee.vessel)   
        partial_id = self.env["hr.embarkation.main"].create({
            # 'attendance_detail_id': 1,
            'vessel': employee.vessel.id,
            'date_search' : employee.date_search,
            'sort_by': employee.sort_by,
            'sorting_type': employee.sorting_type,                           
        })

        x = self.env["hr.embarkation.main"].createReport({'id_main': partial_id.id,})

        

        return {
            'name': "Embarkation Report",
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'hr.embarkation.main',
            'res_id': partial_id.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current', #current
            'domain': '[]',
            'context': context
        }                        

#--- SignOn Report
class hrsignonoffReportMenu(models.Model):
    _name = 'hr.signonoff.report.menu'
    _description = 'SignOn Report'

    signonoff_selection = fields.Selection([('signon', 'Sign On'), ('signoff', 'Sign Off')], string ='Report Type', default = 'signon', required=True)
    vessel = fields.Many2one('hr.vessel','Vessel', required =True)
    date_from_search = fields.Date('Date From')
    date_to_search = fields.Date('Date to')
    employment_status = fields.Many2one('hr.employment.status', 'Employment Status')
    sort_by = fields.Selection(SIGNONSIGNOFF, 'Sorted by')
    sorting_type = fields.Selection(SORTING_TYPE, 'Sorted Type', default= SORTING_TYPE[0][0])
    is_with_remarks = fields.Boolean('With Remarks', default = False)

    @api.onchange('vessel', 'sort_by', 'sorting_type')
    def _onchangevessel(self):
        model_person_tree = self.env['hr.signonoff.report.main'].search([('create_uid', '=', self._uid)])
        model_person_tree.unlink()                
        model_person_tree = self.env['hr.signonoff.report.tree'].search([('create_uid', '=', self._uid)])
        model_person_tree.unlink()        


    def GenerateReport(self):

        context = {}
        employee = self.env["hr.signonoff.report.menu"].browse(self.id)  


        partial_id = self.env["hr.signonoff.report.main"].create({
            # 'attendance_detail_id': 1,
            'vessel': employee.vessel.id,
            'date_from_search' : employee.date_from_search,
            'date_to_search' : employee.date_to_search,
            'signonoff_selection' : employee.signonoff_selection,
            'employment_status' : employee.employment_status.id,
            'sort_by': employee.sort_by,
            'sorting_type': employee.sorting_type,
			'is_with_remarks': employee.is_with_remarks,
        })

        x = self.env["hr.signonoff.report.main"].createReport({'id_main': partial_id.id,})

        str_view_name = 'Sign Off Report'
        if employee.signonoff_selection == "signon":
            str_view_name = 'Sign On Report'

        return {
            'name': str_view_name,
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'hr.signonoff.report.main',
            'res_id': partial_id.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current', #current
            'domain': '[]',
            'context': context
        }                                

#--- Personnel Active on Board With Relative
class hrPersonnelActiveOnBoardwithRelativeMenu(models.Model):
    _name = 'hr.personnel.withrelative.menu'
    _description = 'Personnel Active on Board With Relative'

    vessel = fields.Many2one('hr.vessel','Vessel')
    date_search = fields.Date('Date')
    employment_status = fields.Many2one('hr.employment.status', 'Employment Status')
    sort_by = fields.Selection(WITH_REMARKS_COLUMNS, 'Sorted by')
    sorting_type = fields.Selection(SORTING_TYPE, 'Sorted Type', default= SORTING_TYPE[0][0])   
    is_with_remarks = fields.Boolean('With Remarks', default = False) 

    @api.onchange('vessel', 'sort_by', 'sorting_type')
    def _onchangevessel(self):
        model_person_tree = self.env['hr.personnel.withrelative.main'].search([('create_uid', '=', self._uid)])
        model_person_tree.unlink()                
        model_person_tree = self.env['hr.personnel.withrelative.tree'].search([('create_uid', '=', self._uid)])
        model_person_tree.unlink()        

    # # @api.one
    def genReport(self):
        report = self.env['report'].get_pdf(records = self,report_name = "bahia_personnel_management.report_personnel_active_on_board_w_remarks"), 'pdf'
        return self.env['report'].get_action('bahia_personnel_management.report_personnel_active_on_board_w_remarks')


    def GenerateReport(self):
        #raise Warning(context)
        context = {}
        employee = self.env["hr.personnel.withrelative.menu"].browse(self.id)  
        #sraise Warning(employee.vessel)   
        partial_id = self.env["hr.personnel.withrelative.main"].create({
            'vessel': employee.vessel.id,
           'date_search' : employee.date_search,
           'employment_status' : employee.employment_status.id,
           'sort_by': employee.sort_by,
           'sorting_type': employee.sorting_type,       
           'is_with_remarks': employee.is_with_remarks,                    
        })

        x = self.env["hr.personnel.withrelative.main"].createReport({'id_main': partial_id.id,})

        
        #new
        return {
            'name': "Crew List Active on Board w/ Relatives",
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'hr.personnel.withrelative.main',
            'res_id': partial_id.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'domain': '[]',
            'context': context
        }   

# ----- MAIN WIZARD FORM
#--- Personnel Active on Board
class hrPersonnelActiveOnBoardwithRemarksMenuMainView(models.Model):
    _name = 'hr.personnel.withrmks.main'
    _description = 'Crew List Active on Board'


    def _getExcelFilename(self):
            self.excel_filename = 'Crew List Active on Board.xls'     

    def _getPDFfilename(self):
            self.pdf_filename = 'Crew List Active on Board.pdf'   

    name = fields.Char('Name')
    vessel = fields.Many2one('hr.vessel','Vessel')
    date_search = fields.Date('Date')
    excel_filename = fields.Char('file name', readonly = True,store = False,compute ='_getExcelFilename')
    excel_document = fields.Binary('Excel Report')
    pdf_filename = fields.Char('file name', readonly = True,store = False,compute ='_getPDFfilename')
    pdf_document = fields.Binary('PDF Report')    
    personnel_actived_on_board = fields.One2many('hr.personnel.withrmks.tree','active_id', readonly=False,copy=False)
    employment_status = fields.Many2one('hr.employment.status', 'Employment Status')
    sort_by = fields.Selection(WITH_REMARKS_COLUMNS, 'Sorted by')
    sorting_type = fields.Selection(SORTING_TYPE, 'Sorted Type', default= SORTING_TYPE[0][0])
    is_with_remarks = fields.Boolean('With Remarks', default = False)

    def getTotalYearsService(self, main_id, main_model):

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

        #DETAILS
        tree_model = self.env['hr.personnel.withrmks.tree'].search([('active_id','=',main_id)])
        for employment_history in tree_model:
            str_service_range = employment_history.total_years_of_service
            str_service_range = str_service_range.split()
            if employment_history.employment_status.status_id == 'ACT':
                int_year = int(float(str_service_range[0].replace('Y','')))
                int_month = int(float(str_service_range[1].replace('M','')))
                int_day = int(float(str_service_range[2].replace('D','')))
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
        return  str(int_final_year) + 'Y ' + str(int_final_month) + 'M ' +  str(int_final_day).split('.')[0]  + 'D'


    def getTotalNumberOfRecords(self, main_id, main_model):
        intTotal = 0
        intTotal = self.env['hr.personnel.withrmks.tree'].search_count([('active_id','=',main_id)])
        return intTotal

    def genReport(self):
        return self.env.ref('ibas_bahia.action_report_personnel_active_on_board_with_remarks').report_action(self)

    @api.model
    def createReport(self, id_main  = 0):
        #raise Warning(id_main['id_main'])
        main_model = self.env[self._name].search([('id', '=', id_main['id_main'])])
        tree_model = self.env['hr.personnel.withrmks.tree']
        name_val  = 'Crewlist_active_on_board_' + str(self._uid) 
        main_model.update({'name':name_val})
        QUERY = "Select * from hr_personnel_withremrks_report"
        QUERY_AND = ' and '
        QUERY_WHERE = ' where '


        if len(main_model) > 0:

            #if  isinstance(main_model.date_search, bool):
            #    if QUERY.find('where') > 0:
            #       QUERY +=  "where ('%(date)s'::DATE) BETWEEN date_servicefrom and date_serviceto"
            #    else:
            #       QUERY +=  "and ('%(date)s'::DATE) BETWEEN date_servicefrom and date_serviceto" 
            #    QUERY %{'date': main_model.date_search}


            if not isinstance(main_model.vessel.id, bool) and len(str(main_model.vessel.id)) > 0:
                QUERY += " where object_code = %(vessel)d" %{'vessel': main_model.vessel.id}                

            if  not isinstance(main_model.date_search, bool) and len(str(main_model.date_search)) > 0:
                if QUERY.find('where') > 0:
                    QUERY += " and ('%(date)s'::DATE) BETWEEN date_servicefrom and COALESCE(date_serviceto,date_servicefrom)"
                else:
                    QUERY += " where ('%(date)s'::DATE) BETWEEN date_servicefrom and COALESCE(date_serviceto,date_servicefrom)"

                QUERY  = QUERY %{'date': main_model.date_search}


            if not isinstance(main_model.employment_status, bool) and len(main_model.employment_status) > 0:
                if QUERY.find('where') > 0:
                    QUERY += " and employment_status = %(employment_status_id)d" 
                else:
                    QUERY += " where employment_status = %(employment_status_id)d"
                QUERY = QUERY %{'employment_status_id': main_model.employment_status.id}


            #if  isinstance(main_model.date_search, bool):
            #    QUERY = "Select * from hr_personnel_withremrks_report where" \
            #            " object_code = %(vessel)d" %{'vessel': main_model.vessel.id}                
            #elif len(main_model.date_search) > 0:
            #    QUERY = "Select * from hr_personnel_withremrks_report where ('%(date)s'::DATE) BETWEEN date_servicefrom and date_serviceto" \
            #            " and object_code = %(vessel)d" %{'date': main_model.date_search, 'vessel': main_model.vessel.id}
            #else:
            #    QUERY = "Select * from hr_personnel_withremrks_report where" \
            #            " object_code = %(vessel)d" %{'vessel': main_model.vessel.id}

            #if not isinstance(main_model.employment_status, bool) and len(main_model.employment_status) > 0:
            #    QUERY += " and employment_status = %(employment_status_id)d" %{'employment_status_id': main_model.employment_status.id}

            if main_model.is_with_remarks:
                QUERY += "  and (remarks is not null and length(trim(remarks)) > 0)"
                
            if not isinstance(main_model.sort_by, bool) and len(main_model.sort_by) > 0:
                QUERY += " ORDER BY %(sort_by)s" %{'sort_by': main_model.sort_by}

                if not isinstance(main_model.sorting_type, bool) and len(main_model.sorting_type) > 0: 
                    QUERY += " %(sorting_type)s" %{'sorting_type': main_model.sorting_type}
                    



            #raise Warning(QUERY)

            #TO EXECUTE SQL QUERY
            self.env.cr.execute(QUERY)
            for fetch in self.env.cr.fetchall():

                tree_model.create({
                    'active_id': id_main['id_main'],
                    'employee_number' : fetch[1],
                    'ccl_number' : fetch[2],
                    'employment_rank'  : fetch[3],
                    'last_name'  : fetch[4],
                    'first_name'  : fetch[5],
                    'birth_date'  : fetch[6],
                    'employment_status'  : fetch[7],
                    'date_servicefrom'  : fetch[8],
                    'date_serviceto'  : fetch[9],
                    'remarks'  : fetch[10],
                    'employment_dept_code'  : fetch[11],
                    'object_code'  : fetch[12],
                    'employee_id':   fetch[13],                    
                    })   
            #Create Now an Excel File
            self.createExcelFile(id_main['id_main'],main_model)

    @api.model
    def createExcelFile(self, main_id, main_model):
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
        sheet = workbook.add_sheet("Crewlist Report")
        intRow = 0
        #REPORT TITLE
        sheet.write_merge(intRow,intRow+1, 0,10, "CREWLIST REPORT", styleHeader)  
        intRow +=2
        #HEADER
        sheet.write(intRow, 0, "Vessel:")
        sheet.write(intRow, 1, main_model.vessel.name)       
        intRow +=1
        if not isinstance(main_model.date_search, bool):
            sheet.write(intRow, 0, "Date:")
            sheet.write(intRow, 1, main_model.date_search)
        else:
            sheet.write(intRow, 0, "Date:")
            sheet.write(intRow, 1, "All Date")                   
        intRow +=2          
       
        #COLUMNS
        sheet.write(intRow, 0,"Employee Number",styleColumns)
        sheet.write(intRow, 1, "CCL Number",styleColumns)
        sheet.write(intRow, 2, "Department",styleColumns)
        sheet.write(intRow, 3, "Rank",styleColumns)
        sheet.write(intRow, 4, "Last Name",styleColumns)
        sheet.write(intRow, 5, "First Name",styleColumns)
        sheet.write(intRow, 6, "Birth Date",styleColumns)
        sheet.write(intRow, 7, "Status",styleColumns)
        sheet.write(intRow, 8, "Service from",styleColumns)
        sheet.write(intRow, 9, "Service to",styleColumns)
        sheet.write_merge(intRow,intRow, 10,11, "Remarks",styleColumns)
        sheet.write(intRow, 12, "Total Years of Service",styleColumns)
        intRow +=1

        #DETAILS
        tree_model = self.env['hr.personnel.withrmks.tree'].search([('active_id','=',main_id)])
        for detail in tree_model:
            #str_empnumber = str(detail.employee_number)
            str_empnumber = str(detail.employee_contractNumber)            
            sheet.write(intRow, 0, str_empnumber.zfill(10),styleColumns)
            if isinstance(detail.ccl_number, bool):
                sheet.write(intRow, 1, "",styleColumns)
            else:
                sheet.write(intRow, 1, detail.ccl_number,styleColumns)

            sheet.write(intRow, 2, detail.employment_dept_code.name,styleColumns)
            sheet.write(intRow, 3, detail.employment_rank.name,styleColumns)        
            sheet.write(intRow, 4, detail.last_name,styleColumns)
            sheet.write(intRow, 5, detail.first_name,styleColumns)
            sheet.write(intRow, 6, detail.birth_date,styleColumns)
            sheet.write(intRow, 7, detail.employment_status.name,styleColumns)
            sheet.write(intRow, 8, detail.date_servicefrom,styleColumns)
            sheet.write(intRow, 9, detail.date_serviceto,styleColumns)
            sheet.write_merge(intRow,intRow, 10,11, detail.remarks,styleColumns)
            sheet.write(intRow,12, detail.total_years_of_service,styleColumns)
            intRow +=1

        sheet.write_merge(intRow+1,intRow+1, 10,11, "Total Record/s")    
        sheet.write(intRow+1, 12, self.getTotalNumberOfRecords(main_id,main_model),styleColumns)            

        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data_read = fp.read()
        fp.close()
        byte_arr = base64.b64encode(data_read)
        main_model.write({'excel_document':byte_arr})
        #self.excel_document = byte_arr

class hrPersonnelActiveOnBoardwithRemarksMenuTreeView(models.Model):
    _name = 'hr.personnel.withrmks.tree'
    _description = 'Personnel Active On Board With Remarks'

    active_id = fields.Many2one('hr.personnel.withrmks.main', 'Employee')
    employee_number = fields.Char("Employee Number", readonly=True)
    ccl_number = fields.Char("CCL Number", readonly=True)
    employment_rank = fields.Many2one("hr.rank", readonly=True, string="Rank")
    last_name = fields.Char("Last Name", readonly=True)
    first_name = fields.Char("First Name", readonly=True)
    birth_date = fields.Date("Birth Date", readonly=True)
    employment_status = fields.Many2one("hr.employment.status", readonly=True, string="Status")
    date_servicefrom = fields.Date("Service from", readonly=True)
    date_serviceto = fields.Date("Service to", readonly=True)
    remarks = fields.Char("Remarks", readonly=True)
    employment_dept_code = fields.Many2one("hr.ship.department", readonly=True, string="Ship Department")
    object_code = fields.Many2one("hr.vessel", readonly=True, string="Vessel")
    total_years_of_service = fields.Char('Service Length',store = False,compute ='getYearMonthDay')
    employee_id = fields.Many2one("hr.employee", readonly=True, string="Employee ID")
    employee_contractNumber =  fields.Char("Employee Number", readonly=True, compute ='getContractNumber')


    def getYearMonthDay(self):
        for record in self:
            record.total_years_of_service = record.employee_id.total_years_of_service  

    def getContractNumber(self):
        for record in self:
            record.employee_contractNumber = record.employee_id.employee_contract_number   

#--- Disembarkation Report
class hrDisembarkationMenuMainView(models.Model):
    _name = 'hr.disembarkation.main'
    _description = 'Disembarkation Report Main View'

    def _getExcelFilename(self):
            self.excel_filename = 'Disembarkation.xls'     

    def _getPDFfilename(self):
            self.pdf_filename = 'Disembarkation.pdf'   

    name = fields.Char('Name')
    vessel = fields.Many2one('hr.vessel','Vessel', required =True)
    date_search = fields.Date('Date')
    excel_filename = fields.Char('file name', readonly = True,store = False,compute ='_getExcelFilename')
    excel_document = fields.Binary('Excel Report')
    pdf_filename = fields.Char('file name', readonly = True,store = False,compute ='_getPDFfilename')
    pdf_document = fields.Binary('PDF Report')    
    detail_id = fields.One2many('hr.disembarkation.tree','active_id', readonly=False,copy=False)
    sort_by = fields.Selection(DISEMBARKATION, 'Sorted by')
    sorting_type = fields.Selection(SORTING_TYPE, 'Sorted Type', default= SORTING_TYPE[0][0])        

    def genReport(self):
        return self.env.ref('ibas_bahia.action_report_disembarkation').report_action(self)

    @api.model
    def createReport(self, id_main  = 0):
        main_model = self.env[self._name].search([('id', '=', id_main['id_main'])])
        tree_model = self.env['hr.disembarkation.tree']

        name_val  = 'Disembarkation_Report_' + str(self._uid) 
        main_model.update({'name':name_val})
        if len(main_model) > 0:
            if  isinstance(main_model.date_search, bool):
                QUERY = "Select * from hr_disembarkation_report where" \
                        " object_code = %(vessel)d" %{'vessel': main_model.vessel.id}                
            elif len(str(main_model.date_search)) > 0:
                #QUERY = "Select * from hr_disembarkation_report where ('%(date)s'::DATE) BETWEEN date_servicefrom and date_serviceto" \
                #        " and object_code = %(vessel)d" %{'date': main_model.date_search, 'vessel': main_model.vessel.id}
                QUERY = "Select * from hr_disembarkation_report where ('%(date)s'::DATE) = date_serviceto" \
                        " and object_code = %(vessel)d" %{'date': main_model.date_search, 'vessel': main_model.vessel.id}                
            else:
                QUERY = "Select * from hr_disembarkation_report where" \
                        " object_code = %(vessel)d" %{'vessel': main_model.vessel.id}


            if not isinstance(main_model.sort_by, bool) and len(main_model.sort_by) > 0:
                QUERY += " ORDER BY %(sort_by)s" %{'sort_by': main_model.sort_by}

                if not isinstance(main_model.sorting_type, bool) and len(main_model.sorting_type) > 0: 
                    QUERY += " %(sorting_type)s" %{'sorting_type': main_model.sorting_type}                        

            #TO EXECUTE SQL QUERY
            self.env.cr.execute(QUERY)
            for fetch in self.env.cr.fetchall():

                tree_model.create({
                    'active_id': id_main['id_main'],
                    'employee_number' : fetch[1],
                    'ccl_number' : fetch[2],
                    'last_name'  : fetch[3],
                    'first_name'  : fetch[4],                    
                    'employment_rank'  : fetch[5],
                    'country_id'  : fetch[6],
                    'gender'  : fetch[7],
                    'placeof_birth'  : fetch[8],
                    'passport'  : fetch[9],
                    'passport_date_issued'  : fetch[10],
                    'passport_date_expiry'  : fetch[11],
                    'ssrib'  : fetch[12],
                    'ssrib_date_issued'  : fetch[13],
                    'ssrib_date_expiry'  : fetch[14],
                    'place_signoff'  : fetch[15],
                    'date_depart'  : fetch[16],
                    'date_servicefrom'  : fetch[17],
                    'date_serviceto'  : fetch[18],
                    'employment_dept_code'  : fetch[19],
                    'object_code'  : fetch[20],                                                                                                    
                    'employee_id'  : fetch[21],                     
                    })   
            #Create Now an Excel File
            self.createExcelFile(id_main['id_main'],main_model)


    def getTotalNumberOfRecords(self, main_id, main_model):
        intTotal = 0
        intTotal = self.env['hr.disembarkation.tree'].search_count([('active_id','=',main_id)])
        return intTotal

    @api.model
    def createExcelFile(self, main_id, main_model):
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
        sheet.write_merge(intRow,intRow+1, 0,17, "DISEMBARKATION REPORT", styleHeader)  
        intRow +=2
        #HEADER
        sheet.write(intRow, 0, "Vessel:")
        sheet.write(intRow, 1, main_model.vessel.name)       
        intRow +=1
        if not isinstance(main_model.date_search, bool):
            sheet.write(intRow, 0, "Date:")
            sheet.write(intRow, 1, main_model.date_search)
        else:
            sheet.write(intRow, 0, "Date:")
            sheet.write(intRow, 1, "All Date")                   
        intRow +=2          
       
        #COLUMNS


        sheet.write(intRow, 0,"Employee Number",styleColumns)
        sheet.write(intRow, 1, "CCL Number",styleColumns)
        sheet.write(intRow, 2, "Last Name",styleColumns)
        sheet.write(intRow, 3, "First Name",styleColumns)        
        sheet.write(intRow, 4, "Department",styleColumns)
        sheet.write(intRow, 5, "Rank",styleColumns)
        sheet.write(intRow, 6, "place of Birth",styleColumns)
        sheet.write(intRow, 7, "Nationality",styleColumns)
        sheet.write(intRow, 8, "Gender",styleColumns)
        sheet.write(intRow, 9, "Passport",styleColumns)
        sheet.write(intRow, 10,"Date Issued",styleColumns)
        sheet.write(intRow, 11, "Date Expiry",styleColumns)
        sheet.write(intRow, 12, "SSIRB",styleColumns)
        sheet.write(intRow, 13, "Date Issued",styleColumns)
        sheet.write(intRow, 14, "Date Expiry",styleColumns)
       
        sheet.write(intRow, 15, "Depart Date",styleColumns)
        sheet.write(intRow, 16, "Sign On Date",styleColumns)
        sheet.write(intRow, 17, "Sign Off Date",styleColumns)        
        sheet.write(intRow, 18, "Place Signoff",styleColumns)
        intRow +=1


        #DETAILS
        tree_model = self.env['hr.disembarkation.tree'].search([('active_id','=',main_id)])
        for detail in tree_model:
            #str_empnumber = str(detail.employee_number)
            str_empnumber = str(detail.employee_contractNumber)
            sheet.write(intRow, 0, str_empnumber.zfill(10),styleColumns)
            if isinstance(detail.ccl_number, bool):
                sheet.write(intRow, 1, "",styleColumns)
            else:
                sheet.write(intRow, 1, detail.ccl_number,styleColumns)
            sheet.write(intRow, 2, detail.last_name,styleColumns)
            sheet.write(intRow, 3, detail.first_name,styleColumns)

            
            sheet.write(intRow, 4, detail.employment_dept_code.name,styleColumns)
            sheet.write(intRow, 5, detail.employment_rank.name,styleColumns)

            if isinstance(detail.placeof_birth, bool):
                sheet.write(intRow, 6, "",styleColumns)
            else:
                sheet.write(intRow, 6, detail.placeof_birth,styleColumns)

            sheet.write(intRow, 7, detail.country_id.name,styleColumns)
            sheet.write(intRow, 8, detail.gender,styleColumns)

            if isinstance(detail.passport, bool):
                sheet.write(intRow, 9, "",styleColumns)
            else:
                sheet.write(intRow, 9, detail.passport,styleColumns)

            if isinstance(detail.passport_date_expiry, bool):
                sheet.write(intRow, 10, "",styleColumns)
            else:
                sheet.write(intRow, 10, detail.passport_date_expiry,styleColumns)

            if isinstance(detail.passport_date_expiry, bool):
                sheet.write(intRow, 11, "",styleColumns)
            else:
                sheet.write(intRow, 11, detail.passport_date_expiry,styleColumns)

            #sheet.write(intRow, 9, detail.passport_date_issued,styleColumns)
            #sheet.write(intRow, 10, detail.passport_date_expiry ,styleColumns)

            if isinstance(detail.ssrib, bool):
                sheet.write(intRow, 12, "",styleColumns)
            else:
                sheet.write(intRow, 12, detail.ssrib,styleColumns)

            if isinstance(detail.ssrib_date_issued, bool):
                sheet.write(intRow, 13, "",styleColumns)
            else:
                sheet.write(intRow, 13, detail.ssrib_date_issued,styleColumns)

            if isinstance(detail.ssrib_date_expiry, bool):
                sheet.write(intRow, 14, "",styleColumns)
            else:
                sheet.write(intRow, 14, detail.ssrib_date_expiry,styleColumns)


            #sheet.write(intRow, 11, detail.ssrib,styleColumns)
            #sheet.write(intRow, 12, detail.ssrib_date_issued,styleColumns)
            #sheet.write(intRow, 13, detail.ssrib_date_expiry,styleColumns)
            if isinstance(detail.date_depart, bool):
                sheet.write(intRow, 15, "",styleColumns)
            else:
                sheet.write(intRow, 15, detail.date_depart,styleColumns)

            #sheet.write(intRow, 14, detail.date_depart,styleColumns)
            sheet.write(intRow, 16, detail.date_servicefrom,styleColumns)
            sheet.write(intRow, 17, detail.date_serviceto,styleColumns) 
            self.returnRowValue(detail.place_signoff.name, sheet, intRow, 18, styleColumns)       
            #sheet.write(intRow, 17, detail.place_signoff.name,styleColumns)

            intRow +=1

        sheet.write_merge(intRow+1,intRow+1, 16,17, "Total Record/s")    
        sheet.write(intRow+1, 18, self.getTotalNumberOfRecords(main_id,main_model),styleColumns)     
                
        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data_read = fp.read()
        fp.close()
        byte_arr = base64.b64encode(data_read)
        main_model.write({'excel_document':byte_arr})
        #self.excel_document = byte_arr

    def returnRowValue(self,field_value, psheet, pRowNumber, pRowColumn, pstyleColumns):
        if isinstance(field_value, bool):                
            return psheet.write(pRowNumber, pRowColumn, "",pstyleColumns)
        else:
            return psheet.write(pRowNumber, pRowColumn, field_value,pstyleColumns)

    def ReturnValue(field_value):
        if isinstance(field_value, bool):
            return ""
        else:
            return field_value

class hrDisembarkationMenuTreeView(models.Model):
    _name = 'hr.disembarkation.tree'
    _description = 'Disembarkation Report Tree View'

    # # @api.one
    def getPassportNumber(self):
        date = datetime.datetime.strftime(DATE_NOW, "%Y-%m-%d")
        query = SQL_QUERY %{'my_date': date, 'employee_id': self.employee_id, 'my_abbrv': PASSPORT_CODE}
        self.env.cr.execute(query)
        passportInfos = self.env.cr.fetchall()
        if len(passportInfos) > 0:
            self.passport = passportInfos[0][0]
            self.passport_date_issued = passportInfos[0][1]
            self.passport_date_expiry = passportInfos[0][2]

    # # @api.one
    def getSsribNumber(self):
        date = datetime.datetime.strftime(DATE_NOW, "%Y-%m-%d")
        query = SQL_QUERY %{'my_date': date, 'employee_id': self.employee_id, 'my_abbrv': SSRIB_CODE}
        self.env.cr.execute(query)
        ssribInfos = self.env.cr.fetchall()
        if len(ssribInfos) > 0:
            self.ssrib = ssribInfos[0][0]
            self.ssrib_date_issued = ssribInfos[0][1]
            self.ssrib_date_expiry = ssribInfos[0][2]

    active_id = fields.Many2one('hr.disembarkation.main', 'Employee')
    employee_number = fields.Char("Employee Number", readonly=True)
    ccl_number = fields.Char("CCL Number", readonly=True)
    last_name = fields.Char("Last Name", readonly=True)
    first_name = fields.Char("First Name", readonly=True)
    employment_rank = fields.Many2one("hr.rank", readonly=True, string="Rank")
    country_id = fields.Many2one('res.country', 'Nationality',readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], readonly=True, string ='Gender')
    placeof_birth = fields.Char("Place of Birth", readonly=True)

    passport = fields.Char('Passport', readonly=True, compute =getPassportNumber)
    passport_date_issued = fields.Date('Date issued', readonly=True, compute = getPassportNumber)
    passport_date_expiry = fields.Date('Date expiry', readonly=True, compute = getPassportNumber)

    ssrib = fields.Char('SSIRB', readonly=True, compute=getSsribNumber)
    ssrib_date_issued = fields.Date('Date issued', readonly=True, compute=getSsribNumber)
    ssrib_date_expiry = fields.Date('Date expiry', readonly=True, compute=getSsribNumber)

    place_signoff = fields.Many2one('hr.port', 'Place signoff')

    date_depart = fields.Date("Depart Date", readonly=True)
    date_servicefrom = fields.Date("Sign On Date", readonly=True)
    date_serviceto = fields.Date("Sign Off Date", readonly=True)
    employment_dept_code = fields.Many2one("hr.ship.department", readonly=True, string="Ship Department")
    object_code = fields.Many2one("hr.vessel", readonly=True, string="Vessel")
    employee_id = fields.Integer('Employee ID',readonly=True)

    employee_contractNumber =  fields.Char("Employee Number", readonly=True, compute ='getContractNumber')


    # # @api.one
    def getContractNumber(self):
        model_employee =self.env['hr.employee'].search([('id', '=', self.employee_id)])
        self.employee_contractNumber = model_employee.employee_contract_number    

    # # @api.one
    def genReport(self):
        pass

    # # @api.one
    def GenerateReport(self):
        pass        

#--- Embarkation Report
class hrEmbarkationMenuMainView(models.Model):
    _name = 'hr.embarkation.main'
    _description = 'Embarkation Report Main'

    def _getExcelFilename(self):
            self.excel_filename = 'Embarkation.xls'     

    def _getPDFfilename(self):
            self.pdf_filename = 'Embarkation.pdf'   

    name = fields.Char('Name')
    vessel = fields.Many2one('hr.vessel','Vessel', required =True)
    date_search = fields.Date('Date')
    excel_filename = fields.Char('file name', readonly = True,store = False,compute ='_getExcelFilename')
    excel_document = fields.Binary('Excel Report')
    pdf_filename = fields.Char('file name', readonly = True,store = False,compute ='_getPDFfilename')
    pdf_document = fields.Binary('PDF Report')    
    detail_id = fields.One2many('hr.embarkation.tree','active_id', readonly=False,copy=False)
    sort_by = fields.Selection(EMBARKATION, 'Sorted by')
    sorting_type = fields.Selection(SORTING_TYPE, 'Sorted Type', default= SORTING_TYPE[0][0])    


    def genReport(self, cr, uid, ids, context=None):
        return self.pool['report'].get_action(cr, uid, ids, 'bahia_personnel_management.report_embarkation', context=context)

    @api.model
    def createReport(self, id_main  = 0):
        main_model = self.env[self._name].search([('id', '=', id_main['id_main'])])
        tree_model = self.env['hr.embarkation.tree']

        name_val  = 'Embarkation_Report_' + str(self._uid) 
        main_model.update({'name':name_val})
        if len(main_model) > 0:
            if  isinstance(main_model.date_search, bool):
                QUERY = "Select * from hr_embarkation_report where" \
                        " object_code = %(vessel)d" %{'vessel': main_model.vessel.id}                
            elif len(str(main_model.date_search)) > 0:
                #QUERY = "Select * from hr_embarkation_report where ('%(date)s'::DATE) BETWEEN date_servicefrom and date_serviceto" \
                #        " and object_code = %(vessel)d" %{'date': main_model.date_search, 'vessel': main_model.vessel.id}
                QUERY = "Select * from hr_embarkation_report where ('%(date)s'::DATE) = date_servicefrom" \
                        " and object_code = %(vessel)d" %{'date': main_model.date_search, 'vessel': main_model.vessel.id}                
            else:
                QUERY = "Select * from hr_embarkation_report where" \
                        " object_code = %(vessel)d" %{'vessel': main_model.vessel.id}


            if not isinstance(main_model.sort_by, bool) and len(main_model.sort_by) > 0:
                QUERY += " ORDER BY %(sort_by)s" %{'sort_by': main_model.sort_by}

                if not isinstance(main_model.sorting_type, bool) and len(main_model.sorting_type) > 0: 
                    QUERY += " %(sorting_type)s" %{'sorting_type': main_model.sorting_type}     


            #TO EXECUTE SQL QUERY
            self.env.cr.execute(QUERY)
            for fetch in self.env.cr.fetchall():

                tree_model.create({
                    'active_id': id_main['id_main'],
                    'employee_number' : fetch[1],
                    'ccl_number' : fetch[2],
                    'last_name'  : fetch[3],
                    'first_name'  : fetch[4],                    
                    'employment_rank'  : fetch[5],
                    'country_id'  : fetch[6],
                    'gender'  : fetch[7],
                    'placeof_birth'  : fetch[8],
                    'passport'  : fetch[9],
                    'passport_date_issued'  : fetch[10],
                    'passport_date_expiry'  : fetch[11],
                    'ssrib'  : fetch[12],
                    'ssrib_date_issued'  : fetch[13],
                    'ssrib_date_expiry'  : fetch[14],
                    'place_signon'  : fetch[15],
                    'date_depart'  : fetch[16],
                    'date_servicefrom'  : fetch[17],
                    'date_serviceto'  : fetch[18],
                    'employment_dept_code'  : fetch[19],
                    'object_code'  : fetch[20],                                                                                                    
                    'employee_id'  : fetch[21],                     
                    })   
            #Create Now an Excel File
            self.createExcelFile(id_main['id_main'],main_model)


    def getTotalNumberOfRecords(self, main_id, main_model):
        intTotal = 0
        intTotal = self.env['hr.embarkation.tree'].search_count([('active_id','=',main_id)])
        return intTotal

    @api.model
    def createExcelFile(self, main_id, main_model):
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
        sheet.write_merge(intRow,intRow+1, 0,17, "EMBARKATION REPORT", styleHeader)  
        intRow +=2
        #HEADER
        sheet.write(intRow, 0, "Vessel:")
        sheet.write(intRow, 1, main_model.vessel.name)       
        intRow +=1
        if not isinstance(main_model.date_search, bool):
            sheet.write(intRow, 0, "Date:")
            sheet.write(intRow, 1, main_model.date_search)
        else:
            sheet.write(intRow, 0, "Date:")
            sheet.write(intRow, 1, "All Date")                   
        intRow +=2          
       
        #COLUMNS


        sheet.write(intRow, 0,"Employee Number",styleColumns)
        sheet.write(intRow, 1, "CCL Number",styleColumns)
        sheet.write(intRow, 2, "Last Name",styleColumns)
        sheet.write(intRow, 3, "First Name",styleColumns)

        sheet.write(intRow, 4, "Department",styleColumns)
        sheet.write(intRow, 5, "Rank",styleColumns)
        sheet.write(intRow, 6, "place of Birth",styleColumns)
        sheet.write(intRow, 7, "Nationality",styleColumns)
        sheet.write(intRow, 8, "Gender",styleColumns)
        sheet.write(intRow, 9, "Passport",styleColumns)
        sheet.write(intRow, 10,"Date Issued",styleColumns)
        sheet.write(intRow, 11, "Date Expiry",styleColumns)
        sheet.write(intRow, 12, "SSIRB",styleColumns)
        sheet.write(intRow, 13, "Date Issued",styleColumns)
        sheet.write(intRow, 14, "Date Expiry",styleColumns)
       
        sheet.write(intRow, 15, "Depart Date",styleColumns)
        sheet.write(intRow, 16, "Sign On Date",styleColumns)
        sheet.write(intRow, 17, "Sign Off Date",styleColumns)        
        sheet.write(intRow, 18, "Place Sign On",styleColumns)
        intRow +=1


        #DETAILS
        tree_model = self.env['hr.embarkation.tree'].search([('active_id','=',main_id)])
        for detail in tree_model:
            #str_empnumber = str(detail.employee_number)
            str_empnumber = str(detail.employee_contractNumber)
            sheet.write(intRow, 0, str_empnumber.zfill(10),styleColumns)
            self.returnRowValue(detail.ccl_number, sheet, intRow, 1, styleColumns)  
            sheet.write(intRow, 2, detail.last_name,styleColumns)
            sheet.write(intRow, 3, detail.first_name,styleColumns)
            sheet.write(intRow, 4, detail.employment_dept_code.name,styleColumns)
            sheet.write(intRow, 5, detail.employment_rank.name,styleColumns)


            self.returnRowValue(detail.placeof_birth, sheet, intRow, 6, styleColumns)

            sheet.write(intRow, 7, detail.country_id.name,styleColumns)
            sheet.write(intRow, 8, detail.gender,styleColumns)

            self.returnRowValue(detail.passport, sheet, intRow, 9, styleColumns)
            self.returnRowValue(detail.passport_date_issued, sheet, intRow, 10, styleColumns)
            self.returnRowValue(detail.passport_date_expiry, sheet, intRow, 11, styleColumns)     

            self.returnRowValue(detail.ssrib, sheet, intRow, 12, styleColumns)
            self.returnRowValue(detail.ssrib_date_issued, sheet, intRow, 13, styleColumns)
            self.returnRowValue(detail.ssrib_date_expiry, sheet, intRow, 14, styleColumns)    

            self.returnRowValue(detail.date_depart, sheet, intRow, 15, styleColumns) 

            #sheet.write(intRow, 14, detail.date_depart,styleColumns)
            sheet.write(intRow, 16, detail.date_servicefrom,styleColumns)
            sheet.write(intRow, 17, detail.date_serviceto,styleColumns) 
            self.returnRowValue(detail.place_signon.name, sheet, intRow, 18, styleColumns)       
            #sheet.write(intRow, 17, detail.place_signoff.name,styleColumns)

            intRow +=1
        sheet.write_merge(intRow+1,intRow+1, 16,17, "Total Record/s")    
        sheet.write(intRow+1, 18, self.getTotalNumberOfRecords(main_id,main_model),styleColumns)        
        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data_read = fp.read()
        fp.close()
        byte_arr = base64.b64encode(data_read)
        main_model.write({'excel_document':byte_arr})
        #self.excel_document = byte_arr

    def returnRowValue(self,field_value, psheet, pRowNumber, pRowColumn, pstyleColumns):
        if isinstance(field_value, bool):                
            return psheet.write(pRowNumber, pRowColumn, "",pstyleColumns)
        else:
            return psheet.write(pRowNumber, pRowColumn, field_value,pstyleColumns)

    def ReturnValue(field_value):
        if isinstance(field_value, bool):
            return ""
        else:
            return field_value        

class hrEmbarkationMenuTreeView(models.Model):
    _name = 'hr.embarkation.tree'
    _description = 'Embarkation Report Tree View'

    # # @api.one
    def getPassportNumber(self):
        date = datetime.datetime.strftime(DATE_NOW, "%Y-%m-%d")
        query = SQL_QUERY %{'my_date': date, 'employee_id': self.employee_id, 'my_abbrv': PASSPORT_CODE}
        self.env.cr.execute(query)
        passportInfos = self.env.cr.fetchall()
        if len(passportInfos) > 0:
            self.passport = passportInfos[0][0]
            self.passport_date_issued = passportInfos[0][1]
            self.passport_date_expiry = passportInfos[0][2]

    # # @api.one
    def getSsribNumber(self):
        date = datetime.datetime.strftime(DATE_NOW, "%Y-%m-%d")
        query = SQL_QUERY %{'my_date': date, 'employee_id': self.employee_id, 'my_abbrv': SSRIB_CODE}
        self.env.cr.execute(query)
        ssribInfos = self.env.cr.fetchall()
        if len(ssribInfos) > 0:
            self.ssrib = ssribInfos[0][0]
            self.ssrib_date_issued = ssribInfos[0][1]
            self.ssrib_date_expiry = ssribInfos[0][2]

    active_id = fields.Many2one('hr.embarkation.main', 'Employee')
    employee_number = fields.Char("Employee Number", readonly=True)
    ccl_number = fields.Char("CCL Number", readonly=True)
    last_name = fields.Char("Last Name", readonly=True)
    first_name = fields.Char("First Name", readonly=True)
    employment_rank = fields.Many2one("hr.rank", readonly=True, string="Rank")
    country_id = fields.Many2one('res.country', 'Nationality',readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], readonly=True, string ='Gender')
    placeof_birth = fields.Char("Place of Birth", readonly=True)

    passport = fields.Char('Passport', readonly=True, compute =getPassportNumber)
    passport_date_issued = fields.Date('Date issued', readonly=True, compute = getPassportNumber)
    passport_date_expiry = fields.Date('Date expiry', readonly=True, compute = getPassportNumber)

    ssrib = fields.Char('SSIRB', readonly=True, compute=getSsribNumber)
    ssrib_date_issued = fields.Date('Date issued', readonly=True, compute=getSsribNumber)
    ssrib_date_expiry = fields.Date('Date expiry', readonly=True, compute=getSsribNumber)

    place_signon = fields.Many2one('hr.port', 'Place signon')

    date_depart = fields.Date("Depart Date", readonly=True)
    date_servicefrom = fields.Date("Sign On Date", readonly=True)
    date_serviceto = fields.Date("Sign Off Date", readonly=True)
    employment_dept_code = fields.Many2one("hr.ship.department", readonly=True, string="Ship Department")
    object_code = fields.Many2one("hr.vessel", readonly=True, string="Vessel")
    employee_id = fields.Integer('Employee ID',readonly=True)
    employee_contractNumber =  fields.Char("Employee Number", readonly=True, compute ='getContractNumber')


    # # @api.one
    def getContractNumber(self):
        model_employee =self.env['hr.employee'].search([('id', '=', self.employee_id)])
        self.employee_contractNumber = model_employee.employee_contract_number  

    # # @api.one
    def genReport(self):
        pass

    # # @api.one
    def GenerateReport(self):
        pass        

#--- SignOnOff Report
class hrSignOnoffMenuMainView(models.Model):
    _name = 'hr.signonoff.report.main'
    _description = 'SignOnOff Report Main'

    def _getExcelFilename(self):
        if self.signonoff_selection == 'signon':
            self.excel_filename = 'Sign On Report.xls' 
        else:    
            self.excel_filename = 'Sign Off Report.xls' 

    def _getPDFfilename(self):
        if self.signonoff_selection == 'signon':
            self.pdf_filename = 'Sign On Report.pdf' 
        else:    
            self.pdf_filename = 'Sign Off Report.pdf'            

    name = fields.Char('Name')
    signonoff_selection = fields.Selection([('signon', 'Sign On'), ('signoff', 'Sign Off')], string ='Report Type', default = 'signon', required=True)
    vessel = fields.Many2one('hr.vessel','Vessel', required =True)
    date_from_search = fields.Date('Date From')
    date_to_search = fields.Date('Date to')
    employment_status = fields.Many2one('hr.employment.status', 'Employment Status')
    sort_by = fields.Selection(SIGNONSIGNOFF, 'Sorted by')
    sorting_type = fields.Selection(SORTING_TYPE, 'Sorted Type', default= SORTING_TYPE[0][0])   

    excel_filename = fields.Char('file name', readonly = True,store = False,compute ='_getExcelFilename')
    excel_document = fields.Binary('Excel Report')
    pdf_filename = fields.Char('file name', readonly = True,store = False,compute ='_getPDFfilename')
    pdf_document = fields.Binary('PDF Report')    
    detail_id = fields.One2many('hr.signonoff.report.tree','active_id', readonly=False,copy=False)
    is_with_remarks = fields.Boolean('With Remarks', default = False)

    def genReport(self, cr, uid, ids, context=None):
        return self.pool['report'].get_action(cr, uid, ids, 'bahia_personnel_management.report_signonoff', context=context)

    @api.model
    def createReport(self, id_main  = 0):
        main_model = self.env[self._name].search([('id', '=', id_main['id_main'])])
        tree_model = self.env['hr.signonoff.report.tree']
        name_val  = 'Sign_Off_Report_' + str(self._uid) 
        if self.signonoff_selection == 'signon': 
            name_val  = 'Sign_On_Report_' + str(self._uid) 

        main_model.update({'name':name_val})
        if len(main_model) > 0:
            if main_model.signonoff_selection == 'signon':
                if isinstance(main_model.date_from_search, bool) and isinstance(main_model.date_to_search, bool):
                    QUERY = "Select * from hr_signonoff_report where" \
                            " object_code = %(vessel)d" %{'vessel': main_model.vessel.id}  

                elif not isinstance(main_model.date_from_search, bool) and isinstance(main_model.date_to_search, bool):
                    QUERY = "Select * from hr_signonoff_report where" \
                            " object_code = %(vessel)d " \
                            " and date_servicefrom between ('%(date_from)s'::DATE) and ('2500-12-31'::DATE)" %{'date_from': main_model.date_from_search ,'vessel': main_model.vessel.id}                

                elif isinstance(main_model.date_from_search, bool) and not isinstance(main_model.date_to_search, bool):
                    QUERY = "Select * from hr_signonoff_report where" \
                            " object_code = %(vessel)d " \
                            " and date_servicefrom between ('1900-01-01'::DATE) and ('%(date_to)s'::DATE) " %{'date_to': main_model.date_to_search ,'vessel': main_model.vessel.id} 

                elif not isinstance(main_model.date_from_search, bool) and not isinstance(main_model.date_to_search, bool):
                    QUERY = "Select * from hr_signonoff_report where" \
                            " object_code = %(vessel)d " \
                            " and date_servicefrom between ('%(date_from)s'::DATE) and ('%(date_to)s'::DATE) " %{'date_from': main_model.date_from_search ,
                                                                                                                 'date_to': main_model.date_to_search ,
                                                                                                                 'vessel': main_model.vessel.id} 

                #else:
                #    QUERY = "Select * from hr_signonoff_report where" \
                #            " object_code = %(vessel)d" %{'vessel': main_model.vessel.id}
            else:
                if isinstance(main_model.date_from_search, bool) and isinstance(main_model.date_to_search, bool):
                    QUERY = "Select * from hr_signonoff_report where" \
                            " object_code = %(vessel)d" %{'vessel': main_model.vessel.id}  

                elif not isinstance(main_model.date_from_search, bool) and isinstance(main_model.date_to_search, bool):
                    QUERY = "Select * from hr_signonoff_report where" \
                            " object_code = %(vessel)d " \
                            " and date_serviceto between ('%(date_from)s'::DATE) and ('2500-12-31'::DATE)" %{'date_from': main_model.date_from_search ,'vessel': main_model.vessel.id}                

                elif isinstance(main_model.date_from_search, bool) and not isinstance(main_model.date_to_search, bool):
                    QUERY = "Select * from hr_signonoff_report where" \
                            " object_code = %(vessel)d " \
                            " and date_serviceto between ('1900-01-01'::DATE) and ('%(date_to)s'::DATE) " %{'date_to': main_model.date_to_search ,'vessel': main_model.vessel.id} 

                elif not isinstance(main_model.date_from_search, bool) and not isinstance(main_model.date_to_search, bool):
                    QUERY = "Select * from hr_signonoff_report where" \
                            " object_code = %(vessel)d " \
                            " and date_serviceto between ('%(date_from)s'::DATE) and ('%(date_to)s'::DATE) " %{'date_from': main_model.date_from_search ,
                                                                                                                 'date_to': main_model.date_to_search ,
                                                                                                                 'vessel': main_model.vessel.id} 

            if not isinstance(main_model.employment_status, bool) and len(main_model.employment_status) > 0:
                QUERY += " and employment_status = %(employment_status_id)d" %{'employment_status_id': main_model.employment_status.id}

            if main_model.is_with_remarks:
                QUERY += "  and (remarks is not null and length(trim(remarks)) > 0) "


            if not isinstance(main_model.sort_by, bool) and len(main_model.sort_by) > 0:
                QUERY += " ORDER BY %(sort_by)s" %{'sort_by': main_model.sort_by}

                if not isinstance(main_model.sorting_type, bool) and len(main_model.sorting_type) > 0: 
                    QUERY += " %(sorting_type)s" %{'sorting_type': main_model.sorting_type}
		
#            if main_model.is_with_remarks:
#                QUERY += "  and (remarks is not null and length(trim(remarks)) > 0 "

            #TO EXECUTE SQL QUERY
            self.env.cr.execute(QUERY)
            for fetch in self.env.cr.fetchall():
                tree_model.create({
                    'active_id': id_main['id_main'],
                    'employee_number' : fetch[1],
                    'ccl_number' : fetch[2],
                    'employment_rank'  : fetch[3],
                    'last_name'  : fetch[4],
                    'first_name'  : fetch[5],                                        
                    'birth_date'  : fetch[6],
                    'employment_status'  : fetch[7],
                    'date_depart'  : fetch[8],
                    'employment_dept_code'  : fetch[9],
                    'date_servicefrom'  : fetch[10],
                    'date_serviceto'  : fetch[11],
                    'object_code'  : fetch[12],
                    'remarks'  : fetch[13],                     
                    })   
            #Create Now an Excel File
            self.createExcelFile(id_main['id_main'],main_model)

    def getTotalNumberOfRecords(self, main_id, main_model):
        intTotal = 0
        intTotal = self.env['hr.signonoff.report.tree'].search_count([('active_id','=',main_id)])
        return intTotal

    @api.model
    def createExcelFile(self, main_id, main_model):
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
        if main_model.signonoff_selection == "signon":
            sheet.write_merge(intRow,intRow+1, 0,9, "SIGN ON REPORT", styleHeader)  
        else:
            sheet.write_merge(intRow,intRow+1, 0,9, "SIGN OFF REPORT", styleHeader)  
        intRow +=2
        #HEADER
        sheet.write(intRow, 0, "Vessel:")
        sheet.write(intRow, 1, main_model.vessel.name)       
        intRow +=1
     
        if not isinstance(main_model.date_from_search, bool) and not isinstance(main_model.date_to_search, bool):
            sheet.write(intRow, 0, "Date:")
            sheet.write(intRow, 1, str(main_model.date_from_search) + ' - '  + str(main_model.date_to_search)) 
        elif  isinstance(main_model.date_from_search, bool) and not isinstance(main_model.date_to_search, bool):    
            sheet.write(intRow, 0, "Date:")
            sheet.write(intRow, 1, 'less than or equal to ' + str(main_model.date_to_search))       
        elif  not isinstance(main_model.date_from_search, bool) and isinstance(main_model.date_to_search, bool):    
            sheet.write(intRow, 0, "Date:")
            sheet.write(intRow, 1, 'greater than or equal to ' + str(main_model.date_from_search))                     
        else:
            sheet.write(intRow, 0, "Date:")
            sheet.write(intRow, 1, "All Date")                   
        intRow +=2          
       
        #COLUMNS    
        sheet.write(intRow, 0,"Employee Number",styleColumns)
        sheet.write(intRow, 1, "CCL Number",styleColumns)        
        sheet.write(intRow, 2, "Department",styleColumns)
        sheet.write(intRow, 3, "Rank",styleColumns)
        sheet.write(intRow, 4, "Last Name",styleColumns)
        sheet.write(intRow, 5, "First Name",styleColumns)
        sheet.write(intRow, 6, "Birth Date",styleColumns)
        sheet.write(intRow, 7, "Status",styleColumns)
        sheet.write(intRow, 8, "Depart Date",styleColumns)
        sheet.write(intRow, 9, "Sign On Date",styleColumns)
        sheet.write(intRow, 10, "Sign Off Date",styleColumns)
        intRow +=1

        #DETAILS
        tree_model = self.env['hr.signonoff.report.tree'].search([('active_id','=',main_id)])
        for detail in tree_model:
            str_empnumber = str(detail.employee_number)
            sheet.write(intRow, 0, str_empnumber.zfill(10),styleColumns)
            self.returnRowValue(detail.ccl_number, sheet, intRow, 1, styleColumns)  
            self.returnRowValue(detail.employment_dept_code.name, sheet, intRow, 2, styleColumns)  
            
            sheet.write(intRow, 3, detail.employment_rank.name,styleColumns)
            sheet.write(intRow, 4, detail.last_name,styleColumns)
            sheet.write(intRow, 5, detail.first_name,styleColumns)
            self.returnRowValue(detail.birth_date, sheet, intRow, 6, styleColumns)
            self.returnRowValue(detail.employment_status.name, sheet, intRow, 7, styleColumns)
            self.returnRowValue(detail.date_depart, sheet, intRow, 8, styleColumns)
            self.returnRowValue(detail.date_servicefrom, sheet, intRow, 9, styleColumns)
            self.returnRowValue(detail.date_serviceto, sheet, intRow, 10, styleColumns)
            intRow +=1

        sheet.write_merge(intRow+1,intRow+1, 8,9, "Total Record/s")    
        sheet.write(intRow+1, 10, self.getTotalNumberOfRecords(main_id,main_model),styleColumns)    
        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data_read = fp.read()
        fp.close()
        byte_arr = base64.b64encode(data_read)
        main_model.write({'excel_document':byte_arr})
        #self.excel_document = byte_arr

    def returnRowValue(self,field_value, psheet, pRowNumber, pRowColumn, pstyleColumns):
        if isinstance(field_value, bool):                
            return psheet.write(pRowNumber, pRowColumn, "",pstyleColumns)
        else:
            return psheet.write(pRowNumber, pRowColumn, field_value,pstyleColumns)

    def ReturnValue(field_value):
        if isinstance(field_value, bool):
            return ""
        else:
            return field_value        

class hrSignOnoffMenuTreeView(models.Model):
    _name = 'hr.signonoff.report.tree'
    _description = 'SignOnOff Report Tree'

    active_id = fields.Many2one('hr.signonoff.report.main', 'Employee')
    employee_number = fields.Char("Employee Number", readonly=True)
    ccl_number = fields.Char("CCL Number", readonly=True)
    employment_rank = fields.Many2one("hr.rank", readonly=True, string="Rank")
    last_name = fields.Char("Last Name", readonly=True)
    first_name = fields.Char("First Name", readonly=True)
    birth_date = fields.Date("Birth Date", readonly=True)
    employment_status = fields.Many2one("hr.employment.status", readonly=True, string="Status")
    date_depart = fields.Date("Depart Date", readonly=True)
    employment_dept_code = fields.Many2one("hr.ship.department", readonly=True, string="Ship Department")
    date_servicefrom = fields.Date("Sign On Date", readonly=True)
    date_serviceto = fields.Date("Sign Off Date", readonly=True)
    object_code = fields.Many2one("hr.vessel", readonly=True, string="Vessel")
    remarks = fields.Char("Remarks", readonly=True)


    # # @api.one
    def genReport(self):
        pass

    # # @api.one
    def GenerateReport(self):
        pass        


#--- Active Personnel with Relative Report
class hrPersonnelActiveOnBoardwithRelativeMenuMainView(models.Model):
    _name = 'hr.personnel.withrelative.main'
    _description = 'Active Personnel with Relative Report'

    def _getExcelFilename(self):
            self.excel_filename = 'Crew List Active on Board with Relative.xls'     

    def _getPDFfilename(self):
            self.pdf_filename = 'Crew List Active on Board with Relative.pdf'   

    name = fields.Char('Name')
    vessel = fields.Many2one('hr.vessel','Vessel')
    date_search = fields.Date('Date')
    excel_filename = fields.Char('file name', readonly = True,store = False,compute ='_getExcelFilename')
    excel_document = fields.Binary('Excel Report')
    pdf_filename = fields.Char('file name', readonly = True,store = False,compute ='_getPDFfilename')
    pdf_document = fields.Binary('PDF Report')    
    personnel_actived_on_board = fields.One2many('hr.personnel.withrelative.tree','active_id', readonly=False,copy=False)
    employment_status = fields.Many2one('hr.employment.status', 'Employment Status')
    sort_by = fields.Selection(WITH_REMARKS_COLUMNS, 'Sorted by')
    sorting_type = fields.Selection(SORTING_TYPE, 'Sorted Type', default= SORTING_TYPE[0][0])  
    is_with_remarks = fields.Boolean('With Remarks', default = False) 

    def genReport(self, cr, uid, ids, context=None):
        return self.pool['report'].get_action(cr, uid, ids, 'bahia_personnel_management.report_personnel_active_on_board_w_relative', context=context)

    @api.model
    def createReport(self, id_main  = 0):
        main_model = self.env[self._name].search([('id', '=', id_main['id_main'])])
        tree_model = self.env['hr.personnel.withrelative.tree']
        name_val  = 'Crewlist_active_on_board_with_relative_' + str(self._uid) 
        QUERY = "Select * from hr_personnel_withrelative_report"
        main_model.update({'name':name_val})


        if len(main_model) > 0:

            if not isinstance(main_model.vessel.id, bool) and len(str(main_model.vessel.id)) > 0:
                QUERY += " where object_code = %(vessel)d" %{'vessel': main_model.vessel.id}                

            if  not isinstance(main_model.date_search, bool) and len(str(main_model.date_search)) > 0:
                if QUERY.find('where') > 0:
                    QUERY += " and ('%(date)s'::DATE) BETWEEN date_servicefrom and COALESCE(date_serviceto,date_servicefrom)"
                else:
                    QUERY += " where ('%(date)s'::DATE) BETWEEN date_servicefrom and COALESCE(date_serviceto,date_servicefrom)"

                QUERY  = QUERY %{'date': main_model.date_search}


            if not isinstance(main_model.employment_status, bool) and len(main_model.employment_status) > 0:
                if QUERY.find('where') > 0:
                    QUERY += " and employment_status = %(employment_status_id)d" 
                else:
                    QUERY += " where employment_status = %(employment_status_id)d"
                QUERY = QUERY %{'employment_status_id': main_model.employment_status.id}


            #if  isinstance(main_model.date_search, bool):
            #    QUERY = "Select * from hr_personnel_withrelative_report where" \
            #            " object_code = %(vessel)d" %{'vessel': main_model.vessel.id}                
            #elif len(main_model.date_search) > 0:
            #    QUERY = "Select * from hr_personnel_withrelative_report where ('%(date)s'::DATE) BETWEEN date_servicefrom and date_serviceto" \
            #            " and object_code = %(vessel)d" %{'date': main_model.date_search, 'vessel': main_model.vessel.id}
            #else:
            #    QUERY = "Select * from hr_personnel_withrelative_report where" \
            #            " object_code = %(vessel)d" %{'vessel': main_model.vessel.id}
            #if not isinstance(main_model.employment_status, bool) and len(main_model.employment_status) > 0:
            #    QUERY += " and employment_status = %(employment_status_id)d" %{'employment_status_id': main_model.employment_status.id}                        


            if not isinstance(main_model.sort_by, bool) and len(main_model.sort_by) > 0:
                QUERY += " ORDER BY %(sort_by)s" %{'sort_by': main_model.sort_by}

                if not isinstance(main_model.sorting_type, bool) and len(main_model.sorting_type) > 0: 
                    QUERY += " %(sorting_type)s" %{'sorting_type': main_model.sorting_type}     

            #TO EXECUTE SQL QUERY
            self.env.cr.execute(QUERY)
            for fetch in self.env.cr.fetchall():

                tree_model.create({
                    'active_id': id_main['id_main'],
                    'employee_number' : fetch[1],
                    'ccl_number' : fetch[2],
                    'employment_rank'  : fetch[3],
                    'last_name'  : fetch[4],
                    'first_name'  : fetch[5],
                    'birth_date'  : fetch[6],
                    'employment_status'  : fetch[7],
                    'date_servicefrom'  : fetch[8],
                    'date_serviceto'  : fetch[9],
                    'remarks'  : fetch[10],
                    'employment_dept_code'  : fetch[11],
                    'object_code'  :    fetch[12],
                    'relative_name':    fetch[13], 
                    'relationship':     fetch[14], 
                    'address':          fetch[15], 
                    'city':             fetch[16], 
                    'province':         fetch[17], 
                    'country_id':       fetch[18], 
                    'telephone_number': fetch[19], 
                    'mobile_number':    fetch[20], 
                    'email_number':     fetch[21], 
                    'is_beneficiary':   fetch[22], 
                    'is_allottee':      fetch[23],  
                    'employee_id':      fetch[24],             
                    })   
            #Create Now an Excel File
            self.createExcelFile(id_main['id_main'],main_model)


    def getTotalYearsService(self, main_id, main_model):

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

        #DETAILS
        tree_model = self.env['hr.personnel.withrelative.tree'].search([('active_id','=',main_id)])
        for employment_history in tree_model:
            str_service_range = employment_history.total_years_of_service
            str_service_range = str_service_range.split()
            if employment_history.employment_status.status_id == 'ACT':
                int_year = int(float(str_service_range[0].replace('Y','')))
                int_month = int(float(str_service_range[1].replace('M','')))
                int_day = int(float(str_service_range[2].replace('D','')))
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
        return  str(int_final_year) + 'Y ' + str(int_final_month) + 'M ' +  str(int_final_day).split('.')[0]  + 'D'

    @api.model
    def createExcelFile(self, main_id, main_model):
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
        sheet = workbook.add_sheet("Personnel Information")
        intRow = 0
        #REPORT TITLE
        sheet.write_merge(intRow,intRow+1, 0,20, "CREW LIST WITH RELATIVE INFORMATION", styleHeader)  
        intRow +=2
        #HEADER
        sheet.write(intRow, 0, "Vessel:")
        sheet.write(intRow, 1, main_model.vessel.name)       
        intRow +=1
        if not isinstance(main_model.date_search, bool):
            sheet.write(intRow, 0, "Date:")
            sheet.write(intRow, 1, main_model.date_search)
        else:
            sheet.write(intRow, 0, "Date:")
            sheet.write(intRow, 1, "All Date")                   
        intRow +=2          
       
        #COLUMNS
        sheet.write(intRow, 0,"Employee Number",styleColumns)
        sheet.write(intRow, 1, "CCL Number",styleColumns)
        sheet.write(intRow, 2, "Department",styleColumns)
        sheet.write(intRow, 3, "Rank",styleColumns)
        sheet.write(intRow, 4, "Last Name",styleColumns)
        sheet.write(intRow, 5, "First Name",styleColumns)
        sheet.write(intRow, 6, "Birth Date",styleColumns)
        sheet.write(intRow, 7, "Status",styleColumns)
        sheet.write(intRow, 8, "Service from",styleColumns)
        sheet.write(intRow, 9, "Service to",styleColumns)
        sheet.write_merge(intRow,intRow, 10,11, "Remarks",styleColumns)

        sheet.write(intRow, 12, "Relative's Name",styleColumns)
        sheet.write(intRow, 13, "Relationship",styleColumns)
        sheet.write(intRow, 14, "Address",styleColumns)
        sheet.write(intRow, 15, "City",styleColumns)

        sheet.write(intRow, 16, "Province",styleColumns)
        sheet.write(intRow, 17, "Telephone Number",styleColumns)
        sheet.write(intRow, 18, "Mobile Number",styleColumns)
        sheet.write(intRow, 19, "E-mail",styleColumns)                
        sheet.write(intRow, 20, "Beneficiary",styleColumns)                
        sheet.write(intRow, 21, "Allottee",styleColumns)      
        sheet.write(intRow, 22, "Total Service Length",styleColumns)                            
        intRow +=1

        #DETAILS
        tree_model = self.env['hr.personnel.withrelative.tree'].search([('active_id','=',main_id)])
        for detail in tree_model:
            #str_empnumber = str(detail.employee_number)
            str_empnumber = str(detail.employee_contractNumber)
            sheet.write(intRow, 0, str_empnumber.zfill(10),styleColumns)
            if isinstance(detail.ccl_number, bool):
                sheet.write(intRow, 1, "",styleColumns)
            else:
                sheet.write(intRow, 1, detail.ccl_number,styleColumns)

            sheet.write(intRow, 2, detail.employment_dept_code.name,styleColumns)
            sheet.write(intRow, 3, detail.employment_rank.name,styleColumns)
            sheet.write(intRow, 4, detail.last_name,styleColumns)
            sheet.write(intRow, 5, detail.first_name,styleColumns)
            sheet.write(intRow, 6, detail.birth_date,styleColumns)
            sheet.write(intRow, 7, detail.employment_status.name,styleColumns)
            sheet.write(intRow, 8, detail.date_servicefrom,styleColumns)
            sheet.write(intRow, 9, detail.date_serviceto,styleColumns)
            sheet.write_merge(intRow,intRow, 10,11, detail.remarks,styleColumns)
            self.returnRowValue(detail.relative_name, sheet, intRow, 12, styleColumns)
            self.returnRowValue(detail.relationship.name, sheet, intRow, 13, styleColumns)
            self.returnRowValue(detail.address, sheet, intRow, 14, styleColumns)
            self.returnRowValue(detail.city, sheet, intRow, 15, styleColumns)
            self.returnRowValue(detail.province, sheet, intRow, 16, styleColumns)
            self.returnRowValue(detail.telephone_number, sheet, intRow, 17, styleColumns)
            self.returnRowValue(detail.mobile_number, sheet, intRow, 18, styleColumns)
            self.returnRowValue(detail.email_number, sheet, intRow, 19, styleColumns)
            self.returnRowValue(detail.is_beneficiary, sheet, intRow, 20, styleColumns)
            self.returnRowValue(detail.is_allottee, sheet, intRow, 21, styleColumns)  
            self.returnRowValue(detail.total_years_of_service, sheet, intRow, 22, styleColumns)           
            intRow +=1

        sheet.write_merge(intRow+1,intRow+1, 20,21, "Total Service Length")    
        sheet.write(intRow+1, 22, self.getTotalYearsService(main_id,main_model),styleColumns)                

        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data_read = fp.read()
        fp.close()
        byte_arr = base64.b64encode(data_read)
        main_model.write({'excel_document':byte_arr})

    def returnRowValue(self,field_value, psheet, pRowNumber, pRowColumn, pstyleColumns):
        if isinstance(field_value, bool):                
            return psheet.write(pRowNumber, pRowColumn, "",pstyleColumns)
        else:
            return psheet.write(pRowNumber, pRowColumn, field_value,pstyleColumns)        

class hrPersonnelActiveOnBoardwithRelativeMenuTreeView(models.Model):
    _name = 'hr.personnel.withrelative.tree'
    _description = 'Personnel With Relative Tree'

    active_id = fields.Many2one('hr.personnel.withrelative.main', 'Employee')
    employee_number = fields.Char("Employee Number", readonly=True)
    ccl_number = fields.Char("CCL Number", readonly=True)
    employment_rank = fields.Many2one("hr.rank", readonly=True, string="Rank")
    last_name = fields.Char("Last Name", readonly=True)
    first_name = fields.Char("First Name", readonly=True)
    birth_date = fields.Date("Birth Date", readonly=True)
    employment_status = fields.Many2one("hr.employment.status", readonly=True, string="Status")
    date_servicefrom = fields.Date("Service from", readonly=True)
    date_serviceto = fields.Date("Service to", readonly=True)
    remarks = fields.Char("Remarks", readonly=True)
    employment_dept_code = fields.Many2one("hr.ship.department", readonly=True, string="Ship Department")
    object_code = fields.Many2one("hr.vessel", readonly=True, string="Vessel")

    relative_name = fields.Char("Relative's Name", readonly=True)
    relationship = fields.Many2one("hr.familyrelations", readonly=True, string="Relationship")
    address = fields.Char("Address", readonly=True)
    city = fields.Char("City", readonly=True)
    province = fields.Char("Province", readonly=True)
    country_id = fields.Many2one('res.country', 'Nationality', readonly=True)
    telephone_number = fields.Char("Telephone Number", readonly=True)
    mobile_number = fields.Char("Mobile Number", readonly=True)
    email_number = fields.Char("E-mail", readonly=True)
    is_beneficiary = fields.Boolean("Beneficiary", readonly=True)
    is_allottee = fields.Boolean("Alottee", readonly=True)
    employee_id = fields.Many2one("hr.employee", readonly=True, string="Employee ID")
    total_years_of_service = fields.Char('Service Length',store = False,compute ='getYearMonthDay')
    employee_contractNumber =  fields.Char("Employee Number", readonly=True, compute ='getContractNumber')


    # # @api.one
    def getContractNumber(self):
        self.employee_contractNumber = self.employee_id.employee_contract_number  

    # # @api.one
    def getYearMonthDay(self):
        self.total_years_of_service = self.employee_id.total_years_of_service

        #model_employee= self.env['hr.employee'].search([('employee_number', '=', self.employee_number)])
        #if model_employee:
        #    self.total_years_of_service = model_employee.total_years_of_service

#----------------------- DATABASE CREATION OF VIEW

# To View all the records and to create a customized reports
# Must be Naming convent

class hrPersonnelActiveOnBoardwithRemarks(models.Model):
    _name = "hr.personnel.withremrks.report"
    _description = 'Personnel With Remarks Report'
    _auto = False

    employee_number = fields.Char("Employee Number", readonly=True)
    ccl_number = fields.Char("CCL Number", readonly=True)
    employment_rank = fields.Many2one("hr.rank", readonly=True, string="Rank")
    last_name = fields.Char("Last Name", readonly=True)
    first_name = fields.Char("First Name", readonly=True)
    birth_date = fields.Date("Birth Date", readonly=True)
    employment_status = fields.Many2one("hr.employment.status", readonly=True, string="Status")
    date_servicefrom = fields.Date("Service from", readonly=True)
    date_serviceto = fields.Date("Service to", readonly=True)
    remarks = fields.Char("Remarks", readonly=True)
    employment_dept_code = fields.Many2one("hr.ship.department", readonly=True, string="Ship Department")
    object_code = fields.Many2one("hr.vessel", readonly=True, string="Vessel")
    employee_id = fields.Many2one("hr.employee", readonly=True, string="Employee ID")

    #AND LENGTH(TRIM(REMARKS )) > 0
    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'hr_personnel_withremrks_report')
        self.env.cr.execute("""
                   CREATE OR REPLACE VIEW hr_personnel_withremrks_report AS (
                        SELECT
                            MIN(EMPH.ID) AS ID,
                            EMPLOYEE_NUMBER,
                            CCL_NUMBER,
                            EMPLOYMENT_RANK,
                            LAST_NAME,
                            FIRST_NAME,
                            BIRTHDAY AS BIRTH_DATE,
                            EMPLOYMENT_STATUS,
                            DATE_SERVICEFROM,
                            DATE_SERVICETO,
                            REMARKS,
                            EMPLOYMENT_DEPT_CODE,
                            OBJECT_CODE,
                            EMP.ID AS EMPLOYEE_ID
                        FROM HR_EMPLOYEE EMP, HR_EMPLOYMENTHISTORY EMPH
                        WHERE EMP.ID = EMPH.EMPLOYEE_EMPLOYMENT_ID
                        GROUP BY OBJECT_CODE,
                             EMPLOYMENT_DEPT_CODE,
                             EMPLOYEE_NUMBER,
                             CCL_NUMBER,
                             EMPLOYMENT_RANK,
                             LAST_NAME ,
                             FIRST_NAME,
                             BIRTHDAY,
                             EMPLOYMENT_STATUS,
                             DATE_SERVICEFROM,
                             DATE_SERVICETO,
                             REMARKS,
                             EMPLOYMENT_DEPT_CODE,
                             EMP.ID)
                   """)


class hrPersonnelActiveonBoardwithRelatives(models.Model):
    _name = "hr.personnel.withrelative.report"
    _description = 'Personnel Active On Board With Relative Report'
    _auto = False

    employee_number = fields.Char("Employee Number", readonly=True)
    ccl_number = fields.Char("CCL Number", readonly=True)
    employment_rank = fields.Many2one("hr.rank", readonly=True, string="Rank")
    last_name = fields.Char("Last Name", readonly=True)
    first_name = fields.Char("First Name", readonly=True)
    birth_date = fields.Date("Birth Date", readonly=True)
    employment_status = fields.Many2one("hr.employment.status", readonly=True, string="Status")
    date_servicefrom = fields.Date("Service from", readonly=True)
    date_serviceto = fields.Date("Service to", readonly=True)
    remarks = fields.Char("Remarks", readonly=True)
    employment_dept_code = fields.Many2one("hr.ship.department", readonly=True, string="Ship Department")
    object_code = fields.Many2one("hr.vessel", readonly=True, string="Vessel")

    relative_name = fields.Char("Relative's Name", readonly=True)
    relationship = fields.Many2one("hr.familyrelations", readonly=True, string="Relationship")
    address = fields.Char("Address", readonly=True)
    city = fields.Char("City", readonly=True)
    province = fields.Char("Province", readonly=True)
    country_id = fields.Many2one('res.country', 'Nationality', readonly=True)
    telephone_number = fields.Char("Telephone Number", readonly=True)
    mobile_number = fields.Char("Mobile Number", readonly=True)
    email_number = fields.Char("E-mail", readonly=True)
    is_beneficiary = fields.Char("Beneficiary", readonly=True)
    is_allottee = fields.Boolean("Alottee", readonly=True)
    employee_id = fields.Many2one("hr.employee", readonly=True, string="Employee ID")

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'hr_personnel_withrelative_report')
        self.env.cr.execute("""
                   CREATE OR REPLACE VIEW hr_personnel_withrelative_report AS (
                        SELECT
                            MIN(EMPH.ID) AS ID,
                            EMPLOYEE_NUMBER,
                            CCL_NUMBER,
                            EMPLOYMENT_RANK,
                            LAST_NAME,
                            FIRST_NAME,
                            BIRTHDAY AS BIRTH_DATE,
                            EMPLOYMENT_STATUS,
                            DATE_SERVICEFROM,
                            DATE_SERVICETO,
                            REMARKS,
                            EMPLOYMENT_DEPT_CODE,
                            OBJECT_CODE,
                            RELATIVE_NAME,
                            RELATIONSHIP,
                            "Address",
                            CITY,
                            PROVINCE,
                            a.COUNTRY_ID,
                            TELEPHONE_NUMBER,
                            MOBILE_NUMBER,
                            EMAIL_NUMBER,
                            IS_BENEFICIARY,
                            IS_ALLOTTEE,
                            EMP.ID AS EMPLOYEE_ID
                        FROM HR_EMPLOYEE EMP
                        INNER JOIN 
                        HR_EMPLOYMENTHISTORY EMPH
                        ON EMP.ID = EMPH.EMPLOYEE_EMPLOYMENT_ID
                        INNER JOIN (
                            SELECT  employee_family_relationship_id,
                                NULLIF(last_name, '') || ' ' || NULLIF(first_name,'') || ' ' || NULLIF(middle_name,'') "relative_name",
                                relationship,
                                NULLIF(address_1,'') || ' ' || NULLIF(address_2,'') || ' ' || NULLIF(address_3,'') "Address",
                                city,
                                province,
                                country_id,
                                telephone_number,
                                mobile_number,
                                email_number,
                                is_beneficiary,
                                is_allottee        
                            from hr_employee_families   
                            where relation_level = 1
                            and employee_family_relationship_id IS NOT NULL
                        ) a ON a.employee_family_relationship_id = EMP.ID                        
                        GROUP BY OBJECT_CODE,
                                EMPLOYMENT_DEPT_CODE,
                                EMPLOYEE_NUMBER,
                                CCL_NUMBER,
                                EMPLOYMENT_RANK,
                                LAST_NAME ,
                                FIRST_NAME,
                                BIRTHDAY,
                                EMPLOYMENT_STATUS,
                                DATE_SERVICEFROM,
                                DATE_SERVICETO,
                                REMARKS,
                                EMPLOYMENT_DEPT_CODE,
                                RELATIVE_NAME,
                                RELATIONSHIP,
                                "Address",
                                CITY,
                                PROVINCE,
                                a.COUNTRY_ID,
                                TELEPHONE_NUMBER,
                                MOBILE_NUMBER,
                                EMAIL_NUMBER,
                                IS_BENEFICIARY,
                                IS_ALLOTTEE,
                                EMP.ID

                             )
                   """)


class hrCrewlistperDepartment(models.Model):
    _name = 'hr.crewlist.report'
    _description = 'Crewlist Report'
    _auto = False

    # @api.one
    def getPassportNumber(self):
        date = datetime.datetime.strftime(DATE_NOW, "%Y-%m-%d")
        query = SQL_QUERY %{'my_date': date, 'employee_id': self.employee_id, 'my_abbrv': PASSPORT_CODE}
        self.env.cr.execute(query)
        passportInfos = self.env.cr.fetchall()
        if len(passportInfos) > 0:
            self.passport = passportInfos[0][0]
            self.passport_date_issued = passportInfos[0][1]
            self.passport_date_expiry = passportInfos[0][2]

    employee_number = fields.Char("Employee Number", readonly=True)
    ccl_number = fields.Char("CCL Number", readonly=True)
    employment_rank = fields.Many2one("hr.rank", readonly=True, string="Rank")
    last_name = fields.Char("Last Name", readonly=True)
    first_name = fields.Char("First Name", readonly=True)
    birth_date = fields.Date("Birth Date", readonly=True)
    placeof_birth = fields.Char("Place of Birth", readonly=True)
    passport = fields.Char('Passport', readonly=True, compute =getPassportNumber)
    passport_date_issued = fields.Date('Date issued', readonly=True, compute = getPassportNumber)
    passport_date_expiry = fields.Date('Date expiry', readonly=True, compute = getPassportNumber)

    date_depart = fields.Date("Depart Date", readonly=True)
    date_servicefrom = fields.Date("Sign On Date", readonly=True)
    date_serviceto = fields.Date("Sign Off Date", readonly=True)
    place_signon = fields.Many2one('hr.port', 'Place signOn')

    employee_id = fields.Integer('Employee ID',readonly=True)
    employment_dept_code = fields.Many2one("hr.ship.department", readonly=True, string="Ship Department")
    object_code = fields.Many2one("hr.vessel", readonly=True, string="Vessel")

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'hr_crewlist_report')
        self.env.cr.execute("""
                   CREATE OR REPLACE VIEW hr_crewlist_report AS (
                        SELECT
                            EMPH.ID ID,
                            EMP.ID EMPLOYEE_ID,
                            EMPLOYEE_CONTRACT_NUMBER AS EMPLOYEE_NUMBER,
                            CCL_NUMBER,
                            LAST_NAME,
                            FIRST_NAME,
                            EMPLOYMENT_RANK,
                            COUNTRY_ID,
                            BIRTHDAY BIRTH_DATE,
                            PLACEOF_BIRTH,
                            '' PASSPORT,
                            '' PASSPORT_DATE_ISSUED,
                            '' PASSPORT_DATE_EXPIRY,
                            DATE_DEPARTURE DATE_DEPART,
                            DATE_SERVICETO,
                            DATE_SERVICEFROM,
                            "place_signOn" PLACE_SIGNON,
                            OBJECT_CODE,
                            EMPLOYMENT_DEPT_CODE
                        FROM HR_EMPLOYEE EMP, HR_EMPLOYMENTHISTORY EMPH
                        WHERE EMP.ID = EMPH.EMPLOYEE_EMPLOYMENT_ID
                        )
                   """)

class hrServiceRecordperDepartment(models.Model):
    _name = "hr.service.record.report"
    _description = 'Service Record per Department'
    _auto = False

    # @api.one
    def getServiceLength(self):
        days_remaining = 0
        service_days = int(abs(((self.days_of_service /SECOND_PER_MINUTE)/MINUTE_PER_HOUR)/HOUR_PER_DAY))
        if service_days == 0:
            self.service_length = '0Y 0M 0D'
        elif service_days <= 30:
            self.service_length = '0Y 1M 0D'
        else:
            year = int(abs(service_days/ YEAR))

            days_remaining = int(service_days- (year * YEAR))

            months = int(abs(days_remaining / MONTH))
            days_remaining =days_remaining -  (months * MONTH)
            self.service_length = str(year) + 'Y ' + str(months) + 'M ' +  str(days_remaining)  + 'D'
    # @api.one
    def getEarnedIncentive(self):
        incentive_days = int(abs(((self.incentive_length /SECOND_PER_MINUTE)/MINUTE_PER_HOUR)/HOUR_PER_DAY))
        days_remaining = incentive_days
        if incentive_days == 0:
            self.earned_incentive = '0Y 0M 0D'
        elif incentive_days <= 30:
            self.earned_incentive = '0Y 1M 0D'
        else:
            years = int(abs(incentive_days/YEAR))

            days_remaining = int(incentive_days- (years * YEAR))
            months = abs(days_remaining / MONTH)
            days_remaining =days_remaining -  (months * MONTH)
            self.earned_incentive = str(int(years)) + 'Y ' + str(months) + 'M ' +  str(days_remaining) + 'D'

    # @api.one
    def getserviceincentive(self):
        incentives = int(self.year_3) + int(self.year_5) + int(self.year_7) + int(self.year_10) + int(self.year_15) + int(self.year_20) + int(self.year_25)
        total = self.incentive_rate * incentives
        self.service_incentive = total

    # @api.one
    def getIncentiveYearsRange(self):
        incentive_length_days = int(abs(((self.incentive_length /SECOND_PER_MINUTE)/MINUTE_PER_HOUR)/HOUR_PER_DAY))

        incentive_in_years = abs(incentive_length_days/YEAR)

        if incentive_in_years >= 3:
            self.year_3 = True
        else:
            self.year_3 = False

        if incentive_in_years >= 3:
            self.year_3 = True
        else:
            self.year_3 = False

        if incentive_in_years >= 5:
            self.year_5 = True
        else:
            self.year_5 = False

        if incentive_in_years >= 7:
            self.year_7 = True
        else:
            self.year_7 = False

        if incentive_in_years >= 10:
            self.year_10 = True
        else:
            self.year_10 = False

        if incentive_in_years >= 15:
            self.year_15 = True
        else:
            self.year_15 = False

        if incentive_in_years >= 20:
            self.year_20 = True
        else:
            self.year_20 = False

        if incentive_in_years >= 25:
            self.year_25 = True
        else:
            self.year_25 = False


    employee_number = fields.Char("Employee Number", readonly=True)
    name = fields.Char("Name", readonly=True)
    employment_rank = fields.Many2one("hr.rank", readonly=True, string="Rank")
    employment_ranktype = fields.Char("Rank Type") #fields.Many2one("hr.rank", readonly=True, string="Rank Type")
    service_length = fields.Char("Service Length", readonly=True, compute = getServiceLength)
    earned_incentive = fields.Char("Earned Incentive", readonly=True, compute = getEarnedIncentive)
    incentive_rate = fields.Float("Incentive Rate",(18,2),  readonly=True)
    year_3 = fields.Boolean('3 Years',  readonly=True, compute = getIncentiveYearsRange)
    year_5 = fields.Boolean('5 Years',  readonly=True, compute = getIncentiveYearsRange)
    year_7 = fields.Boolean('7 Years',  readonly=True, compute = getIncentiveYearsRange)
    year_10 = fields.Boolean('10 Years',  readonly=True, compute = getIncentiveYearsRange)
    year_15 = fields.Boolean('15 Years',  readonly=True, compute = getIncentiveYearsRange)
    year_20 = fields.Boolean('20 Years',  readonly=True, compute = getIncentiveYearsRange)
    year_25 = fields.Boolean('25 Years',  readonly=True, compute = getIncentiveYearsRange)
    service_incentive = fields.Float("Service Incentive(US$)",(18,2),  readonly=True, compute = getserviceincentive)

    employment_status = fields.Many2one("hr.employment.status", readonly=True, string="Status")
    employment_dept_code = fields.Many2one("hr.ship.department", readonly=True, string="Ship Department")
    object_code = fields.Many2one("hr.vessel", readonly=True, string="Vessel")
    date_servicefrom = fields.Date("Service from", readonly=True)
    date_serviceto = fields.Date("Service to", readonly=True)
    date_maxservicefrom = fields.Date("Service from", readonly=True)
    date_maxserviceto = fields.Date("Service to", readonly=True)

    years_of_service = fields.Float("Years of Service",(18,2),  readonly=True)
    days_of_service = fields.Float("Days of Service",(18,2),  readonly=True)
    incentive_length = fields.Float("Incentive Length",(18,2),  readonly=True)


    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'hr_service_record_report')
        self.env.cr.execute("""
                   CREATE OR REPLACE VIEW hr_service_record_report AS (
                            SELECT
                                ID,
                                EMPLOYEE_NUMBER,
                                NAME,
                                EMPLOYMENT_RANK,
                                CODE EMPLOYMENT_RANKTYPE,
                                RATE INCENTIVE_RATE,
                                0 AS SERVICE_LENGHT,
                                0 AS EARNED_INCENTIVE,
                                0 YEAR_3,
                                0 YEAR_5,
                                0 YEAR_7,
                                0 YEAR_10,
                                0 YEAR_15,
                                0 YEAR_20,
                                0 YEAR_25,
                                0 AS SERVICE_INCENTIVE	,
                                EMPLOYMENT_STATUS,
                                EMPLOYMENT_DEPT_CODE,
                                DATE_SERVICEFROM,
                                DATE_SERVICETO,
                                OBJECT_CODE,
                                MAX_SERVICEFROM,
                                MAX_SERVICETO	,
                                ((((SERVICE_LENGTH /60)/60)/24)/30)/365 years_of_service,
                                SERVICE_LENGTH days_of_service,
                                INCENTIVE_LENGTH,
                                SERVICE_LENGTH
                            FROM (
                                SELECT
                                    EMPH.ID AS ID,
                                    EMPLOYEE_NUMBER,
                                    LAST_NAME || ', ' || FIRST_NAME AS NAME,
                                    EMPLOYMENT_RANK,
                                    RANKS.CODE,
                                    RATE,
                                    INCENTIVE_LENGTH,
                                    SERVICE_LENGTH,
                                    EMPLOYMENT_STATUS,
                                    EMPLOYMENT_DEPT_CODE,
                                    DATE_SERVICEFROM,
                                    DATE_SERVICETO,
                                    OBJECT_CODE,
                                    (SELECT MIN(DATE_SERVICEFROM) FROM HR_EMPLOYMENTHISTORY
                                     WHERE EMPLOYEE_EMPLOYMENT_ID = EMP.ID) MAX_SERVICEFROM,
                                    (SELECT MAX(DATE_SERVICETO) FROM HR_EMPLOYMENTHISTORY
                                     WHERE EMPLOYEE_EMPLOYMENT_ID = EMP.ID) MAX_SERVICETO
                                FROM HR_EMPLOYEE EMP
                                INNER JOIN HR_EMPLOYMENTHISTORY EMPH
                                    ON EMP.ID = EMPH.EMPLOYEE_EMPLOYMENT_ID
                                LEFT OUTER JOIN (SELECT CODE,HRT.ID, RATE
                                         FROM  HR_RANK HR,hr_ranktype HRT
                                         WHERE HR.RANK_TYPE = HRT.ID) RANKS
                                    ON EMPLOYMENT_RANK = RANKS.ID) A
                        )
                   """)


class hrFoclServiceBoard(models.Model):
    _name = "hr.focl.record.report"
    _description = 'FOCL Record Report'
    _auto = False

class hrSignOn(models.Model):
    _name = 'hr.signonoff.report'
    _description = 'SignOn Report'
    _auto = False

    employee_number = fields.Char("Employee Number", readonly=True)
    ccl_number = fields.Char("CCL Number", readonly=True)
    employment_rank = fields.Many2one("hr.rank", readonly=True, string="Rank")
    last_name = fields.Char("Last Name", readonly=True)
    first_name = fields.Char("First Name", readonly=True)
    birth_date = fields.Date("Birth Date", readonly=True)
    employment_status = fields.Many2one("hr.employment.status", readonly=True, string="Status")
    date_depart = fields.Date("Depart Date", readonly=True)
    date_servicefrom = fields.Date("Sign On Date", readonly=True)
    date_serviceto = fields.Date("Sign Off Date", readonly=True)
    remarks = fields.Char("Remarks", readonly=True)
    employment_dept_code = fields.Many2one("hr.ship.department", readonly=True, string="Ship Department")
    object_code = fields.Many2one("hr.vessel", readonly=True, string="Vessel")
    remarks = fields.Text('Remarks')
    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'hr_signonoff_report')
        self.env.cr.execute("""
                   CREATE OR REPLACE VIEW hr_signonoff_report AS (
                        SELECT
                            ID,
                            EMPLOYEE_CONTRACT_NUMBER AS EMPLOYEE_NUMBER,
                            CCL_NUMBER,
                            EMPLOYMENT_RANK,
                            LAST_NAME,
                            FIRST_NAME,
                            birthday BIRTH_DATE,
                            EMPLOYMENT_STATUS,
                            DATE_DEPARTURE DATE_DEPART,
                            EMPLOYMENT_DEPT_CODE,
                            DATE_SERVICEFROM,
                            DATE_SERVICETO,
                            OBJECT_CODE,
                            REMARKS
                        FROM (
                            SELECT
                                EMPH.ID AS ID,
                                EMPLOYEE_CONTRACT_NUMBER,
                                CCL_NUMBER,
                                LAST_NAME ,
                                FIRST_NAME,
                                birthday,
                                EMPLOYMENT_RANK,
                                EMPLOYMENT_STATUS,
                                EMPLOYMENT_DEPT_CODE,
                                DATE_DEPARTURE,
                                DATE_SERVICEFROM,
                                DATE_SERVICETO,
                                OBJECT_CODE,
				REMARKS
                            FROM HR_EMPLOYEE EMP
                            INNER JOIN HR_EMPLOYMENTHISTORY EMPH
                                ON EMP.ID = EMPH.EMPLOYEE_EMPLOYMENT_ID) A
                        )
                   """)


class hrDisembarkationReport(models.Model):
    _name = 'hr.disembarkation.report'
    _description = 'Disembarkation Report'
    _auto = False

    # @api.one
    def getPassportNumber(self):
        date = datetime.datetime.strftime(DATE_NOW, "%Y-%m-%d")
        query = SQL_QUERY %{'my_date': date, 'employee_id': self.employee_id, 'my_abbrv': PASSPORT_CODE}
        self.env.cr.execute(query)
        passportInfos = self.env.cr.fetchall()
        if len(passportInfos) > 0:
            self.passport = passportInfos[0][0]
            self.passport_date_issued = passportInfos[0][1]
            self.passport_date_expiry = passportInfos[0][2]

    # @api.one
    def getSsribNumber(self):
        date = datetime.datetime.strftime(DATE_NOW, "%Y-%m-%d")
        query = SQL_QUERY %{'my_date': date, 'employee_id': self.employee_id, 'my_abbrv': SSRIB_CODE}
        self.env.cr.execute(query)
        ssribInfos = self.env.cr.fetchall()
        if len(ssribInfos) > 0:
            self.ssrib = ssribInfos[0][0]
            self.ssrib_date_issued = ssribInfos[0][1]
            self.ssrib_date_expiry = ssribInfos[0][2]


    employee_number = fields.Char("Employee Number", readonly=True)
    ccl_number = fields.Char("CCL Number", readonly=True)
    last_name = fields.Char("Last Name", readonly=True)
    first_name = fields.Char("First Name", readonly=True)
    employment_rank = fields.Many2one("hr.rank", readonly=True, string="Rank")
    country_id = fields.Many2one('res.country', 'Nationality',readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], readonly=True, string ='Gender')
    placeof_birth = fields.Char("Place of Birth", readonly=True)

    passport = fields.Char('Passport', readonly=True, compute =getPassportNumber)
    passport_date_issued = fields.Date('Date issued', readonly=True, compute = getPassportNumber)
    passport_date_expiry = fields.Date('Date expiry', readonly=True, compute = getPassportNumber)

    ssrib = fields.Char('SSIRB', readonly=True, compute=getSsribNumber)
    ssrib_date_issued = fields.Date('Date issued', readonly=True, compute=getSsribNumber)
    ssrib_date_expiry = fields.Date('Date expiry', readonly=True, compute=getSsribNumber)

    place_signoff = fields.Many2one('hr.port', 'Place signoff')

    date_depart = fields.Date("Depart Date", readonly=True)
    date_servicefrom = fields.Date("Sign On Date", readonly=True)
    date_serviceto = fields.Date("Sign Off Date", readonly=True)
    employment_dept_code = fields.Many2one("hr.ship.department", readonly=True, string="Ship Department")
    object_code = fields.Many2one("hr.vessel", readonly=True, string="Vessel")
    employee_id = fields.Integer('Employee ID',readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'hr_disembarkation_report')
        self.env.cr.execute("""
                   CREATE OR REPLACE VIEW hr_disembarkation_report AS (
                        SELECT
                            ID,
                            EMPLOYEE_CONTRACT_NUMBER AS EMPLOYEE_NUMBER,
                            CCL_NUMBER,
                            LAST_NAME,
                            FIRST_NAME,
                            EMPLOYMENT_RANK,
                            COUNTRY_ID,
                            GENDER,
                            PLACEOF_BIRTH,
                            '' PASSPORT_NUMBER,
                            '' PASSPORT_DATE_ISSUED,
                            '' PASSPORT_DATE_EXPIRY,
                            '' SSRIB,
                            '' SSRIB_DATE_ISSUED,
                            '' SSRIB_DATE_EXPIRY,
                            "place_signOff" PLACE_SIGNOFF,
                            DATE_DEPARTURE DATE_DEPART,
                            DATE_SERVICEFROM,
                            DATE_SERVICETO,
                            EMPLOYMENT_DEPT_CODE,
                            OBJECT_CODE,
                            EMPLOYEE_ID
                        FROM (
                            SELECT
                                EMPH.ID AS ID,
                                EMPLOYEE_CONTRACT_NUMBER,
                                CCL_NUMBER,
                                LAST_NAME ,
                                FIRST_NAME,
                                EMPLOYMENT_RANK,
                                EMPLOYMENT_STATUS,
                                EMPLOYMENT_DEPT_CODE,
                                DATE_DEPARTURE,
                                DATE_SERVICEFROM,
                                DATE_SERVICETO,
                                OBJECT_CODE,
                                COUNTRY_ID,
                                GENDER,
                                PLACEOF_BIRTH,
                                "place_signOff",
                                EMP.ID EMPLOYEE_ID
                            FROM HR_EMPLOYEE EMP
                            INNER JOIN HR_EMPLOYMENTHISTORY EMPH
                                ON EMP.ID = EMPH.EMPLOYEE_EMPLOYMENT_ID) A
                        )
                   """)


class hrEmbarkationReport(models.Model):
    _name = 'hr.embarkation.report'
    _description = 'Embarkation Report'
    _auto = False

    # @api.one
    def getPassportNumber(self):
        date = datetime.datetime.strftime(DATE_NOW, "%Y-%m-%d")
        query = SQL_QUERY %{'my_date': date, 'employee_id': self.employee_id, 'my_abbrv': PASSPORT_CODE}
        self.env.cr.execute(query)
        passportInfos = self.env.cr.fetchall()
        if len(passportInfos) > 0:
            self.passport = passportInfos[0][0]
            self.passport_date_issued = passportInfos[0][1]
            self.passport_date_expiry = passportInfos[0][2]

    # @api.one
    def getSsribNumber(self):
        date = datetime.datetime.strftime(DATE_NOW, "%Y-%m-%d")
        query = SQL_QUERY %{'my_date': date, 'employee_id': self.employee_id, 'my_abbrv': SSRIB_CODE}
        self.env.cr.execute(query)
        ssribInfos = self.env.cr.fetchall()
        if len(ssribInfos) > 0:
            self.ssrib = ssribInfos[0][0]
            self.ssrib_date_issued = ssribInfos[0][1]
            self.ssrib_date_expiry = ssribInfos[0][2]

    employee_number = fields.Char("Employee Number", readonly=True)
    ccl_number = fields.Char("CCL Number", readonly=True)
    last_name = fields.Char("Last Name", readonly=True)
    first_name = fields.Char("First Name", readonly=True)
    employment_rank = fields.Many2one("hr.rank", readonly=True, string="Rank")
    country_id = fields.Many2one('res.country', 'Nationality',readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], readonly=True, string ='Gender')
    placeof_birth = fields.Char("Place of Birth", readonly=True)

    passport = fields.Char('Passport', readonly=True, compute =getPassportNumber)
    passport_date_issued = fields.Date('Date issued', readonly=True, compute = getPassportNumber)
    passport_date_expiry = fields.Date('Date expiry', readonly=True, compute = getPassportNumber)

    ssrib = fields.Char('SSIRB', readonly=True, compute=getSsribNumber)
    ssrib_date_issued = fields.Date('Date issued', readonly=True, compute=getSsribNumber)
    ssrib_date_expiry = fields.Date('Date expiry', readonly=True, compute=getSsribNumber)

    place_signon = fields.Many2one('hr.port', 'Place signOn')

    date_depart = fields.Date("Depart Date", readonly=True)
    date_servicefrom = fields.Date("Sign On Date", readonly=True)
    date_serviceto = fields.Date("Sign Off Date", readonly=True)
    employment_dept_code = fields.Many2one("hr.ship.department", readonly=True, string="Ship Department")
    object_code = fields.Many2one("hr.vessel", readonly=True, string="Vessel")
    employee_id = fields.Integer('Employee ID',readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'hr_embarkation_report')
        self.env.cr.execute("""
                   CREATE OR REPLACE VIEW hr_embarkation_report AS (
                        SELECT
                            ID,
                            EMPLOYEE_CONTRACT_NUMBER AS EMPLOYEE_NUMBER,
                            CCL_NUMBER,
                            LAST_NAME,
                            FIRST_NAME,
                            EMPLOYMENT_RANK,
                            COUNTRY_ID,
                            GENDER,
                            PLACEOF_BIRTH,
                            '' PASSPORT_NUMBER,
                            '' PASSPORT_DATE_ISSUED,
                            '' PASSPORT_DATE_EXPIRY,
                            '' SSRIB,
                            '' SSRIB_DATE_ISSUED,
                            '' SSRIB_DATE_EXPIRY,
                            "place_signOn" PLACE_SIGNON,
                            DATE_DEPARTURE DATE_DEPART,
                            DATE_SERVICEFROM,
                            DATE_SERVICETO,
                            EMPLOYMENT_DEPT_CODE,
                            OBJECT_CODE,
                            EMPLOYEE_ID
                        FROM (
                            SELECT
                                EMPH.ID AS ID,
                                EMPLOYEE_CONTRACT_NUMBER,
                                CCL_NUMBER,
                                LAST_NAME ,
                                FIRST_NAME,
                                EMPLOYMENT_RANK,
                                EMPLOYMENT_STATUS,
                                EMPLOYMENT_DEPT_CODE,
                                DATE_DEPARTURE,
                                DATE_SERVICEFROM,
                                DATE_SERVICETO,
                                OBJECT_CODE,
                                COUNTRY_ID,
                                GENDER,
                                PLACEOF_BIRTH,
                                "place_signOn",
                                EMP.ID EMPLOYEE_ID
                            FROM HR_EMPLOYEE EMP
                            INNER JOIN HR_EMPLOYMENTHISTORY EMPH
                                ON EMP.ID = EMPH.EMPLOYEE_EMPLOYMENT_ID) A
                        )
                   """)


class hrBeneficiaryList(models.Model):
    _name = 'hr.beneficiary.report'
    _description = 'Beneficiary Report'
    _auto = False

    # @api.one
    def currentVessel(self):
        date = datetime.datetime.strftime(DATE_NOW, "%Y-%m-%d")
        query = SQL_QUERY_EMPLOYMENT_HISTORY %{'my_date': date, 'employee_id': self.employee_id, 'statusid': ACTIVE_ON_BOARD}
        self.env.cr.execute(query)
        vessel = self.env.cr.fetchall()
        if len(vessel) > 0:
            self.object_code = vessel[0][0]


    employee_number = fields.Char("Employee Number", readonly=True)
    last_name = fields.Char("Last Name", readonly=True)
    first_name = fields.Char("First Name", readonly=True)
    middle_name = fields.Char("Middle Name", readonly=True)
    address_1 = fields.Char("Address 1", readonly=True)
    city = fields.Char('City', readonly=True)
    country_id = fields.Many2one('res.country', 'Country',readonly=True)
    object_code = fields.Many2one("hr.vessel", readonly=True, string="Vessel", compute =currentVessel)
    employee_id = fields.Integer('Employee ID',readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'hr_beneficiary_report')
        self.env.cr.execute("""
                   CREATE OR REPLACE VIEW hr_beneficiary_report AS (
                        SELECT
                            EMF.ID ID,
                            EMP.ID EMPLOYEE_ID,
                            EMPLOYEE_CONTRACT_NUMBER AS EMPLOYEE_NUMBER,
                            EMF.LAST_NAME,
                            EMF.FIRST_NAME,
                            EMF.MIDDLE_NAME,
                            EMF.ADDRESS_1,
                            CITY,
                            EMF.COUNTRY_ID,
                            '' OBJECT_CODE
                        FROM HR_EMPLOYEE EMP, HR_EMPLOYEE_FAMILIES EMF
                        WHERE EMP.ID = EMF.EMPLOYEE_FAMILY_RELATIONSHIP_ID
                        AND IS_LIVING = (1::BOOLEAN)
                        AND IS_BENEFICIARY = (1::BOOLEAN))
                   """)


class hrAllotteeList(models.Model):
    _name = 'hr.allottee.report'
    _description = 'Alottee Report'
    _auto = False

    # @api.one
    def currentVessel(self):
        date = datetime.datetime.strftime(DATE_NOW, "%Y-%m-%d")
        query = SQL_QUERY_EMPLOYMENT_HISTORY %{'my_date': date, 'employee_id': self.employee_id, 'statusid': ACTIVE_ON_BOARD}
        self.env.cr.execute(query)
        vessel = self.env.cr.fetchall()
        if len(vessel) > 0:
            self.object_code = vessel[0][0]

    employee_number = fields.Char("Employee Number", readonly=True)
    last_name = fields.Char("Last Name", readonly=True)
    first_name = fields.Char("First Name", readonly=True)
    middle_name = fields.Char("Middle Name", readonly=True)
    address_1 = fields.Char("Address 1", readonly=True)
    city = fields.Char('City', readonly=True)
    country_id = fields.Many2one('res.country', 'Country',readonly=True)
    object_code = fields.Many2one("hr.vessel", readonly=True, string="Vessel", compute =currentVessel)
    employee_id = fields.Integer('Employee ID',readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'hr_allottee_report')
        self.env.cr.execute("""
                   CREATE OR REPLACE VIEW hr_allottee_report AS (
                        SELECT
                            EMF.ID ID,
                            EMPLOYEE_CONTRACT_NUMBER AS EMPLOYEE_NUMBER,
                            EMP.ID EMPLOYEE_ID,
                            EMF.LAST_NAME,
                            EMF.FIRST_NAME,
                            EMF.MIDDLE_NAME,
                            EMF.ADDRESS_1,
                            CITY,
                            EMF.COUNTRY_ID,
                            '' OBJECT_CODE
                        FROM HR_EMPLOYEE EMP, HR_EMPLOYEE_FAMILIES EMF
                        WHERE EMP.ID = EMF.EMPLOYEE_FAMILY_RELATIONSHIP_ID
                        AND IS_LIVING = (1::BOOLEAN)
                        AND EMF.IS_ALLOTTEE = (1::BOOLEAN)
                        )
                   """)
