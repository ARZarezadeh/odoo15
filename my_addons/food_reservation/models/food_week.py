from odoo import api, models, fields
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError, ValidationError


class FoodWeek(models.Model):
    _name = 'food.week'
    _description = 'Food Week'

    name = fields.Char(string="week", compute='_compute_name', store=True)

    year = fields.Char(string="Year", required=True, default="2024")
    week_number = fields.Integer(
        string='Week Number', compute="_compute_week_number", store=True, index=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(
        string='End Date', compute="_compute_end_date", readonly=True, store=True)
    day_ids = fields.One2many('food.day', 'week_id')

    # ----------------- CONSTRAINTS --------------------#

    _sql_constraints = [
        ('unique_week_year', 'unique (week_number, year)',
         'Week and year must be unique'),
    ]

    # ----------------- APIS --------------------#

    @api.model
    def create_first_week(self):
        year, week_number, week_day = datetime.now().isocalendar()
        start_date = datetime.strptime(
            f"{year}-W{week_number - 1}", '%Y-W%W-%w')
        end_date = start_date + timedelta(days=6)
        self.create({
            'name': f"{start_date}-{end_date}",
            "year": year,
            "week_number": week_number,
            "start_date": start_date,
            "end_date": end_date
        })

    @api.model
    def create_next_week(self):
        last_week = self.search([], order='week_number desc', limit=1)
        if last_week:
            year = last_week.year
            week_number = last_week.week_number + 1
            start_date = last_week.end_date + timedelta(days=1)
            end_date = start_date + timedelta(days=6)
            self.create({
                'name': f'Week {week_number}',
                'year': year,
                'week_number': week_number,
                'start_date': start_date,
                'end_date': end_date,
            })
        else:
            self.create_first_week()

    @api.model
    def create(self, vals):
        print("__________creating new week_________")
        week = super(FoodWeek, self).create(vals)
        start_date = week.start_date
        end_date = week.end_date
        delta = timedelta(days=1)

        while start_date <= end_date:
            existing_day = self.env['food.day'].search(
                [('day', '=', start_date), ('week_id', '=', week.id)])
            if not existing_day:
                self.env['food.day'].create({
                    'day': start_date,
                    'week_id': week.id,
                })
            start_date += delta

        return week

    @api.depends('start_date')
    def _compute_name(self):
        for record in self:
            if record.start_date:
                record.name = f"{
                    record.start_date}__{record.start_date + timedelta(days=6)}"
            else:
                record.name = ''

    @api.depends('start_date')
    def _compute_end_date(self):
        for record in self:
            if record.start_date:
                endd = record.start_date + timedelta(days=6)
                print('this is end date; ', endd)
                record.end_date = endd
            else:
                record.end_date = False

    @api.depends('start_date')
    def _compute_week_number(self):
        for record in self:
            if record.start_date:
                year = record.start_date.year
                month = record.start_date.month
                day = record.start_date.day
                print("this is start:: ", year, month, day,
                      date(2010, 6, 16).isocalendar()[1])
                week_number = date(year, month, day).isocalendar()[1]
                print("this is week_number:: ", week_number)
                record.week_number = week_number
            else:
                record.week_number = 0

    @api.constrains('start_date', 'year')
    def _check_unique_week_year(self):
        for record in self:
            if record.start_date and record.year:
                if record.start_date.year != int(record.year):
                    raise UserError(
                        'your selected year and year of start date do not match')
                year = record.start_date.year
                month = record.start_date.month
                day = record.start_date.day
                week_number = date(year, month, day).isocalendar()[1]
                existing_weeks = self.search(
                    [('week_number', '=', week_number), ('year', '=', record.year)])
                if len(existing_weeks) > 1:
                    raise ValidationError('Week and year must be unique')

    # ----------------- FUNTIONS --------------------#

    def create_next_week_button(self):
        self.env['food.week'].create_next_week()
