# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class LocationService(Component):
    _inherit = 'base.rest.public.service'
    _name = "location.service"
    _usage = "locations"
    _description = "Camajora public services: get all locations"

    # OPERATIONS

    def get(self, _id):
        """
        Get Location by ID
        """
        location_id = self.env["rental.location"].sudo().search([("id", "=", _id)])

        return self._to_json(location_id)

    def search(self, offset=0, limit=None, **params):
        """
        Get all Locations
        """
        location_ids = (
            self.env["rental.location"].sudo().search([], offset=offset, limit=limit)
        )

        return self._to_json(location_ids, many=True, offset=offset)

    # SERIALIZERS

    def _serialize(self, location_id):
        return {
            "name": location_id.name,
            "address": location_id.address or "",
            "postal_code": location_id.postal_code or "",
            "city": location_id.city or "",
            "state": location_id.state_id.name if location_id.state_id else "",
            "state_code": location_id.state_id.code if location_id.state_id else "",
            "country": location_id.country_id.name if location_id.country_id else "",
            "state_id": location_id.state_id.id,
            "country_id": location_id.country_id.id,
        }

    # VALIDATORS

    def _get_object_schema(self):
        return {
            "name": {"type": "string", "required": True, "empty": False},
            "address": {"type": "string", "required": False, "empty": True},
            "postal_code": {"type": "string", "required": False, "empty": True},
            "city": {"type": "string", "required": False, "empty": True},
            "state": {"type": "string", "required": False, "empty": True},
            "state_code": {"type": "string", "required": False, "empty": True},
            "country": {"type": "string", "required": False, "empty": True},
            "state_id": {'type': 'integer', 'required': False, 'empty': True},
            "country_id": {'type': 'integer', 'required': False, 'empty': True},
        }
