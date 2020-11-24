# Copyright 2020 Metadonors srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
from odoo.exceptions import MissingError


class UnlockService(Component):
    _inherit = 'base.rest.private.service'
    _name = 'unlock.service'
    _usage = 'unlock'
    _description = 'Camajora private services: unlock Resource by token'

    def create(self, token, sku):
        """
        Get booking slot informations from booking token and resource SKU
        """
        booking_slot_id = self.env['rental.booking.slot'].sudo().search([
            ('booking_id.state', '=', 'confirmed'),
            ('booking_id.token', '=', token),
            ('resource_instance_id.code', '=', sku),
        ])

        if not booking_slot_id:
            raise MissingError('Invalid or expired token')

        return self._serialize(booking_slot_id)

    # PRIVATE  METHODS

    def _serialize(self, record):
        data = {}
        data['dt_start'] = record.dt_start
        data['dt_end'] = record.dt_end
        return data

    # VALIDATORS

    def _validator_create(self):
        return {
            'token': {'type': 'string', 'required': True, 'empty': False},
            'sku': {'type': 'string', 'required': True, 'empty': False}
        }

    def _validator_return_create(self):
        return {
            'dt_start': {'type': 'datetime', 'required': True},
            'dt_end': {'type': 'datetime', 'required': True},
        }
