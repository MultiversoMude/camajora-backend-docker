from odoo.addons.component.core import Component
import logging

_logger = logging.getLogger(__name__)


class BookingSlotsService(Component):
    _inherit = 'booking.slots.service'

    def _serialize(self, record):
        serialized = super()._serialize(record)
        _logger.info('~~~~~~~~~~~')
        _logger.info('~~~~~~~~~~~')
        _logger.info('~~~~~~~~~~~')
        _logger.info('~~~~~~~~~~~')
        _logger.info('~~~~~~~~~~~')

        if record.resource_instance_id.resource_id.image_ids:
            serialized['image'] = record.resource_instance_id.resource_id.image_ids[0].image_id.file_id.url

        _logger.info(record)
        _logger.info(record.resource_instance_id)
        _logger.info(record.resource_instance_id.resource_id)
        _logger.info(record.resource_instance_id.resource_id.image_ids)
        _logger.info(serialized['image'])
        _logger.info('~~~~~~~~~~~')
        _logger.info('~~~~~~~~~~~')
        _logger.info('~~~~~~~~~~~')
        _logger.info('~~~~~~~~~~~')
        _logger.info('~~~~~~~~~~~')
        return serialized
