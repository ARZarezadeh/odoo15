
from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    max_attachment_size = fields.Integer(
        string='Max Attachment Size_MB', store=True, config_parameter='food_reservation.max_attachment_size')

    @api.onchange('max_attachment_size')
    def test(self):
        print("max_attachment_size", self.max_attachment_size)
