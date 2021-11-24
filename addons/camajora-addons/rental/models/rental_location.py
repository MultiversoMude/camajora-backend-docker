# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, api, models, _
import logging

_logger = logging.getLogger(__name__)


class RentalLocation(models.Model):
    _name = 'rental.location'
    _description = 'Rental Location'

    name = fields.Char(string=_('Name'), required=True)
    description = fields.Char(string=_('Description'))
    partner_id = fields.Many2one('res.partner', string=_('Owner'), default=lambda self: self.env['res.partner'].search(
        [('id', '=', self.env.user.partner_id.id)]))

    address = fields.Char(string=_("Address"))
    postal_code = fields.Char(string=_("Zip"))
    city = fields.Char(track_visibility='onchange', string=_('City'))
    state_id = fields.Many2one("res.country.state", string=_('State'))
    country_id = fields.Many2one('res.country', string=_('Country'))
    resource_ids = fields.One2many('rental.resource', 'location_id', string=_('Resources'), required=True)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):

        current_owner = self.env['res.partner'].search([('id', '=', self.env.user.partner_id.id)])

        if current_owner:
            args = [] if args is None else args.copy()
            args.append(('partner_id', '=', current_owner.id))
            _logger.debug("Args:%s", args)

        return super(RentalLocation, self).search(args, offset, limit, order, count)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        current_owner = self.env['res.partner'].sudo().search([('id', '=', self.env.user.partner_id.id)])
        args = [] if args is None else args.copy()
        args += [('partner_id', '=', current_owner.id)]
        return super(RentalLocation, self).name_search(name, args, operator, limit)
