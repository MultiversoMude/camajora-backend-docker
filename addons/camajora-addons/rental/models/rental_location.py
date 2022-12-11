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

    address = fields.Char(string=_("Address"), required=True)
    postal_code = fields.Char(string=_("Zip"), required=True)
    city = fields.Char(track_visibility='onchange', string=_('City'), required=True)
    state_id = fields.Many2one("res.country.state", string=_('State'), required=True)
    country_id = fields.Many2one('res.country', string=_('Country'), required=True)
    resource_ids = fields.One2many('rental.resource', 'location_id', string=_('Resources'), required=True)

    latitudo = fields.Float(sting=_('Lat.'), required=False)
    longitudo = fields.Float(sting=_('Lon.'), required=False)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        backend = self.env.context.get('backend')

        if backend is not None:
            current_owner = self.env['res.partner'].search([('id', '=', self.env.user.partner_id.id)])

            if current_owner:
                args = [] if args is None else args.copy()
                if current_owner.parent_id is not None and current_owner.parent_id is not False:
                    args.append(('partner_id', 'in', [current_owner.id, current_owner.parent_id.id]))
                else:
                    args.append(('partner_id', '=', current_owner.id))

            _logger.debug("Location search args in backend mode:%s", args)

        return super(RentalLocation, self).search(args, offset, limit, order, count)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        current_owner = self.env['res.partner'].sudo().search([('id', '=', self.env.user.partner_id.id)])
        args = [] if args is None else args.copy()
        args += [('partner_id', '=', current_owner.id)]
        return super(RentalLocation, self).name_search(name, args, operator, limit)
