# Copyright 2020 Metadonors srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import AbstractComponent
from odoo.exceptions import MissingError


class BaseCommonService(AbstractComponent):
    _inherit = "base.rest.service"
    _expose_model = None

    def _validator_search(self):
        return {
            "offset": {"type": "integer", 'coerce': to_int, "required": False, "nullable": True},
            "limit": {"type": "integer", 'coerce': to_int, "required": False, "nullable": True},
        }

    def _validator_return_search(self):
        return {
            "count": {"type": "integer", "required": True},
            "offset": {"type": "integer", "required": False, "empty": False},
            "results": {
                "type": "list",
                "required": True,
                "schema": {"type": "dict", "schema": self._validator_return_get()},
            },
        }

    def _validator_get(self):
        return {}

    def _validator_return_get(self):
        res = self._get_object_schema()
        res.update({"id": {"type": "integer", "required": True, "empty": False}})
        return res

    def _serialize_with_id(self, record_id):
        data = self._serialize(record_id)
        data.update({"id": record_id["id"]})
        return data

    def _to_json(self, payload, many=False, offset=0):

        if many:
            data = payload or []
            return {
                "count": len(data),
                "offset": offset,
                "results": [self._serialize_with_id(record_id) for record_id in data],
            }

        if not payload:
            raise MissingError("Record not found")

        return self._serialize_with_id(payload)


class BasePublicService(BaseCommonService):
    _name = "base.rest.public.service"
    _collection = "base.rest.public.services"


class BasePrivateService(BaseCommonService):
    _name = "base.rest.private.service"
    _collection = "base.rest.private.services"
