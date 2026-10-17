from odoo.addons.base_rest.controllers import main


class PrivateShopApiController(main.RestController):
    _root_path = '/api/v1/shop/'
    _collection_name = 'base.rest.private.shop.services'
    _default_auth = 'api_key'


class PublicShopApiController(main.RestController):
    _root_path = '/api/v1/shop/public/'
    _collection_name = 'base.rest.public.shop.services'
    _default_auth = 'public'
