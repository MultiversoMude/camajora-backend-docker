# Copyright 2020 Metadonors srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.component.core import Component
from odoo.exceptions import MissingError

_logger = logging.getLogger(__name__)


class CurrentUserService(Component):
    _inherit = 'base.rest.service'
    _name = 'me.service'
    _usage = 'me'
    _collection = 'rest.auth.services'
    _description = 'Auth services: get current logged user'

    def search(self):
        """
        Get current logged user
        """
        if self.env.user.login == 'public':
            raise MissingError('User not found')
        return self._serialize(self.env.user)

    def _validator_search(self):
        return {}

    def _validator_return_search(self):
        return {
            'id': {'type': 'integer', 'required': True, 'empty': False},
            'partner_id': {'type': 'integer', 'required': True, 'empty': False},
            'name': {'type': 'string', 'required': True, 'empty': False},
            'email': {'type': 'string', 'required': True, 'empty': False},
        }

    def _serialize(self, record):
        data = {}
        data['id'] = record.id
        data['partner_id'] = record.partner_id.id
        data['name'] = record.partner_id.name
        data['email'] = record.login

        return data
