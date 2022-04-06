from openerp import models, fields


class HrEmployeeExtend(models.Model):
    _name ='hr.employee'
    _inherit = ['hr.employee']