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

    booking_ids = fields.One2many('rental.booking', 'user_id', string=_('Bookings'))

    booking_users = fields.Many2many(
        string=_('Booking Users'),
        compute="_compute_booking_users"
    )

    def _compute_is_owner(self):
        for record in self:
            record.is_owner = record.user_ids and (
                self.env.ref("rental.group_rental_owner")
                in record.user_ids[0].groups_id
            )

    def _compute_booking_users(self):
        for record in self:
            booking_users = self.env['res.partner'].search([
                ('booking_ids.slot_ids.resource_instance_id.resource_id.partner_id.id', '=', record.id)
            ])
            record.booking_users = [(6, 0, booking_users.ids)]
