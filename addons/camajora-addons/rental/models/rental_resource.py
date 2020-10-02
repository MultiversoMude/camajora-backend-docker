# Copyright 2019 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class RentalResource(models.Model):

    _name = 'rental.resource'
    _description = 'Rental Resource'

    name = fields.Char(string=_('Name'))
    code = fields.Char(string=_('Code'), readonly=True)
    active = fields.Boolean(default=True, string=_('Active'))

    type_id = fields.Many2one('rental.resource.type', string=_('Type'))
    location_id = fields.Many2one('rental.location', string=_('Location'))
    partner_id = fields.Many2one('res.partner', string=_('Owner'))
    instances_ids = fields.One2many('rental.resource.instance', 'resource_id', string=_('Instances'))

    instance_count = fields.Integer(string=_('Total Instances'), compute='_compute_instance_count')

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

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('rental.resource.code')
        return super().create(vals)

    @api.onchange('location_id')
    def _generate_name(self):
        for record in self:
            record.name = ' '.join([
                record.type_id.category_id.name,
                record.location_id.name,
                record.code
            ])
