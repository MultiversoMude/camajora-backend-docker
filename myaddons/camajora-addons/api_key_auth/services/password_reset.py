# Copyright 2020 Metadonors srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.component.core import Component
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PasswordResetService(Component):
    _inherit = 'base.rest.service'
    _name = "password_reset.service"
    _usage = 'password_reset'
    _collection = 'rest.auth.public.services'
    _description = 'Camajora public services: password reset service'

    def check_token(self, token):
        """
        Check token validity
        """
        partner_id = self.env['res.partner'].sudo()._signup_retrieve_partner(token)

        if not partner_id:
            raise ValidationError("Token missing or expired")

        data = {}
        data['name'] = partner_id.name
        data['email'] = partner_id.email
        return data

    def _validator_check_token(self):
        return {'token': {'type': 'string', "required": True}}

    def _validator_return_check_token(self):
        return {
            'name': {'type': 'string', 'required': True, 'empty': False},
            'email': {'type': 'string', 'required': True, 'empty': False},
        }

    def send_email(self, email):
        """
        Send password reset email
        """

        user_id = self.env['res.users'].sudo().search([('login', '=', email)])

        if not user_id:
            user_id = self.env['res.users'].sudo().search([('partner_id.email', '=', email)])
            if not user_id:
                raise ValidationError("Token missing or expired")

        user_id[0]._send_partner_password_reset()

        return {}

    def _validator_send_email(self):
        return {'email': {'type': 'string', "required": True}}

    def _validator_return_send_email(self):
        return {}

    def reset(self, token, password):
        """
        Reset user password
        """
        partner_id = self.env['res.partner'].sudo()._signup_retrieve_partner(token)

        if not password:
            raise ValidationError("Password cannot be empty")

        if not partner_id:
            raise ValidationError("Token missing or expired")

        user_id = self.env['res.users'].sudo().search([('partner_id', '=', partner_id.id)])

        user_id.sudo().write({"password": password})
        # partner_id.write({ "signup_token": False })

        return {}

    def _validator_reset(self):
        return {
            'token': {'type': 'string', "required": True},
            'password': {'type': 'string', "required": True},
        }

    def _validator_return_reset(self):
        return {}
