# Copyright 2019 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class RentalResourceInstance(models.Model):

    _name = 'rental.resource.instance'
    _description = 'Rental Resource Instance'

    name = fields.Char(string=_('SKU'), readonly=True)
    active = fields.Boolean(default=True, string=_('Active'))

    resource_id = fields.Many2one('rental.resource', string=_('Resource'))
    equipments_ids = fields.Many2many('rental.resource.equipment', string=_('Equipments'))

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('rental.resource.instance.code')
        return super().create(vals)
