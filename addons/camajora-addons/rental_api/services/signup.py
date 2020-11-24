import logging

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class SignupService(Component):
    _inherit = 'base.rest.public.service'
    _name = 'signup.service'
    _usage = 'signup'
    _description = 'Camajora public services: signup user'

    def create(self, **values):
        """
        Register a new user
        """

        partner_id = self.env['res.partner'].sudo().create({
            'name': values['name'],
            'email': values['email']
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
