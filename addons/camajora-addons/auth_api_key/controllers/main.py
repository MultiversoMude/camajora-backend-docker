from odoo.addons.base_rest.controllers import main

class AuthApiController(main.RestController):
    _root_path = '/api/auth/'
    _collection_name = 'auth.services'
    _default_auth = 'public'
    _cors = '*'

class CurrentUserApiController(main.RestController):
    _root_path = '/api/users/'
    _collection_name = 'current_user.services'
    _default_auth = 'api_key'
    _cors = '*'