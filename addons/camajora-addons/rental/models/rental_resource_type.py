# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class RentalResourceType(models.Model):

    _name = 'rental.resource.type'
    _description = 'Rental Resource Type'

    name = fields.Char(string=_('Name'))
    description = fields.Char(string=_('Description'))
    active = fields.Boolean(default=True, string=_('Active'))

    # price = fields.Integer(default=0, help='Price...')
    image = fields.Binary(string=_('Image'))

    category_id = fields.Many2one('rental.resource.category', string=_('Category'))
    setup_id = fields.Many2one('rental.resource.setup', string=_('Setup'))
    size_id = fields.Many2one('rental.resource.size', string=_('Size'))
    performance_id = fields.Many2one('rental.resource.performance', string=_('Performance'))
    availability_id = fields.Many2one('rental.availability', string=_('Availability'))
    duration_id = fields.Many2one('rental.duration', string=_('Duration'))

    resources_ids = fields.One2many('rental.resource', 'type_id', string=_('Resources'))

    slots_count = fields.Integer(compute='_compute_slots_count', store=True)

    def _compute_slots_count(self):
        for record in self:
            instances = self.env['rental.resource.instance'].search(
                [('resource_id', 'in', record.resources_ids.ids)]
            )
            record.slots_count = sum([r.booking_slots_count for r in instances])
