from odoo import api, fields, models, _
import logging
from odoo.exceptions import ValidationError
from datetime import datetime, time, timedelta
import pytz

timezone = pytz.timezone('Europe/Rome')
log = logging.getLogger(__name__)


class MyWizard(models.TransientModel):
    _name = 'my.wizard'
    _inherit = ['multi.step.wizard.mixin']

    location = fields.Many2one(
        comodel_name='rental.location',
        name="Location",
        required=True,
        ondelete='cascade',
        default=lambda self: self._default_project_id(),
    )

    location_id = fields.Integer(string=_('Id'), default=lambda self: self._default_project_id())

    resource_id = fields.Many2one('rental.resource', string=_('Resources'),
                                  default=lambda self: self._default_resource())

    instances_ids = fields.Many2one('rental.resource.instance', string=_('Instances'), required=True)

    name = fields.Char(string=_('SKU'))
    # Campi per la creazione di una prenotazione
    user_id = fields.Many2one('res.partner', string=_('User'), required=True)
    date = fields.Date(string=_('Date'), default=lambda self: fields.Date.today())
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

    total_hours = fields.Integer(string=_('Total Hours'), readonly=True, compute='_compute_range', store=True)
    dt_start = fields.Datetime(string=_('Booking From'), readonly=True, compute='_compute_range', store=True)
    dt_end = fields.Datetime(string=_('Booking To'), readonly=True, compute='_compute_range', store=True)
    # Stati finali
    token = fields.Char(string=_('Secret Token'), readonly=True)
    qr_code = fields.Binary(string=_('QR Code'), readonly=True)
    booking_id = fields.Integer(string=_('Booking ID'))

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

    @api.constrains('instances_ids', 'dt_start', 'dt_end')
    def _check_dates(self):

        for record in self:
            # Starting date must be prior to the ending date
            dt_start = record.dt_start
            dt_end = record.dt_end
            if dt_end < dt_start:
                raise ValidationError(_('The ending date must not be prior to the starting date.'))

            domain = [
                ('id', '!=', record.id),
                ('resource_instance_id', '=', record.instances_ids.id),
                '|', '|',
                '&', ('dt_start', '<=', record.dt_start), ('dt_end', '>=', record.dt_start),
                '&', ('dt_start', '<=', record.dt_end), ('dt_end', '>=', record.dt_end),
                '&', ('dt_start', '<=', record.dt_start), ('dt_end', '>=', record.dt_end),
                '&', ('dt_start', '>=', record.dt_start), ('dt_end', '<=', record.dt_end),
            ]

            if self.env['rental.booking.slot'].sudo().search_count(domain) > 0:
                raise ValidationError(_('You can not have an overlap between two booking slots of the same resource.\n'
                                        'Please correct the start and/or end dates of your booking slot.'))

    @api.depends('booking_id')
    def _compute_unlock_link(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.app.url')

        for record in self:
            record.unlock_link = '{}/api/v1/unlock/?token={}&sku={}'.format(
                base_url,
                record.booking_id.token,
                record.instances_ids.code,
            )

    @api.model
    def _selection_state(self):
        return [
            ('start', 'Start'),
            ('error', 'Error'),
            ('final', 'Final'),
        ]

    @api.model
    def _default_project_id(self):
        log.debug(self, 'active id is %s', self.env.context.get('active_id'))
        resource = self.env['rental.resource'].search([('id', '=', self.env.context.get('active_id'))])
        return resource.location_id

    @api.model
    def _default_resource(self):
        selected_ids = self.env.context.get('active_ids', [])
        selected_records = self.env['rental.resource'].browse(selected_ids)
        return selected_records

    def state_exit_start(self):

        slot = {
            'partner_id': self.user_id.id,
            'owner_id': self.env.user.partner_id.id,
            'duration_id': self.duration_id.id,
            'resource_instance_id': self.instances_ids.id,
            'resource_id': self.resource_id.id,
            'location_id': self.location_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'half_day_type': self.half_day_type,
            'total_hours': self.total_hours,
            'dt_start': self.dt_start,
            'dt_end': self.dt_end
        }

        pronation = {
            'name': 'random',
            'date': self.start_date,
            'user_id': self.user_id.id,
            'rent_channel': 'main_site',
            'state': 'confirmed',
            'slot_ids': [
                (0, 0, slot)
            ]
        }

        booking = self.env['rental.booking'].create(pronation)
        self.env.cr.commit()
        self.booking_id = booking.slot_ids[0].id
        self.send_mail()

        self.state = 'final'

    def send_mail(self):
        log.debug("Invia email Reservation slot :%s", self.booking_id)
        template_ids = self.env.ref('rental.reservation_confirm_email').id
        if template_ids:
            self.env['mail.template'].browse(template_ids).send_mail(self.booking_id, force_send=True)

    def state_exit_error(self):
        self.state = 'error'

    @api.model
    def _compute_current_id(self):
        log.debug(self, "Computing id")
        return self.env.context.get('active_id')

    # ------------


def compute_range(duration, start_date, end_date, start_time, end_time, half_day_type):
    duration = duration or 'hourly'
    start_date = start_date or fields.Date.today()
    end_date = end_date or fields.Date.today()
    start_time = int(start_time or 0)
    end_time = int(end_time or 0)
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


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


def get_monday(day):
    return day - timedelta(days=(day.weekday() % 7))


def get_sunday(day):
    return day + timedelta(days=(6 - (day.weekday() % 7)))
