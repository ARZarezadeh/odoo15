from odoo import models, fields


class FoodProduct(models.Model):
    _name = "food.product"
    _description = "Food Product"

    name = fields.Char(required=True)
    food_type = fields.Selection(
        string='Food Type',
        selection=[('khorak', 'Khorak'), ('polo', 'Polo')],
        required=True,
    )

    day_ids = fields.Many2many(
        'food.day', 'product_day_rel', 'product_id', 'day_id', string="days of this food")

    order_ids = fields.One2many('food.order', 'food_id')

    # ----------------- CONSTRAINTS --------------------#
