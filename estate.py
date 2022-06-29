# from unicodedata import name
from email.policy import default
from odoo import api, fields, models
from odoo.tools import float_compare
from odoo.exceptions import ValidationError
from datetime import timedelta

#Define real estate module
class RealEstate(models.Model):
    _name = "real.estate"
    _description = "Real Estate"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    #basic field for real estate Table
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[(
        'north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    property_type_id = fields.Many2one("property.type")
    sales_man = fields.Many2one("res.users", required=True)
    buyer_id = fields.Many2one("res.partner",  string="Buyer")
    offer_ids = fields.One2many('property.offer', 'property_id')
    property_tag_ids = fields.Many2many("property.tag", string="Tag")
    total_area = fields.Integer(compute="_compute_total")
    amount = fields.Float()
    best_offer = fields.Float(compute="_compute_best_offer")
    state = fields.Selection(group_expand='_expand_states', selection=[('new', 'New'), ('offer_recieved', 'Offer Recieved'), ('offer_accepted', 'Offer Accepted'),('sold', 'Sold'), ('cancel', 'Cancel')], default='new')
    status = fields.Char(compute="_compute_status")
    sequence = fields.Integer('Sequence')
    

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    # compute function to calculate a property total area
    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    # compute function to calculate the best offer for a property
    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            max_price = 0
            for offer in record.offer_ids:
                max_price = offer.price if offer.price > max_price else max_price
            record.best_offer = max_price
            # offers = record.offer_ids.mapped('price')
            # record.best_offer=max(offers)

    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = False
            self.garden_orientation = False

    # change the state of a property when state is sold
    def sold_button(self):
        for record in self:
            record.write({'state': "sold"})
            record.state='sold'
    
    # change the state of a property when state is canceld
    def cancel_button(self):
        for record in self:
            record.write({'state': "cancel"})
            # record.state = 'cancel'

    # function changing the status of a property depending on the state of a property
    @api.depends("state")
    def _compute_status(self):
        for record in self:
            if record.state == 'sold':
                record.status = "Sold"
            elif record.state == 'cancel':
                record.status = "Canceled"
            elif record.state == 'offer_accepted':
                record.status = "Offer Accepted"
            else:
                record.status = "Available"

    # function to restrict entering a negative value for field(expected_price)
    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price < 0:
                raise ValidationError("Expected price cannot be negative")
    
    # function to restrict entering a negative value for field(selling_price)
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError("Selling price cannot be negative")
        
    # function to restrict entering a value 90% less for field(selling_price)
    @api.constrains('selling_price', 'expected_price')
    def _check_percent(self):
        for record in self:
            temp_price = record.expected_price * 90 / 100
            if record.selling_price < temp_price:
                raise ValidationError('Selling price cannot be 90 precent less')

