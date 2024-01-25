 # -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError

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

	@api.onchange('mobile_phone','work_phone')
	def _check_phone_format(self):
		for record in self:
			if record.mobile_phone and not record.mobile_phone.isdigit():
				raise ValidationError("Please enter a valid phone!")
			if record.work_phone and not record.work_phone.isdigit():
				raise ValidationError("Please enter a valid phone!")