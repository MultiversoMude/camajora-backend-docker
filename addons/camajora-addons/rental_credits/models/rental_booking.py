# Copyright 2019 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.exceptions import ValidationError
import logging

log = logging.getLogger(__name__)


class RentalBooking(models.Model):

    _inherit = 'rental.booking'

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
