# Copyright 2019 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class RentalBooking(models.Model):

    _name = 'rental.booking'
    _description = 'Rental Booking'

    name = fields.Char(string=_('SKU'), readonly=True)
    date = fields.Date(string=_('Date'))
    user_id = fields.Many2one('res.partner', string=_('User'))

    total_credits = fields.Integer(string=_('Credits Used'), readonly=True, compute='_compute_total_credits')

    rent_channel = fields.Selection([
        ('main_site', _('Main Site')),
        ('phone', _('Phone')),
        ('external_site', _('External Site')),
        ('location', _('Location')),
        ('app', _('App')),
    ], string=_('Rent Channel'), default='main_site')

    slot_ids = fields.One2many('rental.booking.slot', 'booking_id', string=_('Slots'))
    slot_count = fields.Integer(string=_('Total Slots'), compute='_compute_slot_count')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('rental.booking.sku')
        return super().create(vals)

    def _compute_total_credits(self):
        for record in self:
            total_credits = 0
            for slot_id in record.slot_ids:
                total_credits += (
                    slot_id.total_hours *
                    1  # costo orario in crediti della risorsa
                )
            record.total_credits = total_credits

    def _compute_slot_count(self):
        for record in self:
            count = self.env['rental.booking.slot'].search(
                [('booking_id', '=', record.id)]
            )
            record.slot_count = len(count)
