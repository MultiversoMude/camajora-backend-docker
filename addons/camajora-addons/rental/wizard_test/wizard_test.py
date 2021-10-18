from odoo import api, fields, models, _
import logging

log = logging.getLogger(__name__)


class MyWizard(models.TransientModel):
    _name = 'my.wizard'
    _inherit = ['multi.step.wizard.mixin']

    location = fields.Many2one(
        comodel_name='rental.location',
        name="Location",
        required=True,
        ondelete='cascade',
        default=lambda self: self._default_project_id(),
    )

    location_id = fields.Integer(string=_('Id'), default=lambda self: self._default_project_id())

    resource_ids = fields.Many2one('rental.resource', string=_('Resources'))

    name = fields.Char(string=_('Name'), default='Test')
    field1 = fields.Char()
    field2 = fields.Char()
    field3 = fields.Char()

    @api.model
    def _selection_state(self):
        return [
            ('start', 'Start'),
            ('configure', 'Configure'),
            ('custom', 'Customize'),
            ('final', 'Final'),
        ]

    @api.model
    def _default_project_id(self):
        log.debug(self, 'active id is %s', self.env.context.get('active_id'))
        return self.env.context.get('active_id')

    def state_exit_start(self):
        self.state = 'configure'

    def state_exit_configure(self):
        self.state = 'custom'

    def state_exit_custom(self):
        log.debug(self, 'state_exit_custom id is %s', self.location_id)
        self.state = 'final'

    @api.model
    def _compute_current_id(self):
        log.debug(self, "Computing id")
        return self.env.context.get('active_id')
