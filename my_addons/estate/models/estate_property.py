from odoo import models, fields, api, exceptions
import logging

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True, copy=False, compute='_compute_selling_price')
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')],
        help="Select What Direction you want to garden be."
    )
    total_area = fields.Integer(compute="_compute_total_area")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="The State that this property is in",
        required=True,
        copy=False,
        default='new'
    )

    property_type_id = fields.Many2one(
        'estate.property.type', string='Property Type')

    tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')

    sales_person_id = fields.Many2one(
        'res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner',  string='Buyer',
                               copy=False, compute='_get_buyerid_from_accepted_offer')

    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id', string='Offers')

    best_price = fields.Float(compute='_compute_best_offer')

    # ? --------------------------- CONSTRAINTS  -------------------------------------------------

    _sql_constraints = [
        ('check_strictly_positive_expected_price', 'check(expected_price > 0)',
         'The Exptected Price Should Be strictly Positive'),
        ('check_positive_selling_price', 'check(selling_price >= 0)',
         'Selling Price Should Be Positive If Exist'),
    ]

    # ? --------------------------- APIS  -------------------------------------------------

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        """
        computing total area from adding living area and garden area
        """
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        """
        finding best offer(max price)
        """

        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = record.selling_price

    @api.depends("offer_ids.status")
    def _compute_selling_price(self):
        """
        when an offer accpeted set the selling price with price of accpeted offer
        """
        for record in self:
            if record.offer_ids:
                record.state = record.state if record.state == 'sold' or record.state == 'canceled' else 'offer_received'
                offers_status = record.offer_ids.mapped('status')
                if 'accepted' in offers_status:
                    print("INDEX OF ACCEPTED OFFER: ",
                          offers_status.index('accepted'), offers_status.count('accepted'))
                    print("ACCEPTED OFFER PRICE: ",
                          record.offer_ids[offers_status.index('accepted')].price)
                # record.selling_price = record.offer_ids[offers_status.index(
                #     'accepted')].price
                    record.selling_price = record.offer_ids[offers_status.index(
                        'accepted')].price
                    record.state = record.state if record.state == 'sold' or record.state == 'canceled' else 'offer_accepted'
                else:
                    record.selling_price = 00.00
            else:
                record.selling_price = 00.00

    def _get_buyerid_from_accepted_offer(self):
        """
        when an offer accpeted set the selling price with price of accpeted offer
        """
        for record in self:
            if record.offer_ids:
                offers_status = record.offer_ids.mapped('status')
                if 'accepted' in offers_status:
                    print("INDEX OF ACCEPTED OFFER: ",
                          offers_status.index('accepted'), offers_status.count('accepted'))
                    print("ACCEPTED OFFER PRICE: ",
                          record.offer_ids[offers_status.index('accepted')].price)
                    record.buyer_id = record.offer_ids[offers_status.index(
                        'accepted')].partner_id
                else:
                    record.buyer_id = False
            else:
                record.buyer_id = False

    @api.onchange("garden")
    def _onchange_garden(self):
        """
        when garden set, garden area set to 10 and orientation to North automatically
        """
        if (self.garden):
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.ondelete(at_uninstall=False)
    def _prevent_delete_not_new_not_canceled(self):
        for record in self:
            if not (record.state == 'new' or record.state == 'canceled'):
                print("///////// it sould not be deleted /////////")
                raise exceptions.UserError(
                    'Only New or Canceled Properties Can Be Deleted')

    # ? --------------------------- ACTIONS  -------------------------------------------------

    def action_sell_property(self):
        """
        action for button in veiw, when clicked state change to "sold"
        """
        print('|||| sell property', self.state)
        if self.state == 'canceled':
            raise exceptions.UserError('Cancelled Property Can Not Be Sold')
        self.state = 'sold'

    def action_cancell_property(self):
        """
        action for button in veiw, when clicked state change to "sold"
        """
        if self.state == 'sold':
            raise exceptions.UserError('Sold Property Can Not Be Cancelled')
        self.state = 'canceled'

    def action_back_to_default_property(self):
        """
        when default button clicked, set state to "new", for testing
        """
        self.state = 'new'
