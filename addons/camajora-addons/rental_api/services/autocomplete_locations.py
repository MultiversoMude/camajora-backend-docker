# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component

import logging

_logger = logging.getLogger(__name__)


class AutocompleteLocationService(Component):
    _inherit = "base.rest.public.service"
    _name = "autocomplete_locations.service"
    _usage = "autocomplete_locations"
    _description = "Camajora public services: autocomplete locations"

    # OPERATIONS

    def search(self, offset=0, limit=10, **params):
        """
        Get all Locations
        """
        location_data = (
            self.env["rental.location"]
                .sudo()
                .read_group(
                domain=[],
                fields=["state_id"],
                groupby=["state_id"],
            )
        )

        state_ids = [l["state_id"][0] for l in location_data]

        domain = [("id", "in", state_ids), ("country_id.code", "=", "IT")]

        term = params.pop("term", None)
        if term:
            domain.append(("name", "ilike", term))

        location_ids = (
            self.env["res.country.state"]
                .sudo()
                .search(domain, offset=offset, limit=limit)
        )

        return self._to_json(location_ids, many=True, offset=offset)

    # SERIALIZERS

    def _serialize(self, state_id):
        return {
            "name": state_id.name,
        }

    # VALIDATORS

    def _validator_search(self):
        return {
            "term": {"type": "string", "required": False},
        }

    def _get_object_schema(self):
        return {
            "name": {"type": "string", "required": True, "empty": False},
        }
