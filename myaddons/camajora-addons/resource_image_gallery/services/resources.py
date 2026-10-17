# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component

import logging
_logger = logging.getLogger(__name__)


class ResourceService(Component):
    _inherit = 'resource.service'

    def _serialize(self, resource_id):
        serialized = super()._serialize(resource_id)

        if resource_id.image_ids:
            serialized['image'] = resource_id.image_ids[0].image_id.file_id.url

        serialized['image_gallery'] = [i.image_id.file_id.url for i in resource_id.image_ids]

        return serialized

    def _get_object_schema(self):
        schema = super()._get_object_schema()

        schema['image_gallery'] = {
            'type': 'list',
            'schema': {
                'type': 'string', 'required': False, 'empty': True, 'nullable': True
            }
        }

        return schema
