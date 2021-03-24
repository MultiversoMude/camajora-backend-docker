# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class ResPartner(models.Model):

    _inherit = 'res.partner'

    fiscal_code = fields.Char(string=_('Fiscal Code'), required=False)
    invoice_recipient_code = fields.Char(string=_('Invoice Recipient Code'), required=False)
    pec_address = fields.Char(string=_('PEC Address'), required=False)
    is_owner = fields.Boolean(
        string=_('Is Owner'),
        compute="_compute_is_owner")

    booking_ids = fields.One2many(
        'rental.booking',
        'user_id',
        string=_("Bookings"))

    booking_count = fields.Integer(
        compute="_compute_booking_count",
        string=_("Total Bookings"))

    booking_slot_ids = fields.One2many(
        'rental.booking.slot',
        'partner_id',
        string=_("Bookings"))

    booking_slot_count = fields.Integer(
        compute="_compute_booking_count",
        string=_("Total Bookings Slots"))

    def action_slots(self):
        pass
    
    def action_booking_slots(self):
        pass

    @api.depends('booking_ids', 'booking_ids.slot_ids')
    def _compute_booking_count(self):
        for record in self:
            record.booking_count = len(record.booking_ids.filtered(lambda b: b.state == 'confirmed'))
            record.booking_slot_count = len(record.booking_slot_ids.filtered(lambda b: b.state == 'confirmed'))

    def _compute_is_owner(self):
        for record in self:
            record.is_owner = record.user_ids and (
                self.env.ref("rental.group_rental_owner")
                in record.user_ids[0].groups_id
            )
