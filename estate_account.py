from email import message
from unicodedata import name
from odoo import api,fields,models
import logging
_logger=logging.getLogger(__name__)


# Inheritance class Real Estate for invoicing
class InheritedModel(models.Model):
    _inherit = "real.estate"

    # function to create invoice for sold property
    def sold_button(self):
        res = super(InheritedModel, self).sold_button()
        display_msg = 'property has been sold :)'
        offers = self.filtered(lambda x: x.state == 'sold') 
        for offer in offers:
            account_move = self.env['account.move'].create({
                "partner_id": offer.buyer_id,
                "move_type": "out_invoice",
                "journal_id": self.env['account.journal'].search([('code', '=', 'INV')], limit=1).id,
                "invoice_line_ids": [
                    fields.Command.create({
                        "name": offer.name,
                        "quantity": 1,
                        "price_unit": offer.selling_price,
                    })
                ],
                
            })
            offer.buyer_id.message_post(body=display_msg)
            account_move.action_post()
            
            # _logger.warn('Property is stolen :)))')
        return res
    

