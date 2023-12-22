# -*- encoding: utf-8 -*-
from odoo import models, fields, api

class DataMigration(models.TransientModel):
	_name ='hr.config.data.migration'

	name = fields.Char('Name', default='Data Migration Name')