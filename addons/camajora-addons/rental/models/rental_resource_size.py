# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class RentalResourceSize(models.Model):

    _name = 'rental.resource.size'
    _description = 'Rental Resource Size'
    _order = 'sequence'

    name = fields.Char(string=_('Name'))
    description = fields.Char(string=_('Description'))
    sequence = fields.Integer(default=0)
