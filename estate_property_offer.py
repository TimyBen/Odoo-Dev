from datetime import date, datetime
from email.policy import default
from odoo import api, fields, models
# from datetime import datetime
from datetime import timedelta
from odoo.exceptions import ValidationError

#Property offer model
class Property_offers(models.Model):
    _name= "property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner",  string="Partner")
    property_id = fields.Many2one('real.estate')
    validity = fields.Integer()
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', readonly=False)

    # function to calculate date depending on validity value
    @api.depends('validity')
    def _compute_date_deadline(self):
        today = fields.Date.today()
        for line in self:
            date = False
            if line.validity:
                date = today + timedelta(days=line.validity)
            line.date_deadline = date

    # inverse function to calculate vaidity based on selected date 
    def _inverse_date_deadline(self):
        today = fields.Date.today()
        for line in self:
            validity = False
            if line.date_deadline:
                delta = line.date_deadline - today
                validity = delta.days
            line.validity = validity

    # function accepet offer button
    def accept_button(self):
        for record in self:
            record.write({'status': "accepted"})
            record.property_id.write({'buyer_id': record.partner_id.id, 'state': 'offer_accepted', 'selling_price': record.price})
            # record.property_id.activity_schedule(act_type_xmlid='oe_chatter',
            #     date_deadline=datetime.now() + timedelta(record.validity), summary='Hello', 
            #     note='offer has been accepted, and an activity have been scheduled')

    # function refuse offer button
    def refuse_button(self):
        for record in self:
            record.write({'status': "refused"})

    # function restrict entering value less than expected price for offer
    @api.constrains('price')
    def _check_offer_price(self):  
        for record in self:
            if record.price < record.property_id.expected_price:
                raise ValidationError("The offer price must be larger than expected price %s!!!" % record.property_id.expected_price)

    def create(self, vals):
        res = super(Property_offers, self).create(vals)
        for record in res:
            record.property_id.activity_schedule(
                'mail.mail_activity_data_todo',
                user_id=record.property_id.sales_man.id,
                date_deadline=datetime.now() + timedelta(record.validity), summary='Hello', 
                note='offer has been create, and an activity have been scheduled')
        return res
        