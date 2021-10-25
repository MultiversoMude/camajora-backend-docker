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

    resource_id = fields.Many2one('rental.resource', string=_('Resources'),
                                  default=lambda self: self._default_resource())

    instances_ids = fields.Many2one('rental.resource.instance', string=_('Instances'))

    name = fields.Char(string=_('SKU'))
    # Campi per la creazione di una prenotazione
    user_id = fields.Many2one('res.partner', string=_('User'))
    date = fields.Date(string=_('Date'), default=lambda self: fields.Date.today())

    # Stati finali
    token = fields.Char(string=_('Secret Token'), readonly=True)
    qr_code = fields.Binary(string=_('QR Code'), readonly=True)

    @api.onchange('resource_id')
    def onchange_resource(self):
        domain = [('resource_id', '=', self.resource_id.id)]
        self.instances_ids = self.env['rental.resource.instance'].search(domain)

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
        resource = self.env['rental.resource'].search([('id', '=', self.env.context.get('active_id'))])
        return resource.location_id

    @api.model
    def _default_resource(self):
        selected_ids = self.env.context.get('active_ids', [])
        selected_records = self.env['rental.resource'].browse(selected_ids)
        return selected_records

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
