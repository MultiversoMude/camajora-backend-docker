import logging

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class BookingService(Component):
    _inherit = 'booking.service'

    def _serialize_one_slot(self, line):
        serialized = super()._serialize_one_slot(line)

        if line.resource_instance_id.resource_id.image_ids:
            serialized['image'] = line.resource_instance_id.resource_id.image_ids[0].image_id.file_id.url

        return serialized
