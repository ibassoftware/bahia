 # -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResCountry(models.Model):
	_inherit = 'res.country'

	active = fields.Boolean(default=True)