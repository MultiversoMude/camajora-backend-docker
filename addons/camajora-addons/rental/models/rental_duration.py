# Copyright 2019 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class RentalDuration(models.Model):

    _name = 'rental.duration'
    _description = 'Rental Duration'

    _sql_constraint = [(
        'unique_type',
        'unique(type)',
        'There can be only one rental duration per duration type'
    )]

    name = fields.Char(string=_('Name'))
    description = fields.Char(string=_('Description'))
    discount = fields.Float(string=_('Discount'))

    type = fields.Selection([
        ('hourly', _('Hourly')),
        ('half_daily', _('Half daily')),
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
    ], string=_('Type'), default='hourly')
