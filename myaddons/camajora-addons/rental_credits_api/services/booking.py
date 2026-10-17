import logging

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class BookingService(Component):
    _inherit = 'booking.service'

    def confirm(self):
        """
        Set current cart state to 'confirmed'
        """
        # Call action confirm on Booking model to check credits
        cart = self._get()
        cart.action_confirm()
        return self._to_json(cart)

    def _serialize(self, record):
        data = super()._serialize(record)
        data['credits_used'] = record.credits_used

        return data

    def _serialize_one_slot(self, line):
        data = super()._serialize_one_slot(line)
        data['credit_total'] = line.credit_total

        return data

    def _get_object_schema(self):
        schema = super()._get_object_schema()
        amount_schema = {
            'type': 'float',
            'required': True,
            'empty': False,
            'nullable': False
        }
        schema['credits_used'] = amount_schema
        schema['lines']['schema']['items']['schema']['schema']['credit_total'] = amount_schema

        return schema
