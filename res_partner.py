from odoo import api, fields, models


class InheritResUser(models.Model):
    _inherit = "res.partner"

    property_ids = fields.One2many('real.estate', 'buyer_id', string='Offer')
    property_acct = fields.Integer(compute='_compute_offer_accepted_count')

    @api.depends('property_ids')
    def _compute_offer_accepted_count(self):
        for record in self:
            record.property_acct = len(record.property_ids)

    def open_property_offer_action(self):
        return {
            'name': "Offers",
            'type': 'ir.actions.act_window',
            'view_type': 'list,form',
            'view_mode': 'list',
            'res_model': 'real.estate',
            'target': 'current',
            'domain': [('id', 'in', self.property_ids.ids)]
        }