# Copyright 2020 Metadonors srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base_rest.controllers import main


class AuthApiController(main.RestController):
    _root_path = '/api/v1/auth/'
    _collection_name = 'rest.auth.public.services'
    _default_auth = 'public'
    _cors = '*'


class CurrentUserApiController(main.RestController):
    _root_path = '/api/v1/auth/user/'
    _collection_name = 'rest.auth.services'
    _default_auth = 'api_key'
    _cors = '*'
