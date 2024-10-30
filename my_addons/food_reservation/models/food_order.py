from odoo import api, models, fields
from odoo.exceptions import ValidationError


class FoodOrder(models.Model):
    _name = 'food.order'
    _description = 'Food Order'
    _order = "day_id"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(compute="_compute_name")
    week_id = fields.Many2one("food.week", string="Week")
    # day = fields.Many2one("food.day", string="Day")
    day_id = fields.Many2one(
        "food.day", string="Day", store=True, tracking=True)
    food_id = fields.Many2one(
        "food.product", string="Foods", store=True, tracking=True)

    user_id = fields.Many2one(
        'res.users', string='orderer', default=lambda self: self.env.user, store=True)
    user_image = fields.Binary(
        related='user_id.image_128', string="User  Image", store=True)

    attachment_ids = fields.Many2many('ir.attachment',
                                      compute='_compute_attachments',
                                      inverse='_inverse_attachments'
                                      )
    # ----------------- CONSTRAINTS --------------------#

    @api.constrains('day_id', 'user_id')
    def _check_unique_order_per_day(self):
        for record in self:
            if self.search_count([('day_id', '=', record.day_id.id), ('user_id', '=', record.user_id.id)]) > 1:
                raise ValidationError(
                    'You cannot create more than one food order per day!')

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

    @api.onchange('message_attachment_count')
    def _compute_attachments(self):
        for record in self:
            attachment_ids = self.env['ir.attachment'].search([
                ('res_model', '=', self._name),
                ('res_id', '=', record.id)
            ])
            record.attachment_ids = attachment_ids.ids

    def _inverse_attachments(self):
        for record in self:
            # Clear existing attachments
            existing_attachments = self.env['ir.attachment'].search([
                ('res_model', '=', self._name),
                ('res_id', '=', record.id)
            ])
            existing_attachment_ids = existing_attachments.ids

            # Add new attachments
            for attachment in record.attachment_ids:
                if attachment.id not in existing_attachment_ids:
                    attachment.write({
                        'res_model': self._name,
                        'res_id': record.id,
                    })

            # Remove attachments that are no longer linked
            for attachment in existing_attachments:
                if attachment.id not in record.attachment_ids.ids:
                    attachment.unlink()

    # ----------------- METHODES --------------------#

    def _test_food_cron(self):
        print("TEST CRON IS RUNNING . . . . .. .")
