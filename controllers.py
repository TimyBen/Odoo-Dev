# -*- coding: utf-8 -*-
from urllib import request
from odoo import http
from odoo.http import request


class RealEstate(http.Controller):
    @http.route('/realestate/estate', auth='public', website=True)
    def real_estate(self, **kw):
        # return "Hello, world"
        sale_order = request.env['sale.order'].sudo().search([])
        print("sale_order-----", sale_order.order_line)
        values = {}
        for sale in sale_order:
            if sale.partner_id not in values:
                values.update({sale.partner_id: sale})
            else:
                values[sale.partner_id] |= sale
        return request.render("estate.estate_page", {
            "values": values,
        })
