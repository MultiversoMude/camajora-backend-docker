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
        }

    # VALIDATORS

    def _get_object_schema(self):
        return {
            "name": {"type": "string", "required": True, "empty": False},
        }
