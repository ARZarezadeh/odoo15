from odoo import models, fields, api
from datetime import timedelta, datetime


class EstatePropertyOffer(models.Model):
    """
    potential offers that send from buyer to seller
    """
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help='an offer can be accepted or refused by seller of property',
        copy=False
    )
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True)
    property_id = fields.Many2one(
        'estate.property', string='Property', required=True)
    property_type_id = fields.Many2one(
        'estate.property.type', related='property_id.property_type_id', readonly=True, store=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse='_inverse_date_deadline')

    # ? --------------------------- CONSTRAINTS  -------------------------------------------------

    _sql_constraints = [
        ('check_strictly_positive_price', 'check(price > 0)',
         'The Exptected Price Should Be strictly Positive'),
    ]

    # ? --------------------------- APIS  -------------------------------------------------

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """
        compute date deadline from create_date and validity
        """
        for record in self:
            if record.create_date:
                record.date_deadline = (record.create_date +
                                        timedelta(days=record.validity))
            else:
                record.date_deadline = datetime.now() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        """
        compute validity base on date_deadline
        """
        for record in self:
            print("_____INVERSE DEADLINE______")
            if record.create_date:
                print('++++++++create date is exists: ')

                record.validity = int(
                    (record.date_deadline - record.create_date.date())/timedelta(days=1))
            else:
                print("______create date do not exists")
                record.validity = 7

    def action_accept_offer(self):
        #  TODO: only one offer should be accepted.
        for record in self:
            print("status in offer set accpet status:::::;;;; ", record.status)
        self.status = 'accepted'

    def action_refuse_offer(self):
        for record in self:
            print("status in offer set refuse status:::::;;;; ", record.status)

        self.status = 'refused'
