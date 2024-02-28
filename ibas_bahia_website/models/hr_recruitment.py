# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from werkzeug import urls

from odoo import api, fields, models, _
from odoo.tools.translate import html_translate

class Job(models.Model):
    _inherit = 'hr.job'

    def _get_default_website_description(self):
        res = super(Job,self)._get_default_website_description()
        default_description = self.env.ref("ibas_bahia_website.default_website_description", raise_if_not_found=False)
        return (default_description._render() if default_description else "")


    website_description = fields.Html('Website description', translate=html_translate, sanitize_attributes=False, default=_get_default_website_description, prefetch=False, sanitize_form=False)

class HRApplicant(models.Model):
    _inherit = 'hr.applicant'

    is_created_website = fields.Boolean(string="Is Created From Website?")

    @api.model_create_multi
    def create(self, vals_list):
        applicants = super().create(vals_list)
        for applicant in applicants:
            if applicant.is_created_website:
                template_id = self.env['ir.model.data']._xmlid_to_res_id('hr_recruitment.email_template_data_applicant_congratulations')
                applicant.message_post_with_template(template_id, **{
                    'auto_delete_message': True,
                    'subtype_id': self.env['ir.model.data']._xmlid_to_res_id('mail.mt_note'),
                    'email_layout_xmlid': 'mail.mail_notification_light'
                })
        return applicants