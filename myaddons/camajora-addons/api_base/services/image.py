# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import logging

from odoo import SUPERUSER_ID
from odoo.addons.base_rest.components.service import skip_secure_response
from odoo.addons.component.core import AbstractComponent
from odoo.exceptions import MissingError
from odoo.http import request

log = logging.getLogger(__name__)


class BaseImageService(AbstractComponent):
    _inherit = 'base.rest.service'
    _name = 'base.rest.public.image'
    _collection = 'base.rest.public.services'
    _expose_model = None

    @skip_secure_response
    def _get_image_response(self, _id, model):
        status, headers, content = self.env['ir.http'].binary_content(
            model=model, id=_id, field='image', env=self.env(user=SUPERUSER_ID)
        )

        if not content:
            raise MissingError('Image not found')

        image_base64 = base64.b64decode(content)
        headers.append(('Content-Length', len(image_base64)))
        response = request.make_response(image_base64, headers)
        response.status_code = status
        return response

    def _validator_get(self):
        return {
            'model': {'type': 'string', 'required': True},
        }
