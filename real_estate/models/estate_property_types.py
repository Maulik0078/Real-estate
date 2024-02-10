from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyTypes(models.Model):
    _name = "propertytypes.model"
    _description = "Estate Property Type Model"
    _rec_name = "name"

    name = fields.Char('Name', required=True)
    line_ids = fields.One2many("estate.model", "property_type_id")
    offer_count = fields.Integer(compute='_compute_offer_count', string='Offer Count')


    
    @api.depends('line_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = record.env['offer.model'].search_count([('property_id.property_type_id', '=', record.id)])
            

