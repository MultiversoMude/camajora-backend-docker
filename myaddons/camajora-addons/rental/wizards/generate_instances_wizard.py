# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
import logging

log = logging.getLogger(__name__)


class GenerateInstancesWizard(models.TransientModel):
    _name = 'rental.resource.instance.wizard'
    _description = 'Wizard per generazione massiva di istanze di risorse'

    count = fields.Integer(string=_("Number of Instances"), help=_("Number of Instances"), default=1)
    equipments_ids = fields.Many2many('rental.resource.equipment', string=_('Equipments'))

    def generate_instances(self):
        """Generates the number of resource instances entered in wizard field 'count'"""

        resource = self.env['rental.resource'].browse(self.env.context.get('active_id'))

        count = self.env['rental.resource.instance'].search(
            [('resource_id', '=', resource.id)]
        )

        if len(count) == 0:
            self.env['rental.resource.instance'].create({
                'resource_id': resource.id,
                'equipments_ids': [(6, 0, self.equipments_ids.ids)]
            })
