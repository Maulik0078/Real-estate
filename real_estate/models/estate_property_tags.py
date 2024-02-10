from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EstatePropertytags(models.Model):
	_name = "propertytags.model"
	_description = "Property Tags Model"
	_rec_name = "name"
	_order = "name"

	name = fields.Char("Name", required=True)
	color = fields.Integer("Color")

	_sql_constraints = [
		('name_unique', 'unique(name)', 'Property tag name must be unique!'),
	]

# 	@api.model
# 	def default_get(self, field_list):
# 		#         print ("\n field list >>>>>>>>",field_list)
# 		res = super(EstatePropertytags, self).default_get(field_list)
# #         print ("\n res >>>>>>>>>>",res)
# 		# currency = self.env['res.currency'].search([('name', '=', 'INR')])
# #         print ("\n cureency >>>>>>>",currency)
# 		res.update({'color': 123,
# 					})
# 		return res