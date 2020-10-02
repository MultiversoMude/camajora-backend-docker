# Copyright 2019 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class RentalResourceCategory(models.Model):

    _name = 'rental.resource.category'
    _description = 'Rental Resource Category'

    name = fields.Char(string=_('Name'))
    description = fields.Char(string=_('Description'))
