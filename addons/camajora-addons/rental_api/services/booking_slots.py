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
        slot_id = self.env['rental.booking.slot'].search([
            ('id', '=', _id),
            ('booking_id.state', 'in', ['confirmed']),
        ])
        response = self._to_json(slot_id)
        response['qr_code'] = slot_id.booking_id.qr_code.decode('utf-8')
        return response

    def search(self):
        """
        Get all user's confirmed orders
        """
        slot_ids = self.env['rental.booking.slot'].search([
            ('booking_id.state', 'in', ['confirmed']),
        ])
        return self._to_json(slot_ids, many=True)

    # PRIVATE  METHODS

    def _serialize(self, record):
        image = '{}/api/v1/public/images/{}?model=rental.resource.type'.format(
            self.env['ir.config_parameter'].sudo().get_param('web.base.url'),
            record.resource_instance_id.resource_id.type_id.id,
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
            'name': record.resource_instance_id.resource_id.name,
            'sku': record.name,
            'total_hours': record.total_hours,
            'image': image,
            'dt_start': record.dt_start,
            'dt_end': record.dt_end,
            'start_date': record.start_date,
            'end_date': record.end_date,
            'start_time': record.start_time,
            'end_time': record.end_time,
            'token': record.booking_id.token,
            'section': section,
        }

    @staticmethod
    def _get_object_schema():

        return {
            'id': {'type': 'integer', 'required': True},
            'sku': {'type': 'string', 'required': True},
            'name': {'type': 'string', 'required': True},
            'total_hours': {'type': 'integer', 'required': True},
            'image': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
            'dt_start': {'type': 'datetime', 'required': True},
            'dt_end': {'type': 'datetime', 'required': True},
            'start_date': {'type': 'date', 'required': True},
            'end_date': {'type': 'date', 'required': False, 'nullable': True, 'empty': True},
            'start_time': {'type': 'integer', 'required': True},
            'end_time': {'type': 'integer', 'required': True},
            'token': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
            'qr_code': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
            'section': {'type': 'string', 'required': True},
        }
