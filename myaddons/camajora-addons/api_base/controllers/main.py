# Copyright 2020 Metadonors srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base_rest.controllers import main


class PublicApiController(main.RestController):
    _root_path = '/api/v1/public/'
    _collection_name = 'base.rest.public.services'
    _default_auth = 'public'


class PrivateApiController(main.RestController):
    _root_path = '/api/v1/'
    _collection_name = 'base.rest.private.services'
    _default_auth = 'api_key'
