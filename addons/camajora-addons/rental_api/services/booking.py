import logging

from odoo import _
from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class BookingService(Component):
    _inherit = 'base.rest.private.service'
    _name = 'booking.service'
    _usage = 'booking'
    _description = 'Camajora private services: booking operations'

    def search(self):
        """
        Get current cart or create one if not found
        """
        cart = self._get()
        return self._to_json(cart)

    def add_item(self, **params):
        """
        Add a booking slot to current cart
        """
        cart = self._get()
        self._add_item(cart, params)
        return self._to_json(cart)

    def remove_item(self, **params):
        """
        Remove a booking slot from current cart
        """
        cart = self._get()
        self._delete_item(cart, params)
        return self._to_json(cart)

    def clear(self, **params):
        """
        Remove all booking slots from current cart
        """
        cart = self._get()
        cart = self._clear_cart(cart)
        return self._to_json(cart)

    def confirm(self):
        """
        Set current cart state to 'confirmed'
        WITHOUT CHECKING CREDITS!!
        """
        cart = self._get()
        cart.write({'state': 'confirmed'})
        return self._to_json(cart)

    def get_confirmed(self):
        """
        Get all user's confirmed orders
        """
        booking_ids = self.env['rental.booking'].sudo().search([
            ('state', 'in', ['confirmed']),
            ('user_id', '=', self.env.user.partner_id.id)
        ])
        return self._to_json(booking_ids, many=True)

    # PRIVATE  METHODS

    def _serialize(self, record):
        data = {}
        data['id'] = record.id
        data['state'] = record.state
        data['name'] = record.name
        data['user_id'] = record.user_id.id
        data['user_name'] = record.user_id.name
        data['date'] = record.date
        data['token'] = record.token
        data['lines'] = self._serialize_slots(record)

        _logger.error('Serialized cart:')
        _logger.error(data)
        return data

    def _serialize_slots(self, cart):
        items = []
        for slot in cart.slot_ids:
            items.append(self._serialize_one_slot(slot))

        return {'count': cart.slot_count, 'items': items}

    def _serialize_one_slot(self, line):
        image = '{}/api/v1/public/images/{}?model=rental.resource.type'.format(
            self.env['ir.config_parameter'].sudo().get_param('web.base.url'),
            line.resource_instance_id.resource_id.type_id.id,
        )

        return {
            'id': line.id,
            'sku': line.name,
            'total_hours': line.total_hours,
            'image': image,
            'dt_start': line.dt_start,
            'dt_end': line.dt_end,
        }

    def _get_object_schema(self):
        return {
            'id': {'type': 'integer', 'required': True, 'empty': False, 'nullable': False},
            'state': {'type': 'string', 'required': True, 'empty': False, 'nullable': False},
            'name': {'type': 'string', 'required': True, 'empty': False, 'nullable': False},
            'user_id': {'type': 'integer', 'required': True, 'empty': False, 'nullable': False},
            'user_name': {'type': 'string', 'required': True, 'empty': False, 'nullable': False},
            'date': {'type': 'date', 'required': True, 'empty': False, 'nullable': False},
            'token': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
            'lines': {
                'type': 'dict',
                'schema': {
                    'count': {'type': 'float', 'required': False, 'empty': True, 'nullable': True},
                    'items':  {
                        'type': 'list',
                        'schema': {
                            'type': 'dict',
                            'schema': {
                                'id': {'type': 'integer', 'required': True},
                                'sku': {'type': 'string', 'required': True},
                                'total_hours': {'type': 'integer', 'required': True},
                                'image': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
                                'dt_start': {'type': 'datetime', 'required': True},
                                'dt_end': {'type': 'datetime', 'required': True},
                            }
                        }
                    }
                }
            }
        }

    def _get(self, create_if_not_found=True):
        self.env.cr.execute(
            'SELECT 1 FROM rental_booking WHERE state = \'draft\' and user_id = %s FOR UPDATE',
            [self.env.user.partner_id.id]
        )

        cart = self.env['rental.booking'].sudo().search([
            ('state', 'in', ['draft']),
            ('user_id', '=', self.env.user.partner_id.id)
        ])

        if cart:
            return cart[0]

        _logger.error('CART NOT FOUND')
        if create_if_not_found:
            return self._create_empty_cart()

    def _create_empty_cart(self):
        return self.env['rental.booking'].sudo().create({
            'user_id': self.env.user.partner_id.id
        })

    def _add_item(self, cart, params):
        if cart.state != 'draft':
            raise UserError(_('You can\'t add item in this cart'))

        resource_id = self.env['rental.resource'].sudo().search([('id', '=', params['resource_id'])])
        if not resource_id:
            raise UserError(_('Resource not found'))

        duration_id = self.env['rental.duration'].sudo().search([('type', '=', params['duration'])])
        if not duration_id:
            raise UserError(_('Duration not found'))

        resource_instance_id = resource_id.get_best_instance_match(**params)

        self.env['rental.booking.slot'].sudo().create({
            'booking_id': cart.id,
            'resource_instance_id': resource_instance_id,
            'duration_id': duration_id.id,
            'start_date':  params['start_date'],
            'end_date':  params['end_date'],
            'start_time':  params['start_time'],
            'end_time':  params['end_time'],
            'half_day_type':  params['half_day_type'],
        })

    def _clear_cart(self, cart):
        if cart.state != 'draft':
            raise UserError(_('State cart error'))

        cart.sudo().write({'slot_ids': [(5, False, False)]})
        return cart

    def _delete_item(self, cart, params):
        if cart.state != 'draft':
            raise UserError(_('You can\'t delete items from this cart'))

        slot_id = self.env['rental.booking.slot'].sudo().search([
            ('id', '=', params['slot_id']),
            ('booking_id', '=', cart.id),
        ])

        if slot_id:
            slot_id.sudo().unlink()

    # VALIDATORS

    def _validator_return_search(self):
        return self._validator_return_get()

    def _validator_add_item(self):
        return {
            'resource_id': {
                'type': 'integer',
                'coerce': to_int,
                'required': True,
            },
            'duration': {'type': 'string', 'required': True},
            'start_date': {'type': 'string', 'required': True},
            'end_date': {'type': 'string', 'required': False, 'nullable': True},
            'start_time': {'type': 'string', 'required': False, 'nullable': True},
            'end_time': {'type': 'string', 'required': False, 'nullable': True},
            'half_day_type': {'type': 'string', 'required': False, 'nullable': True},  # FIXME LIMIT TO POTENTIAL
        }

    def _validator_remove_item(self):
        return {
            'slot_id': {'type': 'integer', 'coerce': to_int, 'required': True}
        }

    def _validator_clear(self):
        return {}

    def _validator_confirm(self):
        return {}

    def _validator_get_confirmed(self):
        return {}
