from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(required=True)

    sequence = fields.Integer('Sequence', default=1,
                              help="Used to order stages. Lower is better.")

    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string='properties')

    offer_ids = fields.One2many(
        'estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(
        compute='_compute_offer_count')

    # ? --------------------------- CONSTRAINTS  -------------------------------------------------
    _sql_constraints = [
        ('name_unique', 'unique (name)', 'Property Type Name Should Be Unique')
    ]

    # ? --------------------------- APIS  -------------------------------------------------

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
