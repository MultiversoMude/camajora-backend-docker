# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base_rest.components.service import skip_secure_response
from odoo.addons.component.core import Component


class ResourceImageService(Component):
    _inherit = 'base.rest.public.image'
    _name = 'resource.image.service'
    _usage = 'images'
    _description = 'Camajora public services: get images by ID, model and size'

    @skip_secure_response
    def get(self, _id, model):
        return self._get_image_response(_id, 'rental.resource.type')
