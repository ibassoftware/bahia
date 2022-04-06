# -*- coding: utf-8 -*-
from openerp import models,fields,api
from openerp import tools
from openerp.report import report_sxw
import datetime
import base64
from openerp.exceptions import except_orm, Warning, RedirectWarning,ValidationError


DATE_NOW = datetime.datetime.now()


class print_reception_report(models.TransientModel):
    _name = 'print.reception.report'
    _description = 'Print Reception Report'

    date_from = fields.Date('Date From', required=True, default = DATE_NOW)
    date_to = fields.Date('Date To', required=True, default = DATE_NOW)
    @api.multi
    def print_checks(self):
    	#raise Warning("You've done quite annoying!!")
        reception_model = self.env['hr.reception']#.browse(self.env.context['payment_ids'])
        #for payment in payments:
        #    payment.check_number = check_number
        #    check_number += 1
        return reception_model.generateExcelReport(self.date_from, self.date_from)