from odoo import api, fields, models
from datetime import timedelta

class EstateOffer(models.Model):
	_name = "offer.model"
	_description = "Offer Model"
	_order = "price desc"
	

	price = fields.Float(string="Price")
	state = fields.Selection(selection=[
			("accept","Accepted"),("refuse","Refused"),
			],
			string="Status", copy=False)
	partner_id = fields.Many2one('res.partner')
	property_id = fields.Many2one('estate.model', string="Property")
	validity = fields.Integer(string="Validity", default=7)
	date_deadline = fields.Datetime(string="Date Deadline", compute='_compute_validity',store=True, readonly=False)
	property_type_id = fields.Many2one('estate.model', string='Property Type')

	

	def action_accept(self):
		for record in self:
			record.state = 'accept'
			record.property_id.state = 'offer accepted'
			record.property_id.buyer_id = record.partner_id.id
			record.property_id.best_price = record.price
			record.property_id.selling_price = record.price

	def action_refuse(self):
		self.state = 'refuse'
		self.property_id.state = 'offer received'



	@api.depends('validity')
	def _compute_validity(self):
		for offer in self:
			if offer.validity:
				date_deadline = fields.datetime.now() + timedelta(days=offer.validity)
				offer.date_deadline = date_deadline

	def write(self, vals):
		if 'validity' in vals:
			vals.pop('validity')
		return super(EstateOffer, self).write(vals)   

	@api.constrains('price')
	def _check_price_positive(self):
		for record in self:
			if record.price < 0:
				raise ValidationError("Selling price must be positive.")


	