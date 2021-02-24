# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class ResPartner(models.Model):

    _inherit = 'res.partner'

    fiscal_code = fields.Char(string=_('Fiscal Code'), required=False)
    invoice_recipient_code = fields.Char(string=_('Invoice Recipient Code'), required=False)
    pec_address = fields.Char(string=_('PEC Address'), required=False)
    is_owner = fields.Boolean(
        string=_('Is Owner'),
        compute="_compute_is_owner"
    )

    def _compute_is_owner(self):
        for record in self:
            record.is_owner = record.user_ids and (
                self.env.ref("rental.group_rental_owner")
                in record.user_ids[0].groups_id
            )
