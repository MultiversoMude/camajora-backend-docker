# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class RentalResourceInstance(models.Model):

    _name = 'rental.resource.instance'
    _description = 'Rental Resource Instance'

    name = fields.Char(string=_('Name'), readonly=True, default=lambda self: _('New'), compute='_compute_name')
    code = fields.Char(string=_('SKU'), readonly=True)
    active = fields.Boolean(default=True, string=_('Active'))

    resource_id = fields.Many2one('rental.resource', string=_('Resource'), required=True, ondelete='cascade')
    equipments_ids = fields.Many2many('rental.resource.equipment', string=_('Equipments'))

    booking_slots_ids = fields.One2many(
        'rental.booking.slot', 'resource_instance_id', string=_('Booking Slots')
    )

    def _compute_name(self):
        for record in self:
            record.name = ' '.join([
                record.resource_id.name,
                record.code
            ])

    @api.model
    def create(self, vals):
        resource_id = self.env['rental.resource'].search([
            ('id', '=', vals['resource_id'])
        ])
        vals['code'] = '{}-{}'.format(
            resource_id.code,
            self.env['ir.sequence'].next_by_code('rental.resource.instance.code')
        )
        return super().create(vals)
