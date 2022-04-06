from openerp import models, fields,api

class ir_attachment_Class(models.Model):
    _inherit = 'ir.attachment'

    @api.v8
    def read(self, fields=None, load='_classic_read'):
        super(ir_attachment_Class, self).sudo().read(fields,Load)    