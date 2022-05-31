 # -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResourceResource(models.Model):
	_inherit = 'resource.resource'

	code = fields.Char()