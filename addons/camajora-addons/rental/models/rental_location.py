# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class RentalLocation(models.Model):

    _name = 'rental.location'
    _description = 'Rental Location'

    name = fields.Char(string=_('Name'))
    description = fields.Char(string=_('Description'))
    partner_id = fields.Many2one('res.partner', string=_('Owner'))
