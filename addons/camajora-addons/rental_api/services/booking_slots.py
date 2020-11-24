from datetime import datetime
from odoo.addons.component.core import Component


class BookingSlotsService(Component):
    _inherit = 'base.rest.private.service'
    _name = 'booking.slots.service'
    _usage = 'booking_slots'
    _description = 'Camajora private services: booking operations'

    def get(self, _id):
        """
        Get specific booking slot
        """
        slot_id = self.env['rental.booking.slot'].sudo().search([
            ('id', '=', _id),
            ('booking_id.state', 'in', ['confirmed']),
            ('booking_id.user_id', '=', self.env.user.partner_id.id)
        ])
        response = self._to_json(slot_id)
        response['qr_code'] = slot_id.booking_id.qr_code.decode('utf-8')
        return response

    def search(self):
        """
        Get all user's confirmed orders
        """
        slot_ids = self.env['rental.booking.slot'].sudo().search([
            ('booking_id.state', 'in', ['confirmed']),
            ('booking_id.user_id', '=', self.env.user.partner_id.id)
        ])
        return self._to_json(slot_ids, many=True)

    # PRIVATE  METHODS

    def _serialize(self, record):
        image = '{}/website/image/rental.resource.type/{}/image/200x0'.format(
            self.env['ir.config_parameter'].sudo().get_param('web.base.url'),
            record.resource_instance_id.resource_id.type_id.id
        )

        today = datetime.today()

        if today < record.dt_start:
            section = 'incoming'
        elif today > record.dt_end:
            section = 'archive'
        else:
            section = 'today'

        return {
            'id': record.id,
            'sku': record.name,
            'total_hours': record.total_hours,
            'image': image,
            'dt_start': record.dt_start,
            'dt_end': record.dt_end,
            'token': record.booking_id.token,
            'section': section,
        }

    def _get_object_schema(self):
        return {
            'id': {'type': 'integer', 'required': True},
            'sku': {'type': 'string', 'required': True},
            'total_hours': {'type': 'integer', 'required': True},
            'image': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
            'dt_start': {'type': 'datetime', 'required': True},
            'dt_end': {'type': 'datetime', 'required': True},
            'token': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
            'qr_code': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
            'section': {'type': 'string', 'required': True},
        }
