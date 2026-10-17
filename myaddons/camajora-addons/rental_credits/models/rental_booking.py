# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging

log = logging.getLogger(__name__)


class RentalBooking(models.Model):
    _inherit = 'rental.booking'

    credits_used = fields.Integer(string=_('Credits Used'), readonly=True, compute='_compute_credits_used')

    def action_confirm(self):
        if self.user_id.credits < self.credits_used:
            raise ValidationError('Not enough credits')

        res = super().action_confirm()

        self.user_id.write({
            'credits': self.user_id.credits - self.credits_used
        })

        return res

    def _compute_credits_used(self):
        for record in self:
            credit_cost = 0
            for slot_id in record.slot_ids:
                credit_cost += (
                        slot_id.total_hours *
                        (slot_id.resource_instance_id.resource_id.credit_cost / 3600)  # hourly credit cost
                    # applicable discount
                )
            record.credits_used = credit_cost
