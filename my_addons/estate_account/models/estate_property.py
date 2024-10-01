from odoo import models, Command, exceptions


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        print("_________ sel property ___________")
        print("//// this is account.move:::",
              self.env['account.move'].check_access_rights('create'), self.buyer_id.id, self.env['account.journal'])

        # ? Create Invoice
        if not (self.env['account.move'].check_access_rights('create')):
            raise exceptions.AccessError(
                'you do not have access to sell this property')
        if not self.buyer_id:
            raise exceptions.MissingError(
                'this property do not have partner_id')
        newInvoice = self.env['account.move'].sudo().create({
            'name': f"{self.name}-invoice",
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create(
                    {'name': 'commission', 'price_unit': self.selling_price, 'quantity': 0.06}),
                Command.create(
                    {'name': 'fee', 'price_unit': 100.00, 'quantity': 1}),
            ],
        })
        print("||||||| new invoice: ", newInvoice)

        return super().action_sell_property()
