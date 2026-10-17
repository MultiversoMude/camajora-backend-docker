# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class ResourceTypesService(Component):
    _inherit = 'base.rest.public.service'
    _name = 'rental.resource.type.service'
    _usage = 'resource_types'
    _description = 'Camajora public services: get all resource types'

    # OPERATIONS

    def get(self, _id):
        """
        Get Resource by ID
        """
        category_id = self.env['rental.resource.type'].sudo().search([('id', '=', _id)])

        return self._to_json(category_id)

    def search(self):
        """
        Get all Types
        """
        category_ids = self.env['rental.resource.type'].sudo().search([])
        return self._to_json(category_ids, many=True)

    def category(self, **params):
        category = params['id']
        domain = [('category_id.id', '=', category if category else -100)]
        resource_ids = self.env['rental.resource.type'].sudo().search(domain)
        return self._to_json(resource_ids, many=True)

    def _validator_category(self):
        return {
            "id": {"type": "integer", "required": True},
        }

    # SERIALIZERS
    def _serialize(self, category_id):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        category_image_url = '{}/api/v1/public/images/{}?model=rental.resource.type'.format(
            base_url,
            category_id.id,
        )

        return {
            'name': category_id.name,
            'description': category_id.description or '',
            'image': category_image_url,
        }

    # VALIDATORS

    def _get_object_schema(self):
        return {
            'name': {
                'type': 'string',
                'required': True,
                'empty': False,
            },
            'description': {
                'type': 'string',
                'required': True,
                'empty': True,
            },
            'image': {
                'type': 'string',
                'required': True,
                'empty': True,
            },
        }
