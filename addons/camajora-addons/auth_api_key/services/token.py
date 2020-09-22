import logging
from werkzeug.exceptions import MethodNotAllowed
from odoo.addons.component.core import Component
from odoo.addons.base_rest.components.service import skip_secure_response
from odoo.exceptions import AccessDenied, ValidationError, MissingError

_logger = logging.getLogger(__name__)

class TokenService(Component):
    _inherit = 'base.rest.service'
    _name = 'token.service'
    _usage = 'token'
    _collection = 'auth.services'

    def create(self, **data):
        try:
            uid = self.env['res.users'].sudo()._login(self.env.cr.dbname, data['login'], data['password'])
        except AccessDenied as e:
            raise AccessDenied()
        
        if not uid:
            raise AccessDenied()
        
        user_id = self.env['res.users'].sudo().browse(uid)
        api_key_id = self.env['auth.api.token'].sudo().retrieve_from_user(user_id)

        response = {"auth_token": api_key_id.token}

        return response
    
    def _validator_create(self):
        return {
            'login': {"type": "string", "required": True, "empty": False},
            'password': {"type": "string", "required": True, "empty": False}
        }
    
    def _validator_return_create(self):
        return {
            'auth_token': {"type": "string", "required": True, "empty": False},
        }
    
