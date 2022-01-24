# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
import logging

log = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credits = fields.Integer(string=_("Available credits"))

    check_superuser = fields.Boolean(string=_("Check Super user"), compute='_compute_showing_credits',
                                     readonly=True, store=False)

    credits_available = fields.Integer(string=_("Credits"), compute='_compute_credits', readonly=True,
                                       store=False)

    @api.model
    def _compute_showing_credits(self):

        log.debug(self, 'Check current user is superuser ', self.env.context.get('active_id'))

        try:
            self.check_superuser = self.env.user.has_group('rental.group_rental_superuser')


        except:
            self.check_superuser = False

    @api.model
    def _compute_credits(self):
        self.credits_available = self.credits
