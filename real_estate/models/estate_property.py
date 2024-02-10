from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Estateproperty(models.Model):
	_name = "estate.model"
	_description = "Estate Property Model"
	_rec_name = "name"

	name = fields.Char('Name', required=True)
	description = fields.Text('Description')
	postcode = fields.Char('Postcode')
	date_availability = fields.Datetime('Date Availability', 
		default  = datetime.now() + relativedelta(months=3), copy=False)
	expected_price = fields.Float('Expected Price', required=True)
	selling_price = fields.Float('Selling Price', readonly=False, copy=False)
	bedrooms = fields.Integer('Bedrooms', default=2)
	living_area = fields.Integer('Living Area')
	facades = fields.Integer('Facades')
	garage = fields.Boolean('Garage')
	garage_area = fields.Integer('Garage_area')
	garden = fields.Boolean('Garden')
	garden_area = fields.Integer('Garden_area')
	garden_orientation = fields.Selection([
		('north', 'North'), ('east', 'East'),
		('south', 'South'), ('west', 'west')],
		string='Garden Orientation')
	active = fields.Boolean('active', default=True)
	state = fields.Selection([
		('new', 'New'),
		('offer received', 'Offer Received'),
		('offer accepted', 'Offer Accepted'),
		('sold', 'Sold'),('canceled','Canceled')
		], 
	   string='State', default='new')
	buyer_id = fields.Many2one('res.partner',string="Buyer")	
	salesman_id	 = fields.Many2one('res.users',string="Sales Man")
	tags_ids = fields.Many2many('propertytags.model', string="Tags")
	property_type_id = fields.Many2one('propertytypes.model', String="Property Type Id")
	offer_ids = fields.One2many('offer.model', 'property_id', 
		string="Property")
	total_area = fields.Float('Total Area', compute="_compute_total")
	best_price = fields.Float('Best Price', compute="_mapping")
	sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
	# reference_1 = fields.Reference(
        # [('res.partner', 'Partner'), ('res.users', 'User')], string='Reference One')

	def action_new(self):
		self.state = 'new'
	def action_offer_received(self):
		self.state = 'offer received'
	def action_offer_accepted(self):
		self.state = 'offer accepted'
	def action_sold(self):
		self.state = 'sold'
	def action_canceled(self):
		self.state = 'canceled'

	@api.model
	def _test_cron(self):
	    sold_properties = self.env['estate.model'].search([('state', '=', 'sold')])
	    user_sudo = self.env.user.sudo()
	    
	    for property in sold_properties:
	        template = self.env.ref('ab.estate_happy_email', raise_if_not_found=False)
	        if template:
	            template.sudo().send_mail(user_sudo.id, force_send=True)
	    print("Emails sent successfully for sold properties.")
	    return "Emails sent successfully for sold properties."



	@api.onchange('garden')
	def onchange_gardern(self):
		if not self.garden:
			self.garden_area = 0
			self.garden_orientation = ''
		else:
			self.garden_area = 1000
			self.garden_orientation = 'north'

	@api.onchange('garage')
	def onchange_garage(self):
		if not self.garage:
			self.garage_area = 0
		else:
			self.garage_area = 1000


	@api.depends('living_area', 'garden_area', 'garden', 'garage', 'garage_area')
	def _compute_total(self):
		for record in self:
			total_area = record.living_area
			if record.garden:
				total_area += record.garden_area
			if record.garage:
				total_area += record.garage_area
			record.total_area = total_area 

	@api.depends('offer_ids.price')
	def _mapping(self):
		for record in self:
			values = record.offer_ids.mapped('price')
			if values:
				record.best_price = max(values)
			else:
				record.best_price = 0


	@api.model
	def ondelete(self, vals):
		if vals.get('property_id'):
			property_id = self.env['propertytypes.model'].browse(vals['property_id'])
			property_id.state = 'offer_received'

			existing_offers = self.search([('property_id', '=', property_id.id)])
			for offer in existing_offers:
				if vals.get('price') and vals['price'] < offer.price:
					raise exceptions.UserError("You cannot create an offer with a lower amount than an existing offer.")
		return super(offer, self).create(vals)

	@api.constrains('expected_price')
	def _check_expected_price_positive(self):
		for record in self:
			if record.expected_price < 0:
				raise ValidationError("Selling price must be positive.")

	@api.constrains('selling_price')
	def _check_selling_price_positive(self):
		for record in self:
			if record.selling_price < 0:
				raise ValidationError("Selling price must be positive.")
			if record.selling_price < (0.9 * record.expected_price):
				raise ValidationError("Selling price cannot be lower than 90(percent) of the expected price.")

	
	def unlink(self):
		for estate_property_types in self:
			if estate_property_types.state not in ['new', 'canceled']:
				raise exceptions.ValidationError("You can't delete a property that is not in 'New' or 'Canceled' state.")
		return super(Estateproperty, self).unlink()

	
	_sql_constraints = [
		('unique_property_title', 'UNIQUE(title)', 'Property title must be unique.'),
	]


