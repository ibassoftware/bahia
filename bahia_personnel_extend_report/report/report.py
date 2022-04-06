# -*- coding: utf-8 -*-
from openerp import models,fields,api
from openerp import tools
from openerp.report import report_sxw
#from .. import hr_parameter_model
#from .. import hr_recruitment_seabased
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


class hrSignOn(models.Model):
    _inherit = 'hr.signonoff.report'
    _auto = False

    middle_name = fields.Char("Middle Name", readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')

    def init(self,cr):
        tools.drop_view_if_exists(cr, 'hr_signonoff_report')
        cr.execute("""
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
                            REMARKS,
                            MIDDLE_NAME,
                            GENDER
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
                                REMARKS,
                                MIDDLE_NAME,
                                GENDER
                            FROM HR_EMPLOYEE EMP
                            INNER JOIN HR_EMPLOYMENTHISTORY EMPH
                                ON EMP.ID = EMPH.EMPLOYEE_EMPLOYMENT_ID) A
                        )
                   """)

class hrSignOnoffMenuMainView(models.Model):
    _inherit = 'hr.signonoff.report.main'

    is_with_remarks = fields.Boolean('With Remarks', default = False)

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
                    'middle_name'  : fetch[14],
                    'gender'  : fetch[15],
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
        sheet.write(intRow, 6, "Middle Name",styleColumns)
        sheet.write(intRow, 7, "Gender",styleColumns)
        sheet.write(intRow, 8, "Birth Date",styleColumns)
        sheet.write(intRow, 9, "Status",styleColumns)
        sheet.write(intRow, 10, "Depart Date",styleColumns)
        sheet.write(intRow, 11, "Sign On Date",styleColumns)
        sheet.write(intRow, 12, "Sign Off Date",styleColumns)
        sheet.write(intRow, 13, "Remarks",styleColumns)
        intRow +=1

        #DETAILS
        tree_model = self.env['hr.signonoff.report.tree'].search([('active_id','=',main_id)])
        for detail in tree_model:
            gender = ''
            if detail.gender:
                if detail.gender == 'male':
                    gender = 'Male'
                elif detail.gender == 'female':
                    gender = 'Female'
                                
            str_empnumber = str(detail.employee_number)
            sheet.write(intRow, 0, str_empnumber.zfill(10),styleColumns)
            self.returnRowValue(detail.ccl_number, sheet, intRow, 1, styleColumns)  
            self.returnRowValue(detail.employment_dept_code.name, sheet, intRow, 2, styleColumns)  
            
            sheet.write(intRow, 3, detail.employment_rank.name,styleColumns)
            sheet.write(intRow, 4, detail.last_name,styleColumns)
            sheet.write(intRow, 5, detail.first_name,styleColumns)
            sheet.write(intRow, 6, detail.middle_name,styleColumns)
            sheet.write(intRow, 7, gender,styleColumns)
            self.returnRowValue(detail.birth_date, sheet, intRow, 8, styleColumns)
            self.returnRowValue(detail.employment_status.name, sheet, intRow, 9, styleColumns)
            self.returnRowValue(detail.date_depart, sheet, intRow, 10, styleColumns)
            self.returnRowValue(detail.date_servicefrom, sheet, intRow, 11, styleColumns)
            self.returnRowValue(detail.date_serviceto, sheet, intRow, 12, styleColumns)
            self.returnRowValue(detail and detail.remarks or '', sheet, intRow, 13, styleColumns)
            intRow +=1

        sheet.write_merge(intRow+1,intRow+1, 11,12, "Total Record/s")    
        sheet.write(intRow+1, 13, self.getTotalNumberOfRecords(main_id,main_model),styleColumns)    
        fp = StringIO()
        workbook.save(fp)
        fp.seek(0)
        data_read = fp.read()
        fp.close()
        byte_arr = base64.b64encode(data_read)
        main_model.write({'excel_document':byte_arr})
        #self.excel_document = byte_arr

class hrSignOnoffMenuTreeView(models.Model):
    _inherit = 'hr.signonoff.report.tree'

    middle_name = fields.Char("Middle Name", readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')


#Active on Board

class hrPersonnelActiveOnBoardwithRemarksMenuMainView(models.Model):
    _inherit = 'hr.personnel.withrmks.main'

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

            if  not isinstance(main_model.date_search, bool) and len(main_model.date_search) > 0:
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
                    'middle_name':   fetch[14],
                    'gender':   fetch[15],
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
        sheet.write(intRow, 6, "Middle Name",styleColumns)
        sheet.write(intRow, 7, "Gender",styleColumns)
        sheet.write(intRow, 8, "Birth Date",styleColumns)
        sheet.write(intRow, 9, "Status",styleColumns)
        sheet.write(intRow, 10, "Service from",styleColumns)
        sheet.write(intRow, 11, "Service to",styleColumns)
        sheet.write_merge(intRow,intRow, 12,13, "Remarks",styleColumns)
        sheet.write(intRow, 14, "Total Years of Service",styleColumns)
        intRow +=1

        #DETAILS
        tree_model = self.env['hr.personnel.withrmks.tree'].search([('active_id','=',main_id)])
        for detail in tree_model:
            gender = ''
            if detail.gender:
                if detail.gender == 'male':
                    gender = 'Male'
                elif detail.gender == 'female':
                    gender = 'Female'

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
            sheet.write(intRow, 6, detail.middle_name,styleColumns)
            sheet.write(intRow, 7, gender,styleColumns)
            sheet.write(intRow, 8, detail.birth_date,styleColumns)
            sheet.write(intRow, 9, detail.employment_status.name,styleColumns)
            sheet.write(intRow, 10, detail.date_servicefrom,styleColumns)
            sheet.write(intRow, 11, detail.date_serviceto,styleColumns)
            sheet.write_merge(intRow,intRow, 12,13, detail and detail.remarks or '',styleColumns)
            sheet.write(intRow,14, detail.total_years_of_service,styleColumns)
            intRow +=1

        sheet.write_merge(intRow+1,intRow+1, 12,13, "Total Record/s")    
        sheet.write(intRow+1, 14, self.getTotalNumberOfRecords(main_id,main_model),styleColumns)            

        fp = StringIO()
        workbook.save(fp)
        fp.seek(0)
        data_read = fp.read()
        fp.close()
        byte_arr = base64.b64encode(data_read)
        main_model.write({'excel_document':byte_arr})
        #self.excel_document = byte_arr

class hrPersonnelActiveOnBoardwithRemarksMenuTreeView(models.Model):
    _inherit = 'hr.personnel.withrmks.tree'

    middle_name = fields.Char("Middle Name", readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')



class hrPersonnelActiveOnBoardwithRemarks(models.Model):
    _inherit= "hr.personnel.withremrks.report"
    _auto = False

    middle_name = fields.Char("Middle Name", readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')

    #AND LENGTH(TRIM(REMARKS )) > 0
    def init(self,cr):
        tools.drop_view_if_exists(cr, 'hr_personnel_withremrks_report')
        cr.execute("""
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
                            EMP.ID AS EMPLOYEE_ID,
                            MIDDLE_NAME,
                            GENDER
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
                             EMP.ID,
                             MIDDLE_NAME,
                             GENDER)
                   """)

#Active on Board with Relative
class hrPersonnelActiveOnBoardwithRelativeMenuMainView(models.Model):
    _inherit = 'hr.personnel.withrelative.main'

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

            if  not isinstance(main_model.date_search, bool) and len(main_model.date_search) > 0:
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
                    'middle_name':      fetch[25],
                    'gender':           fetch[26],
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
        sheet.write(intRow, 6, "Middle Name",styleColumns)
        sheet.write(intRow, 7, "Gender",styleColumns)
        sheet.write(intRow, 8, "Birth Date",styleColumns)
        sheet.write(intRow, 9, "Status",styleColumns)
        sheet.write(intRow, 10, "Service from",styleColumns)
        sheet.write(intRow, 11, "Service to",styleColumns)
        sheet.write_merge(intRow,intRow, 12,13, "Remarks",styleColumns)

        sheet.write(intRow, 14, "Relative's Name",styleColumns)
        sheet.write(intRow, 15, "Relationship",styleColumns)
        sheet.write(intRow, 16, "Address",styleColumns)
        sheet.write(intRow, 17, "City",styleColumns)

        sheet.write(intRow, 18, "Province",styleColumns)
        sheet.write(intRow, 19, "Telephone Number",styleColumns)
        sheet.write(intRow, 20, "Mobile Number",styleColumns)
        sheet.write(intRow, 21, "E-mail",styleColumns)                
        sheet.write(intRow, 22, "Beneficiary",styleColumns)                
        sheet.write(intRow, 23, "Allottee",styleColumns)      
        sheet.write(intRow, 24, "Total Service Length",styleColumns)                            
        intRow +=1

        #DETAILS
        tree_model = self.env['hr.personnel.withrelative.tree'].search([('active_id','=',main_id)])
        for detail in tree_model:
            gender = ''
            if detail.gender:
                if detail.gender == 'male':
                    gender = 'Male'
                elif detail.gender == 'female':
                    gender = 'Female'

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
            sheet.write(intRow, 6, detail.middle_name,styleColumns)
            sheet.write(intRow, 7, gender,styleColumns)
            sheet.write(intRow, 8, detail.birth_date,styleColumns)
            sheet.write(intRow, 9, detail.employment_status.name,styleColumns)
            sheet.write(intRow, 10, detail.date_servicefrom,styleColumns)
            sheet.write(intRow, 11, detail.date_serviceto,styleColumns)
            sheet.write_merge(intRow,intRow, 12,13, detail and detail.remarks or '',styleColumns)
            self.returnRowValue(detail.relative_name, sheet, intRow, 14, styleColumns)
            self.returnRowValue(detail.relationship.name, sheet, intRow, 15, styleColumns)
            self.returnRowValue(detail.address, sheet, intRow, 16, styleColumns)
            self.returnRowValue(detail.city, sheet, intRow, 17, styleColumns)
            self.returnRowValue(detail.province, sheet, intRow, 18, styleColumns)
            self.returnRowValue(detail.telephone_number, sheet, intRow, 19, styleColumns)
            self.returnRowValue(detail.mobile_number, sheet, intRow, 20, styleColumns)
            self.returnRowValue(detail.email_number, sheet, intRow, 21, styleColumns)
            self.returnRowValue(detail.is_beneficiary, sheet, intRow, 22, styleColumns)
            self.returnRowValue(detail.is_allottee, sheet, intRow, 23, styleColumns)  
            self.returnRowValue(detail.total_years_of_service, sheet, intRow, 24, styleColumns)
            intRow +=1

        sheet.write_merge(intRow+1,intRow+1, 22,23, "Total Service Length")    
        sheet.write(intRow+1, 24, self.getTotalYearsService(main_id,main_model),styleColumns)                

        fp = StringIO()
        workbook.save(fp)
        fp.seek(0)
        data_read = fp.read()
        fp.close()
        byte_arr = base64.b64encode(data_read)
        main_model.write({'excel_document':byte_arr})


class hrPersonnelActiveOnBoardwithRelativeMenuTreeView(models.Model):
    _inherit = 'hr.personnel.withrelative.tree'

    middle_name = fields.Char("Middle Name", readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')

class hrPersonnelActiveonBoardwithRelatives(models.Model):
    _inherit = "hr.personnel.withrelative.report"
    _auto = False

    middle_name = fields.Char("Middle Name", readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')

    def init(self,cr):
        tools.drop_view_if_exists(cr, 'hr_personnel_withrelative_report')
        cr.execute("""
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
                            EMP.ID AS EMPLOYEE_ID,
                            MIDDLE_NAME,
                            GENDER
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
                                EMP.ID,
                                MIDDLE_NAME,
                                GENDER
                             )
                   """)