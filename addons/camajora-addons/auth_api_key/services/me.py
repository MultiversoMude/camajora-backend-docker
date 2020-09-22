import logging
from werkzeug.exceptions import MethodNotAllowed
from odoo.addons.component.core import Component
from odoo.addons.base_rest.components.service import skip_secure_response
from odoo.exceptions import AccessDenied, ValidationError, MissingError

_logger = logging.getLogger(__name__)

class CurrentUserService(Component):
    _inherit = 'base.rest.service'
    _name = 'me.service'
    _usage = 'me'
    _collection = 'current_user.services'

    def search(self):
        if self.env.user.login == "public":
            raise MissingError("User not found")
        return self._serialize(self.env.user)
    
    def _validator_search(self):
        return {}
    
    def _validator_return_search(self):
        return {
            'id': {"type": "integer", "required": True, "empty": False},
            'partner_id': {"type": "integer", "required": True, "empty": False},
            'name': {"type": "string", "required": True, "empty": False},
            'email': {"type": "string", "required": True, "empty": False},
        }
    
    def _serialize(self, record):
        data = {}
        data['id'] = record.id
        data['partner_id'] = record.partner_id.id
        data['name'] = record.partner_id.name
        data['email'] = record.login

        return data
    
