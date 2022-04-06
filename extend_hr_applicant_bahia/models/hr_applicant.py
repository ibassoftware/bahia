# -*- encoding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools.translate import _

class ExtendHrApplicant(models.Model):
    _inherit = 'hr.applicant'

    def create(self, cr, uid, vals, context=None):
        context = dict(context or {})
        context['mail_create_nolog'] = False

        obj_id = super(ExtendHrApplicant, self).create(cr, uid, vals, context=context)

        applicant_obj = self.browse(cr, uid, [obj_id], context)
        if applicant_obj.stage_id.id == 1: #vals.get('stage_id'):
            stage = self.pool['hr.recruitment.stage'].browse(cr, uid, [applicant_obj.stage_id.id], context=context)
            if stage.template_id:
                compose_ctx = dict(context,
                                   active_id=False,
                                   active_ids=[obj_id])
                compose_id = self.pool['mail.compose.message'].create(
                    cr, uid, {
                        'model': self._name,
                        'composition_mode': 'mass_mail',
                        'template_id': stage.template_id.id,
                        'post': True,
                        'notify': True,
                    }, context=compose_ctx)
                values = self.pool['mail.compose.message'].onchange_template_id(
                    cr, uid, [compose_id], stage.template_id.id, 'mass_mail', self._name, False, context=compose_ctx)['value']
                if values.get('attachment_ids'):
                    values['attachment_ids'] = [(6, 0, values['attachment_ids'])]
                self.pool['mail.compose.message'].write(
                    cr, uid, [compose_id],
                    values,
                    context=compose_ctx)
                self.pool['mail.compose.message'].send_mail(cr, uid, [compose_id], context=compose_ctx)        
        return obj_id