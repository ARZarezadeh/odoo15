import datetime
from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError


class FoodDay(models.Model):
    _name = "food.day"
    _description = "Food Day"
    _order = "day"

    name = fields.Char(compute='_compute_name')
    day = fields.Date(required=True, string='Day',
                      default=fields.Date.context_today)
    food_ids = fields.Many2many(
        'food.product', 'product_day_rel', 'day_id', 'product_id', string="today's Foods")
    food_ids_count = fields.Integer(
        compute="_compute_food_ids_count", store=True, default=0)
    week_id = fields.Many2one('food.week', "Week")
    order_ids = fields.One2many('food.order', 'day_id')
    khorak_orders_count = fields.Integer(
        compute="_compute_khorak_orders_count")

    polo_orders_count = fields.Integer(
        compute="_compute_polo_orders_count")

    # ----------------- CONSTRAINTS --------------------#

    _sql_constraints = [
        ('day_unique', 'unique (day)', 'The day already exists!'),
    ]

    # ----------------- APIS --------------------#

    @api.depends('day')
    def _compute_name(self):
        for record in self:
            if record.day:
                record.name = record.day.strftime('%Y-%m-%d_%A')
            else:
                record.name = datetime.datetime.now().strftime('%Y-%m-%d_%A')

    @api.onchange('food_ids')
    def _compute_food_ids_count(self):
        for record in self:
            khoresht_count = len(
                list(filter(lambda food: food.food_type == 'khorak', record.food_ids)))
            polo_count = len(
                list(filter(lambda food: food.food_type == 'polo', record.food_ids)))
            print("____these are khoresht and polo count; ",
                  khoresht_count, polo_count)
            if (khoresht_count > 1 or polo_count > 1):
                raise UserError(
                    'you only can select one food from every type.')
            if len(record.food_ids) > 2:
                raise ValidationError("you can't order more than 2")
            record.food_ids_count = len(
                record.food_ids) if record.food_ids else 0

    @api.depends('order_ids')
    def _compute_khorak_orders_count(self):
        for record in self:
            if record.order_ids:
                print('orderds exist. compute khorak counts...',
                      len(record.order_ids), record.order_ids[0].food_id.food_type)
                khorak_count = 0
                for order in record.order_ids:
                    if order.food_id.food_type == 'khorak':
                        khorak_count += 1
                print("final khorak count: ", khorak_count)
                record.khorak_orders_count = khorak_count
            else:
                record.khorak_orders_count = 0

    @api.depends('order_ids')
    def _compute_polo_orders_count(self):
        for record in self:
            if record.order_ids:
                print('orderds exist. compute polo counts...',
                      len(record.order_ids), record.order_ids[0].food_id.food_type)
                polo_count = 0
                for order in record.order_ids:
                    if order.food_id.food_type == 'polo':
                        polo_count += 1
                record.polo_orders_count = polo_count
            else:
                record.polo_orders_count = 0
