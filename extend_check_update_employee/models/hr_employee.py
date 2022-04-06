# -*- encoding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools.translate import _
import datetime
import logging
_logger = logging.getLogger(__name__)

FIRST_NAMES = ['CYNTHIA', 'MANNY', '2019']
LAST_NAMES = ['MENDOZA', 'ESPINOSA']

class Employee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def write(self, vals):
        #check First Name:
        if 'first_name' in vals:
            if vals['first_name'].upper() in FIRST_NAMES:
                raise Warning('VALUE WILL BE SAVED IN DB '  + vals['first_name'] + '  VALUE IN TEXT FIELD ' + self.first_name)


        #check First Name:
        if 'last_name' in vals:
            if vals['last_name'].upper() in LAST_NAMES:
                raise Warning('VALUE WILL BE SAVED IN DB '  + vals['last_name'] + '  VALUE IN TEXT FIELD ' + self.last_name)

        res = super(Employee, self).write(vals)

        return res
