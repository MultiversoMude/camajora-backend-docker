# Copyright 2019 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class RentalBookingSlot(models.Model):

    _name = 'rental.booking.slot'
    _description = 'Rental Booking Slot'

    name = fields.Char(related='resource_instance_id.name', string=_('SKU'))
    booking_id = fields.Many2one('rental.booking', string=_('Booking'))
    resource_instance_id = fields.Many2one('rental.resource.instance', string=_('Resource Instance'))
    duration_id = fields.Many2one('rental.duration', string=_('Duration'))

    start_date = fields.Date(string=_('Start Date'))
    end_date = fields.Date(string=_('End Date'))
    start_time = fields.Integer(string=_('Start Time'))
    total_hours = fields.Integer(string=_('Hours'))

    qr_code = fields.Char(string=_('Code'), readonly=True)

    @api.model
    def create(self, vals):
        """
        vals['qr_code'] = '+'.join[
            vals['resource_instance_id'].location.name,
            vals['resource_instance_id'].id,
            vals['resource_instance_id'].resource_id.type_id.id,
            vals['start_date'],
            vals['booking_id'].sku,
        ]
        """
        return super().create(vals)
