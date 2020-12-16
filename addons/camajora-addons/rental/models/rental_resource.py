# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class RentalResource(models.Model):

    _name = 'rental.resource'
    _description = 'Rental Resource'

    name = fields.Char(string=_('Name'), readonly=True, default=lambda self: _('New'), compute='_compute_name')
    code = fields.Char(string=_('Code'), required=True, copy=False, readonly=True, index=True)
    active = fields.Boolean(default=True, string=_('Active'))

    type_id = fields.Many2one('rental.resource.type', string=_('Type'), required=True)
    location_id = fields.Many2one('rental.location', string=_('Location'), required=True)
    partner_id = fields.Many2one('res.partner', related='location_id.partner_id', string=_('Owner'), required=True)
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
