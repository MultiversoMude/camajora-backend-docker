from odoo.addons.component.core import Component


class CreditProductsService(Component):
    _inherit = 'products.service'
    _name = 'credit_products.service'
    _usage = 'credits'
    _collection = 'base.rest.public.shop.services'

    def _retrieve_products(self, **params):
        domain = [('is_credits', '=', True), ('website_ok', '=', True)]
        return self.env['product.template'].sudo().search(domain, offset=0, limit=1000)
