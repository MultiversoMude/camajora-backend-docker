# Copyright 2020 Metadonors srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class HomeService(Component):
    _inherit = 'base.rest.public.service'
    _name = 'website.service'
    _usage = 'home'
    _description = 'Camajora home configuration'

    def search(self):
        """
        Get home config
        """
        home_config = self.env['rental.website.home'].sudo().search([])
        if not home_config:
            return {
                'title': '',
                'subtitle': '',
                'image': '',
                'explore_title': '',
                'explore_subtitle': '',
                'about_text_left': '',
                'about_text_right': '',
            }
        return self._serialize(home_config[0])

    # PRIVATE METHODS

    def _serialize(self, record):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        image_url = '{}/api/v1/public/images/{}?model=rental.website.home'.format(
            base_url,
            record.id,
        )


        data = {}
        data['title'] = record.title
        data['subtitle'] = record.subtitle
        data['image'] = image_url
        data['explore_title'] = record.explore_title
        data['explore_subtitle'] = record.explore_subtitle
        data['about_text_left'] = record.about_text_left
        data['about_text_right'] = record.about_text_right
        return data

    # VALIDATORS

    def _validator_search(self):
        return {}

    def _validator_return_search(self):
        return {
            'title': {'type': 'string', 'required': True, 'empty': True},
            'subtitle': {'type': 'string', 'required': True, 'empty': True},
            'image': {'type': 'string', 'required': True, 'empty': True},
            'explore_title': {'type': 'string', 'required': True, 'empty': True},
            'explore_subtitle': {'type': 'string', 'required': True, 'empty': True},
            'about_text_left': {'type': 'string', 'required': True, 'empty': True},
            'about_text_right': {'type': 'string', 'required': True, 'empty': True},
        }
