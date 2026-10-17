# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class RentalResource(models.Model):

    _inherit = 'rental.resource'

    _sql_constraints = [(
        'positive_credit_cost',
        'check(credit_cost > 0)',
        _('Credit cost must be positive')
    )]

    credit_cost = fields.Integer(string=_('Credit Cost'), required=True)
