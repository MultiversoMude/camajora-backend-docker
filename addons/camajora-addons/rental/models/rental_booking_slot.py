# Copyright 2020 Metadonors srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, time, timedelta
import pytz

timezone = pytz.timezone('Europe/Rome')


class RentalBookingSlot(models.Model):

    _name = 'rental.booking.slot'
    _description = 'Rental Booking Slot'
    """ :(
    _sql_constraints = [(
        'no_overlap',
        'EXCLUDE USING gist (resource_instance_id WITH =, tsrange(dt_start, dt_end) WITH &&)',
        _('Overlapping slots')  # CREATE EXTENSION btree_gist;
    )]
    """

    name = fields.Char(related='resource_instance_id.name', string=_('SKU'))
    partner_id = fields.Many2one(related="booking_id.user_id", store=True, string=_("Customer"))
    booking_id = fields.Many2one('rental.booking', string=_('Booking'), required=True, ondelete='cascade')
    resource_instance_id = fields.Many2one('rental.resource.instance', string=_('Resource Instance'), required=True)
    resource_id = fields.Many2one('rental.resource', related="resource_instance_id.resource_id", store=True, string=_('Resource'))
    location_id = fields.Many2one('rental.location', related="resource_id.location_id", store=True, string=_('Location'))
    owner_id = fields.Many2one('res.partner', related="resource_id.location_id.partner_id", store=True, string=_('Owner'))
    duration_id = fields.Many2one('rental.duration', string=_('Duration'), required=True)
    state = fields.Selection(related="booking_id.state", string="State")
    duration = fields.Selection([
        ('hourly', _('Hourly')),
        ('half_daily', _('Half daily')),
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
    ], related='duration_id.type', string=_('Duration Type'))

    start_date = fields.Date(string=_('Start Date'), required=True)
    end_date = fields.Date(string=_('End Date'), required=False)
    start_time = fields.Integer(string=_('Start Time'), required=False)
    end_time = fields.Integer(string=_('End Time'), required=False)

    half_day_type = fields.Selection([
        ('morning', _('09:00 - 14:00')),
        ('afternoon', _('14:00 - 19:00')),
        ('day', _('09:00 - 19:00')),
    ], string=_('Half Day'), default='morning', required=False)

    total_hours = fields.Integer(string=_('Total Hours'), readonly=True, compute='_compute_range', store=True)
    dt_start = fields.Datetime(string=_('Booking From'), readonly=True, compute='_compute_range', store=True)
    dt_end = fields.Datetime(string=_('Booking To'), readonly=True, compute='_compute_range', store=True)

    unlock_link = fields.Char(string=_('Unlock Link'), readonly=True, compute='_compute_unlock_link')

    @api.depends(
        'duration',
        'start_date',
        'end_date',
        'start_time',
        'end_time',
        'half_day_type'
    )
    def _compute_range(self):
        for record in self:
            slot_range = compute_range(
                record.duration,
                record.start_date,
                record.end_date,
                record.start_time,
                record.end_time,
                record.half_day_type,
            )
            record.total_hours = slot_range['total_hours']
            record.dt_start = slot_range['dt_start']
            record.dt_end = slot_range['dt_end']

    @api.constrains('resource_instance_id', 'dt_start', 'dt_end')
    def _check_dates(self):
        '''
        Check for overlapping date between booking slots of the same resource.
        There are 3 cases to consider:
        s1   s2   e1   e2
        (    [----)----]
        s2   s1   e2   e1
        [----(----]    )
        s1   s2   e2   e1
        (    [----]    )
        '''
        for record in self:
            # Starting date must be prior to the ending date
            dt_start = record.dt_start
            dt_end = record.dt_end
            if dt_end < dt_start:
                raise ValidationError(_('The ending date must not be prior to the starting date.'))

            domain = [
                ('id', '!=', record.id),
                ('resource_instance_id', '=', record.resource_instance_id.id),
                '|', '|',
                '&', ('dt_start', '<=', record.dt_start), ('dt_end', '>=', record.dt_start),
                '&', ('dt_start', '<=', record.dt_end), ('dt_end', '>=', record.dt_end),
                '&', ('dt_start', '<=', record.dt_start), ('dt_end', '>=', record.dt_end),
            ]

            # if self.search_count(domain) > 0:
            #     raise ValidationError(_('You can not have an overlap between two booking slots of the same resource.\n'
            #                             'Please correct the start and/or end dates of your booking slot.'))

    @api.depends('booking_id')
    def _compute_unlock_link(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.app.url')

        for record in self:
            record.unlock_link = '{}/api/v1/unlock/?token={}&sku={}'.format(
                base_url,
                record.booking_id.token,
                record.resource_instance_id.code,
            )

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.start_date < fields.Date.today():
            raise ValidationError(_('The starting date must not be in the past.'))
        return record


# ------------


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


def get_monday(day):
    return day - timedelta(days=(day.weekday() % 7))


def get_sunday(day):
    return day + timedelta(days=(6 - (day.weekday() % 7)))


def compute_range(duration, start_date, end_date, start_time, end_time, half_day_type):
    duration = duration or 'hourly'
    start_date = start_date or fields.Date.today()
    end_date = end_date or fields.Date.today()
    start_time = int(start_time) or 0
    end_time = int(end_time) or 0
    half_day_type = half_day_type or 'morning'
    day_hours = 0
    dt_start = None
    dt_end = None

    if duration == 'hourly':
        day_hours = end_time - start_time
        dt_start = datetime.combine(start_date, time(start_time, 0))
        dt_end = datetime.combine(start_date, time(end_time, 0))

    elif duration == 'half_daily':
        day_hours = 4 if half_day_type != 'day' else 8
        if half_day_type == 'morning':
            dt_start = datetime.combine(start_date, time(9, 0))
            dt_end = datetime.combine(start_date, time(13, 59))
        if half_day_type == 'afternoon':
            dt_start = datetime.combine(start_date, time(14, 0))
            dt_end = datetime.combine(start_date, time(18, 59))
        if half_day_type == 'day':
            dt_start = datetime.combine(start_date, time(9, 0))
            dt_end = datetime.combine(start_date, time(18, 59))

    elif duration == 'daily':
        day_hours = 10
        dt_start = datetime.combine(start_date, time(0, 0))
        dt_end = datetime.combine(end_date, time(23, 59))

    elif duration == 'weekly':
        day_hours = 10
        dt_start = datetime.combine(get_monday(start_date), time(0, 0))
        dt_end = datetime.combine(get_sunday(end_date), time(23, 59))

    elif duration == 'monthly':
        day_hours = 10
        dt_start = datetime.combine(start_date.replace(day=1), time(0, 0))
        dt_end = datetime.combine(last_day_of_month(end_date), time(23, 59))

    number_of_days = (dt_end - dt_start).days + 1

    total_hours = number_of_days * day_hours
    dt_start = timezone.localize(dt_start).astimezone(pytz.utc).replace(tzinfo=None)
    dt_end = timezone.localize(dt_end).astimezone(pytz.utc).replace(tzinfo=None)

    return {'total_hours': total_hours, 'dt_start': dt_start, 'dt_end': dt_end}
