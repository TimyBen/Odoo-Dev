from odoo import api, fields, models

# Property tag model
class Property_tag(models.Model):
    _name= "property.tag"
    _description = "Property Tag"
    _order = "name"

    # property tag basic fields
    name = fields.Char(required=True)
    color=fields.Integer()
    
