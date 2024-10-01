from odoo import api, models, fields


class FoodOrder(models.Model):
    _name = 'food.order'
    _description = 'Food Order'

    name = fields.Char(compute="_compute_name")
    week_id = fields.Many2one("food.week", string="Week")
    # day = fields.Many2one("food.day", string="Day")
    day_id = fields.Many2one(
        "food.day", string="Day")
    food_id = fields.Many2one("food.product", string="Foods")

    # ----------------- APIS --------------------#

    @api.depends('week_id', 'food_id')
    def _compute_name(self):
        for record in self:
            record.name = F"{record.day_id.name}_{record.food_id.name}" if (
                record.week_id and record.food_id) else False

    @api.onchange('week_id')
    def onchange_week_id(self):
        if self.week_id:
            return {'domain': {'day_id': [('day', '<=', self.week_id.end_date), ('day', '>=', self.week_id.start_date)]}}
        else:
            return {'domain': {'day_id': []}}

    @api.onchange('day_id')
    def onchange_day_id(self):
        if self.day_id and (not self.week_id):
            domain = [('start_date', '<=', self.day_id.day),
                      ('end_date', '>=', self.day_id.day)]
            self.week_id = False
            return {'domain': {'week_id': domain}}
        else:
            return {'domain': {'week_id': []}}

    @api.onchange('day_id')
    def onchange_day_id_food(self):
        if self.day_id:
            domain = [('day_ids', 'in', [self.day_id.id])]
            self.food_id = False
            return {'domain': {'food_id': domain}}
        else:
            return {'domain': {'food_id': []}}
