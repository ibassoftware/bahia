 # -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResPartner(models.Model):
	_inherit = 'res.partner'

	ean13 = fields.Char()
	image_medium = fields.Binary("Medium-sized image", attachment=True,
		help="Medium-sized image of this contact. It is automatically "\
			 "resized as a 128x128px image, with aspect ratio preserved. "\
			 "Use this field in form views or some kanban views.")
	image_small = fields.Binary("Small-sized image", attachment=True,
		help="Small-sized image of this contact. It is automatically "\
			 "resized as a 64x64px image, with aspect ratio preserved. "\
			 "Use this field anywhere a small image is required.")
