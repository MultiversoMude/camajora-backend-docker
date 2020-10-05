# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class RentalAvailability(models.Model):

    _name = 'rental.availability'
    _description = 'Rental Availability'

    name = fields.Char(string=_('Name'))
    description = fields.Char(string=_('Description'))
