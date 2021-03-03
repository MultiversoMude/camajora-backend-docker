# Copyright 2020 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class UserService(Component):
    _inherit = "base.rest.private.service"
    _name = "user.service"
    _usage = "users"
    _description = "Camajora private services: get all users"

    # OPERATIONS

    def get(self, _id):
        """
        Get User by ID
        """
        user_id = (
            self.env["res.users"]
            .sudo()
            .search([("share", "=", True), ("id", "=", _id)])
        )

        return self._to_json(user_id)

    def search(self, offset=0, limit=None, **params):
        """
        Get all Users
        """
        user_ids = (
            self.env["res.users"]
            .sudo()
            .search([("share", "=", True)], offset=offset, limit=limit)
        )

        return self._to_json(user_ids, many=True, offset=offset)

    # SERIALIZERS

    def _serialize(self, user_id):
        return {
            "email": user_id.login,
            "name": user_id.partner_id.name,
            "partner_id": user_id.partner_id.id,
        }

    # VALIDATORS

    def _get_object_schema(self):
        return {
            "email": {"type": "string", "required": True, "empty": False},
            "name": {"type": "string", "required": True, "empty": False},
            "partner_id": {"type": "integer", "required": True},
        }
