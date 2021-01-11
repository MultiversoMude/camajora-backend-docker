# Copyright 2020 Metadonors srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class SignupService(Component):
    _inherit = 'base.rest.service'
    _name = 'signup.service'
    _usage = 'signup'
    _collection = 'rest.auth.public.services'
    _description = 'Camajora public services: signup user'

    def create(self, **values):
        """
        Register a new user
        """

        country_id = self.env['res.country'].sudo().search([
            ('code', '=', 'IT')
        ], limit=1)

        partner_id = self.env['res.partner'].sudo().create({
            'name': values['name'],
            'email': values['email'],
            'country_id': country_id.id
        })

        user_id = self.env['res.users'].sudo().create({
            'partner_id': partner_id.id,
            'login': values['email'],
            'new_password': values['password']
        })

        api_key_id = self.env['auth.api.token'].sudo().retrieve_from_user(user_id)

        return self._to_json(api_key_id.token)

    def _validator_create(self):
        return {
          "name": {"type": "string", "required": True, "empty": False},
          "email": {"type": "string", "required": True, "empty": False},
          "password": {"type": "string", "required": True, "empty": False},
        }

    def _validator_return_create(self):
        return {
            'auth_token': {'type': 'string', 'required': True, 'empty': False},
        }

    def _to_json(self, token):
        return {
            'auth_token': token
        }
