# Copyright 2020 Metadonors srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import calendar
import datetime
import logging
import pytz

from odoo.addons.component.core import Component
from odoo.exceptions import MissingError

_logger = logging.getLogger(__name__)
timezone = pytz.timezone('Europe/Rome')


def unpack_calendar_param(param):
    a, b = param.split('-', 1)
    return int(a), int(b)


class CalendarService(Component):
    _inherit = 'base.rest.public.service'
    _name = 'calendar.service'
    _usage = 'calendar'
    _description = 'Camajora public services: get calendar busy slots'

    # OPERATIONS

    def get(self, _id, target, slots):
        """
        Get busy days by resource, target (YYYY-MM) and slots ([0-24]-[0-24])
        """
        resource_id = self.env['rental.resource.instance'].sudo().search([('id', '=', _id)])

        if not resource_id:
            raise MissingError('Resource not found')

        try:
            year, month = unpack_calendar_param(target)
            start, end = unpack_calendar_param(slots)
        except Exception as e:
            raise MissingError('Cannot parse target date (YYYY-MM) or slots ([0-24]-[0-24]): ' + str(e))

        return {'busy': self._get_busy_days(resource_id, year, month, start, end)}

    def _validator_get(self):
        return {
            'target': {'type': 'string', 'required': True},
            'slots': {'type': 'string', 'required': True},
        }

    def _validator_return_get(self):
        return {
            'busy': {
                'type': 'list',
                'schema': {'type': 'string', 'required': True},
            }
        }

    def _get_busy_days(self, resource_id, year, month, start, end):
        busy = []

        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            target_start = datetime.datetime(year, month, day, start, 0)
            target_end = datetime.datetime(year, month, day, end - 1, 59)

            utc_target_start = timezone.localize(target_start).astimezone(pytz.utc).replace(tzinfo=None)
            utc_target_end = timezone.localize(target_end).astimezone(pytz.utc).replace(tzinfo=None)

            domain = [
                ('resource_instance_id', '=', resource_id.id),
                '|',
                    '&', ('dt_start', '<=', utc_target_start), ('dt_end', '>=', utc_target_end),
                    '|',
                        '&', ('dt_start', '<=', utc_target_start), ('dt_end', '>=', utc_target_start),
                        '&', ('dt_start', '<=', utc_target_end), ('dt_end', '>=', utc_target_end),
                    
            ]

            if self.env['rental.booking.slot'].sudo().search_count(domain) > 0:
                busy.append('{}-{:02}-{:02}'.format(year, month, day))

        return busy
