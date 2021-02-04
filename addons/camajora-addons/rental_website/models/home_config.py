# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class Homepage(models.Model):

    _name = 'rental.website.home'
    _description = 'Homepage configuration'

    title = fields.Char(string=_('Title'))
    subtitle = fields.Char(string=_('Subtitle'))
    image = fields.Binary(string=_('Cover Image'))

    explore_title = fields.Char(string=_('Explore Title'))
    explore_subtitle = fields.Char(string=_('Explore Subtitle'))

    about_text_left = fields.Text(string=_('About Text Left'))
    about_text_right = fields.Text(string=_('About Text Right'))
