# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging

log = logging.getLogger(__name__)


class RentalBooking(models.Model):

    _inherit = 'rental.booking'

    credits_used = fields.Integer(string=_('Credits Used'), readonly=True, compute='_compute_credits_used')

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.user_id.write({
            'credits': res.user_id.credits - res.total_credits
        })
        return res

    @api.constrains('user_id')
    def _check_user_credits(self):
        for record in self:
            if record.user_id.credits < record.total_credits:
                raise ValidationError('Not enough credits')

    def _compute_credits_used(self):
        for record in self:
            total_credits = 0
            for slot_id in record.slot_ids:
                total_credits += (
                    slot_id.total_hours *
                    slot_id.resource_instance_id.resource_id.credit_cost  # hourly credit cost
                    # applicare sconto
                )
            record.total_credits = total_credits
