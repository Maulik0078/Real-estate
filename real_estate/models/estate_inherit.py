from odoo import fields, models

class InheritedModel(models.Model):
    _inherit = "res.users"
    
    custom_field = fields.Char(string="Custom Field")
    propertytype_ids = fields.One2many('estate.model','salesman_id',string='Property Types')
    