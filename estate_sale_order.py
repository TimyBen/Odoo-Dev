from odoo import api,fields,models


# class sales_order(models.Model):
#     _inherit = "real.estate"

#     def sale_order(self):
#         res = super(sales_order, self).sold_button()
#         sale_order = self.filtered(lambda x: x.state == 'sold')
 
#         for sale in sale_order:
#             self.env['sale.order.line'].create({
#                 'product_id': sale.name,
#                 'price_unit': sale.selling_price,
#                 'product_uom_qty': 1,
#                 'order_id': self.id
#                 ]
#             })
#         return res
