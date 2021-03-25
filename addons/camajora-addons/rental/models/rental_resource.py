# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from .rental_booking_slot import compute_range
import logging

_logger = logging.getLogger(__name__)


class RentalResource(models.Model):

    _name = 'rental.resource'
    _description = 'Rental Resource'
    _order = 'create_date DESC'

    image = fields.Binary(string=_('Image'))
    name = fields.Char(string=_('Name'), readonly=True, default=lambda self: _('New'), compute='_compute_name')
    description = fields.Char(string=_('Description'))
    code = fields.Char(string=_('Code'), required=False, copy=False, readonly=True, index=True)
    active = fields.Boolean(default=True, string=_('Active'))

    category_id = fields.Many2one('rental.resource.category', string=_('Category'), store=True, related='type_id.category_id')
    setup_id = fields.Many2one('rental.resource.setup', string=_('Setup'), store=True, related='type_id.setup_id')
    size_id = fields.Many2one('rental.resource.size', string=_('Size'), store=True, related='type_id.size_id')
    performance_id = fields.Many2one('rental.resource.performance', string=_('Performance'), related='type_id.performance_id', store=True,)
    availability_id = fields.Many2one('rental.availability', string=_('Availability'), related='type_id.availability_id', store=True,)
    duration_id = fields.Many2one('rental.duration', string=_('Duration'), related='type_id.duration_id', store=True,)

    type_id = fields.Many2one('rental.resource.type', string=_('Type'), required=True)
    location_id = fields.Many2one('rental.location', string=_('Location'), required=True)
    partner_id = fields.Many2one('res.partner', related='location_id.partner_id', store=True, string=_('Owner'), required=True)
    instances_ids = fields.One2many('rental.resource.instance', 'resource_id', string=_('Instances'), required=True)

    instance_count = fields.Integer(string=_('Total Instances'), compute='_compute_instance_count')

    def _compute_name(self):
        for record in self:
            if record.type_id and record.type_id.category_id and record.location_id:
                record.name = ' '.join([
                    record.type_id.category_id.name,
                    record.location_id.name
                ])

    def _compute_instance_count(self):
        for record in self:
            count = self.env['rental.resource.instance'].search(
                [('resource_id', '=', record.id)]
            )
            record.instance_count = len(count)

    @api.multi
    def action_open_instances(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Resource Instances',
            'res_model': 'rental.resource.instance',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('resource_id', '=', self.id)],
            'context': {'default_resource_id': self.id},
        }

    @api.multi
    def action_open_calendar(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Booking Calendar',
            'res_model': 'rental.booking.slot',
            'view_type': 'tree',
            'view_mode': 'calendar',
            'target': 'current',
            'domain': [('resource_instance_id', 'in', self.instances_ids)],
        }

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('rental.resource.code') or _('New')
        return super().create(vals)

    def get_best_instance_match(self, **kwargs):
        slot_range = compute_range(
            kwargs['duration'],
            fields.Date.from_string(kwargs['start_date']),
            fields.Date.from_string(kwargs['end_date']),
            kwargs['start_time'],
            kwargs['end_time'],
            kwargs['half_day_type'],
        )

        dt_start = slot_range['dt_start']
        dt_end = slot_range['dt_end']

        for record in self:
            domain = [
                ('resource_id', '=', record.id),
                '|',
                    '|',
                        '&', ('booking_slots_ids.dt_start', '>', dt_start), ('booking_slots_ids.dt_start', '>', dt_end),
                        '&', ('booking_slots_ids.dt_end', '<', dt_start), ('booking_slots_ids.dt_end', '<', dt_end),
                    ('booking_slots_ids', '=', False)

            ]
            matches = self.env['rental.resource.instance'].sudo().search(domain, order='booking_slots_ids desc', limit=1)

            if len(matches) < 1:
                _logger.error('No free instances found, should always be at least one')
                return

            return matches[0].id
