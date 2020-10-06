# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
# from odoo.exceptions import ValidationError
from datetime import datetime, time, timedelta
import pytz

timezone = pytz.timezone('Europe/Rome')


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


def get_monday(day):
    return day - timedelta(days=(day.weekday() % 7))


def get_sunday(day):
    return day + timedelta(days=(6 - (day.weekday() % 7)))


class RentalBookingSlot(models.Model):

    _name = 'rental.booking.slot'
    _description = 'Rental Booking Slot'

    name = fields.Char(related='resource_instance_id.name', string=_('SKU'))
    booking_id = fields.Many2one('rental.booking', string=_('Booking'), required=True)
    resource_instance_id = fields.Many2one('rental.resource.instance', string=_('Resource Instance'), required=True)
    duration_id = fields.Many2one('rental.duration', string=_('Duration'), required=True)
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

    total_hours = fields.Integer(string=_('Total hours'), readonly=True, compute='_compute_range', store=True)
    dt_start = fields.Datetime(string=_('Datetime from'), readonly=True, compute='_compute_range', store=True)

    dt_end = fields.Datetime(string=_('Datetime to'), readonly=True, compute='_compute_range', store=True)
    qr_code = fields.Char(string=_('Code'), readonly=True)

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
            duration = record.duration or 'hourly'
            start_date = record.start_date or fields.Date.today()
            end_date = record.end_date or fields.Date.today()
            start_time = record.start_time or 0
            end_time = record.end_time or 0
            half_day_type = record.half_day_type or 'morning'

            if duration == 'hourly':
                record.total_hours = end_time - start_time
                dt_start = datetime.combine(start_date, time(start_time, 0))
                dt_end = datetime.combine(start_date, time(end_time, 0))

            elif duration == 'half_daily':
                record.total_hours = 4 if half_day_type != 'day' else 8
                if half_day_type == 'morning':
                    dt_start = datetime.combine(start_date, time(9, 0))
                    dt_end = datetime.combine(start_date, time(14, 0))
                if half_day_type == 'afternoon':
                    dt_start = datetime.combine(start_date, time(14, 0))
                    dt_end = datetime.combine(start_date, time(19, 0))
                if half_day_type == 'day':
                    dt_start = datetime.combine(start_date, time(9, 0))
                    dt_end = datetime.combine(start_date, time(19, 0))

            elif duration == 'daily':
                record.total_hours = 10
                dt_start = datetime.combine(start_date, time(0, 0))
                dt_end = datetime.combine(end_date, time(23, 59))

            elif duration == 'weekly':
                record.total_hours = 168
                dt_start = datetime.combine(get_monday(start_date), time(0, 0))
                dt_end = datetime.combine(get_sunday(end_date), time(23, 59))

            elif duration == 'monthly':
                record.total_hours = 720
                dt_start = datetime.combine(start_date.replace(day=1), time(0, 0))
                dt_end = datetime.combine(last_day_of_month(end_date), time(23, 59))

            record.dt_start = timezone.localize(dt_start).astimezone(pytz.utc).replace(tzinfo=None)
            record.dt_end = timezone.localize(dt_end).astimezone(pytz.utc).replace(tzinfo=None)
