
# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


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

    def search(self):
        """
        Get all Resources
        """
        resource_ids = self.env['rental.resource'].sudo().search([])
        return self._to_json(resource_ids, many=True)

    # SERIALIZERS

    def _serialize(self, resource_id):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        resource_image_url = '{}/api/v1/public/images/{}?model=rental.resource.type'.format(
            base_url,
            resource_id.type_id.id,
        )

        """ NOT WORKING IF NOT LOGGED
        resource_image_url = '{}/website/image/rental.resource.type/{}/image/500x0'.format(
            base_url,
            resource_id.type_id.id,
        )
        """

        return {
            'name': resource_id.name,
            'code': resource_id.code,
            'location': resource_id.location_id.name,
            'type': resource_id.type_id.category_id.name,
            'description': resource_id.type_id.description if resource_id.type_id.description else "",
            'image': resource_image_url,
            'performance': resource_id.type_id.performance_id.name,
            'price': resource_id.type_id.price,
            'setup': resource_id.type_id.setup_id.name,
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

    def _get_object_schema(self):
        return {
            'name': {
                'type': 'string',
                'required': True,
                'empty': False,
            },
            'code': {
                'type': 'string',
                'required': True,
                'empty': False,
            },
            'location': {
                'type': 'string',
                'required': True,
                'empty': False,
            },
            'type': {
                'type': 'string',
                'required': True,
                'empty': False,
            },
            'description': {
                'type': 'string',
                'required': False,
                'empty': True,
                'nullable': True,
            },
            'image': {
                'type': 'string',
                'required': True,
                'empty': False,
            },
            'performance': {
                'type': 'string',
                'required': True,
                'empty': False,
            },
            'price': {
                'type': 'float',
                'required': True,
                'empty': False,
            },
            'setup': {
                'type': 'string',
                'required': True,
                'empty': False,
            },
            'size': {
                'type': 'string',
                'required': True,
                'empty': False,
            },
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
