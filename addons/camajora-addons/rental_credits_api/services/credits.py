# Copyright 2020 Metadonors srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component
from odoo.exceptions import MissingError


class CreditService(Component):
    _inherit = 'base.rest.private.service'
    _name = 'credit.service'
    _usage = 'credits'
    _description = 'Camajora private services: credits operations demo (no $ transactions)'

    def search(self):
        """
        Get current logged user credits
        """
        return self._serialize(self._get_user())

    def create(self, **kwargs):
        """
        Buy credits for current logged user
        """
        user = self._get_user()

        credits = user.partner_id.credits
        credits += kwargs.get('quantity', 0)

        user.partner_id.write({'credits': credits})

        return self._serialize(user)

    # PRIVATE  METHODS

    def _get_user(self):
        if self.env.user.login == 'public':
            raise MissingError('User not found')
        return self.env.user

    def _serialize(self, record):
        data = {}
        data['credits'] = record.partner_id.credits
        return data

    # VALIDATORS

    def _validator_search(self):
        return {}

    def _validator_return_search(self):
        return {
            'credits': {'type': 'integer', 'required': True, 'empty': False}
        }

    def _validator_create(self):
        return {
            'quantity': {'type': 'integer', 'coerce': to_int, 'required': True, 'empty': False}
        }

    def _validator_return_create(self):
        return self._validator_return_search()
