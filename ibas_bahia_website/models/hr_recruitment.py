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
