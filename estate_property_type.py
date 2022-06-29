from odoo import api, fields, models
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# Property Type model
class Property(models.Model):
    _name= "property.type"
    _description = "Property Type"
    _order = "name"

    # Property type basic field table
    name = fields.Char(required=True)
    title = fields.Char()
    property_ids = fields.One2many('real.estate','property_type_id')

# Inheritance from Real Estate model
class RealEstate(models.Model):
    _inherit = "real.estate"

    user_id = fields.Many2one('res.partner')

    @api.ondelete(at_uninstall=False)
    def _unlink(self):
        if any(record.state not in ('new', 'cancel') for record in self):
            raise UserError("Can't delete selected data!")


# class InheritResUser(models.Model):
#     _inherit= "res.partner"

#     property_ids = fields.One2many('real.estate', 'buyer_id', string='Offer')
#     property_acct= fields.Integer(compute='_compute_offer_accepted_count')

#     @api.depends('property_ids')
#     def _compute_offer_accepted_count(self):
#         for record in self:
#             record.property_acct=len(record.property_ids)


