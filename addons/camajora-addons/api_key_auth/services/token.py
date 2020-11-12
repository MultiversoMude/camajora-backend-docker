# Copyright 2020 Metadonors srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.component.core import Component
from odoo.exceptions import AccessDenied

_logger = logging.getLogger(__name__)


class TokenService(Component):
    _inherit = 'base.rest.service'
    _name = 'token.service'
    _usage = 'token'
    _collection = 'rest.auth.public.services'
    _description = 'Auth services: get a token from credentials'

    def create(self, **data):
        """
        Get a token from credentials
        """
        try:
            uid = self.env['res.users'].sudo()._login(
                self.env.cr.dbname, data['login'], data['password']
            )
        except AccessDenied:
            raise AccessDenied()

        if not uid:
            raise AccessDenied()

        user_id = self.env['res.users'].sudo().browse(uid)
        api_key_id = self.env['auth.api.token'].sudo().retrieve_from_user(user_id)

        return self._to_json(api_key_id.token)

    def _validator_create(self):
        return {
            'login': {'type': 'string', 'required': True, 'empty': False},
            'password': {'type': 'string', 'required': True, 'empty': False}
        }

    def _validator_return_create(self):
        return {
            'auth_token': {'type': 'string', 'required': True, 'empty': False},
        }

    def _to_json(self, token):
        return {
            'auth_token': token
        }
