# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component

import logging
_logger = logging.getLogger(__name__)


class ResourceService(Component):
    _inherit = 'base.rest.public.service'
    _name = 'resource.service'
    _usage = 'resources'
    _description = 'Camajora public services: get all resources'

    # OPERATIONS

    def get(self, _id):
        """
        Get Resource by ID
        """
        resource_id = self.env['rental.resource'].sudo().search([('id', '=', _id)])

        return self._to_json(resource_id)

    def search(self, **params):
        """
        Get all Resources
        """
        where_search_value = params.pop("where", None)
        when_search_value = params.pop("when", None)
        what_search_value = params.pop("what", None)

        domain = [('instances_ids', '!=', False)]

        if where_search_value:
            domain.append('|')
            domain.append(('location_id.name', 'ilike', where_search_value))
            domain.append(('location_id.city', 'ilike', where_search_value))
        if when_search_value:
            domain.append(('location_id.name', 'ilike', when_search_value))
        if what_search_value:
            domain.append(('type_id.category_id.name', 'ilike', what_search_value))

        resource_ids = self.env['rental.resource'].sudo().search(domain)
        return self._to_json(resource_ids, many=True)

    # SERIALIZERS

    def _serialize(self, resource_id):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        resource_image_url = '{}/api/v1/public/images/{}?model=rental.resource.type'.format(
            base_url,
            resource_id.type_id.id,
        )

        return {
            'name': resource_id.name,
            'code': resource_id.code,
            'location': resource_id.location_id.name,
            'location_id': resource_id.location_id.id,
            'location_address': resource_id.location_id.address or "",
            'location_postal_code': resource_id.location_id.postal_code or "",
            'location_city': resource_id.location_id.city or "",
            'location_state': resource_id.location_id.state_id.name if resource_id.location_id.state_id else "",
            'location_state_code': resource_id.location_id.state_id.code if resource_id.location_id.state_id else "",
            'location_country': resource_id.location_id.country_id.name if resource_id.location_id.country_id else "",
            'location_state_id': resource_id.location_id.state_id.id,
            'location_country_id': resource_id.location_id.country_id.id,
            'type': resource_id.type_id.category_id.name or "",
            'category_id': resource_id.type_id.category_id.id,
            'description': resource_id.type_id.description if resource_id.type_id.description else "",
            'image': resource_image_url or "",
            'performance': resource_id.type_id.performance_id.name or "",
            'credit_cost': resource_id.credit_cost,
            'setup': resource_id.type_id.setup_id.name or "",
            'size': resource_id.type_id.size_id.name,
            'instance_count': resource_id.instance_count,
            'instances': self._serialize_instances(resource_id),
        }

    def _serialize_instances(self, resource_id):
        return [self._serialize_instance(instance_id) for instance_id in resource_id.instances_ids]

    def _serialize_instance(self, instance_id):
        return {
            'id': instance_id.id,
            'code': instance_id.code
        }

    # VALIDATORS

    def _validator_search(self):
        return {
            "where": {"type": "string", "required": False},
            "when": {"type": "string", "required": False},
            "what": {"type": "string", "required": False},
        }

    def _get_object_schema(self):
        return {
            'name': {'type': 'string', 'required': True, 'empty': False},
            'code': {'type': 'string', 'required': True, 'empty': False},
            'location': {'type': 'string', 'required': True, 'empty': False},
            'location_id': {'type': 'integer', 'required': True},
            'location_address': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
            'location_postal_code': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
            'location_city': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
            'location_state': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
            'location_state_code': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
            'location_country': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
            'location_state_id': {'type': 'integer', 'required': False, 'empty': True, 'nullable': True},
            'location_country_id': {'type': 'integer', 'required': False, 'empty': True, 'nullable': True},
            'type': {'type': 'string', 'required': True, 'empty': False},
            'category_id': {'type': 'integer', 'required': True},
            'description': {'type': 'string', 'required': False, 'empty': True, 'nullable': True},
            'image': {'type': 'string', 'required': True, 'empty': False},
            'performance': {'type': 'string', 'required': True, 'empty': False},
            'credit_cost': {'type': 'float', 'required': True, 'empty': False},
            'setup': {'type': 'string', 'required': True, 'empty': False},
            'size': {'type': 'string', 'required': True, 'empty': False},
            'instance_count': {'type': 'integer', 'required': True},
            'instances': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'id': {'type': 'integer', 'required': True},
                        'code': {'type': 'string', 'required': True},
                    }
                }
            }
        }
